import smtplib
from email.message import EmailMessage
from datetime import datetime, timezone
import requests
from fastapi import Depends, FastAPI, HTTPException, Request, Response, status, UploadFile, File
import logging
import sys
import traceback

# Use uvicorn logger for consistency in Render logs
logger = logging.getLogger("uvicorn.error")
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import uuid
import shutil
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded



from .auth import (
    check_rate_limit,
    clear_failed_attempts,
    create_access_token,
    get_client_ip,
    get_current_admin,
    register_failed_attempt,
    verify_password,
)
from .config import Settings, get_settings
from .database import get_db, engine, Base
from .models import ITEM_TYPES, Item, Tag, Testimonial

Base.metadata.create_all(bind=engine)
try:
    with engine.begin() as conn:
        conn.exec_driver_sql("ALTER TYPE item_type ADD VALUE IF NOT EXISTS 'blog'")
except Exception:
    pass
from .schemas import ItemCreate, ItemRead, ItemType, ItemUpdate, LoginRequest, TagCreate, TagRead, TokenResponse, TestimonialCreate, TestimonialRead, TestimonialUpdate, ContactRequest

app = FastAPI(title="Portfolio API", version="1.0.0")
settings = get_settings()

# Setup Rate Limiter
limiter = Limiter(key_func=get_client_ip)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_origin_regex=r"https://mon-portofolio-.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/login", response_model=TokenResponse)
def login(request: Request, payload: LoginRequest, settings: Settings = Depends(get_settings)) -> TokenResponse:
    check_rate_limit(request)
    valid_username = payload.username == settings.admin_username
    valid_password = verify_password(payload.password, settings.admin_password_hash)
    if not valid_username or not valid_password:
        register_failed_attempt(request)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Identifiants invalides.")

    clear_failed_attempts(request)
    return TokenResponse(access_token=create_access_token(settings.admin_username, settings))


@app.get("/api/items", response_model=list[ItemRead])
def list_items(type: ItemType | None = None, db: Session = Depends(get_db)) -> list[Item]:
    query = select(Item).order_by(Item.display_order.asc(), Item.created_at.desc(), Item.id.desc())
    if type is not None:
        query = query.where(Item.type == type)
    return list(db.scalars(query))

@app.get("/api/veille")
def get_veille(limit: int = 6) -> dict[str, object]:
    limit = max(1, min(limit, 12))
    now = datetime.now(timezone.utc).timestamp()
    cached = getattr(app.state, "veille_cache", None)
    if cached and now < cached.get("expires_at", 0):
        return cached["payload"]

    url = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
    try:
        response = requests.get(url, timeout=20, headers={"Accept": "application/json"})
        response.raise_for_status()
        data = response.json()
        vulnerabilities = data.get("vulnerabilities", []) if isinstance(data, dict) else []
        vulnerabilities = sorted(
            [v for v in vulnerabilities if isinstance(v, dict)],
            key=lambda v: (v.get("dateAdded") or "", v.get("cveID") or ""),
            reverse=True,
        )
        items = [
            {
                "cveID": vuln.get("cveID", ""),
                "vendorProject": vuln.get("vendorProject", ""),
                "product": vuln.get("product", ""),
                "vulnerabilityName": vuln.get("vulnerabilityName", ""),
                "dateAdded": vuln.get("dateAdded", ""),
                "shortDescription": vuln.get("shortDescription", ""),
                "requiredAction": vuln.get("requiredAction", ""),
                "dueDate": vuln.get("dueDate", ""),
            }
            for vuln in vulnerabilities[:limit]
        ]
        payload = {
            "catalogVersion": data.get("catalogVersion", ""),
            "dateReleased": data.get("dateReleased", ""),
            "count": data.get("count", len(vulnerabilities)),
            "sourceUrl": url,
            "items": items,
            "updatedAt": now,
            "stale": False,
        }
        app.state.veille_cache = {"payload": payload, "expires_at": now + 120}
        return payload
    except Exception as exc:
        logger.exception("Échec de récupération de la veille CISA: %s", exc)
        cached = getattr(app.state, "veille_cache", None)
        if cached:
            stale_payload = dict(cached["payload"])
            stale_payload["stale"] = True
            return stale_payload
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Impossible de récupérer la veille automatique pour le moment.") from exc


@app.get("/api/tags", response_model=list[TagRead])
def list_tags(type: ItemType | None = None, db: Session = Depends(get_db)) -> list[Tag]:
    query = select(Tag).order_by(Tag.type.asc(), Tag.name.asc())
    if type is not None:
        query = query.where(Tag.type == type)
    return list(db.scalars(query))


@app.post("/api/tags", response_model=TagRead, status_code=status.HTTP_201_CREATED)
def create_tag(
    payload: TagCreate,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_admin),
) -> Tag:
    tag = Tag(type=payload.type, name=payload.name.strip())
    db.add(tag)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ce tag existe déjà pour ce type.") from exc
    db.refresh(tag)
    return tag


@app.delete("/api/tags/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tag(
    tag_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_admin),
) -> Response:
    tag = db.get(Tag, tag_id)
    if tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag introuvable.")

    in_use = db.scalar(select(func.count()).select_from(Item).where(Item.type == tag.type, Item.category == tag.name))
    if in_use:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ce tag est utilisé par un élément.")

    db.delete(tag)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.post("/api/items", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
def create_item(
    payload: ItemCreate,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_admin),
) -> Item:
    data = payload.model_dump()
    if data["type"] != "realisation":
        data["featured"] = False
    elif data["featured"]:
        db.query(Item).filter(Item.type == "realisation", Item.featured.is_(True)).update({"featured": False})

    if data["display_order"] == 0:
        max_order = db.scalar(select(func.max(Item.display_order)).where(Item.type == data["type"])) or 0
        data["display_order"] = max_order + 10

    item = Item(**data)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@app.put("/api/items/{item_id}", response_model=ItemRead)
def update_item(
    item_id: int,
    payload: ItemUpdate,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_admin),
) -> Item:
    item = db.get(Item, item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Element introuvable.")

    data = payload.model_dump()
    if data["type"] != "realisation":
        data["featured"] = False
    elif data["featured"]:
        db.query(Item).filter(
            Item.id != item_id,
            Item.type == "realisation",
            Item.featured.is_(True),
        ).update({"featured": False})

    for key, value in data.items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item


@app.delete("/api/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_admin),
) -> Response:
    item = db.get(Item, item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Element introuvable.")

    db.delete(item)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get("/api/testimonials", response_model=list[TestimonialRead])
def list_testimonials(request: Request, db: Session = Depends(get_db)) -> list[Testimonial]:
    # If admin token is provided, return all testimonials. Otherwise, only visible ones.
    is_admin = False
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        try:
            from .auth import get_current_admin
            # Just test if the token is valid
            get_current_admin(token, get_settings())
            is_admin = True
        except Exception:
            pass

    query = select(Testimonial).order_by(Testimonial.created_at.desc())
    if not is_admin:
        query = query.where(Testimonial.is_visible == True)
        
    return list(db.scalars(query))


@app.post("/api/testimonials", response_model=TestimonialRead, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
def create_testimonial(request: Request, payload: TestimonialCreate, db: Session = Depends(get_db)) -> Testimonial:
    testimonial = Testimonial(**payload.model_dump())
    db.add(testimonial)
    db.commit()
    db.refresh(testimonial)
    return testimonial


@app.put("/api/testimonials/{testimonial_id}", response_model=TestimonialRead)
def update_testimonial_visibility(
    testimonial_id: int,
    payload: TestimonialUpdate,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_admin),
) -> Testimonial:
    testimonial = db.get(Testimonial, testimonial_id)
    if testimonial is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Témoignage introuvable.")

    testimonial.is_visible = payload.is_visible
    db.commit()
    db.refresh(testimonial)
    return testimonial


@app.delete("/api/testimonials/{testimonial_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_testimonial(
    testimonial_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_admin),
) -> Response:
    testimonial = db.get(Testimonial, testimonial_id)
    if testimonial is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Témoignage introuvable.")

    db.delete(testimonial)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.post("/api/contact", status_code=status.HTTP_202_ACCEPTED)
@limiter.limit("3/minute")
def send_contact_email(request: Request, payload: ContactRequest, settings: Settings = Depends(get_settings)) -> dict[str, str]:
    if not settings.smtp_user or not settings.smtp_password or not settings.smtp_recipient:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="L'envoi d'email n'est pas encore configuré (SMTP manquant).",
        )

    msg = EmailMessage()
    msg.set_content(
        "Nouveau message depuis votre portfolio\n\n"
        f"Nom / email: {payload.email}\n"
        f"Objet: {payload.subject or 'Sans objet'}\n\n"
        f"Message:\n{payload.message}"
    )
    msg['Subject'] = payload.subject if payload.subject else 'Nouveau message depuis votre portfolio'
    msg['From'] = settings.smtp_user
    msg['To'] = settings.smtp_recipient
    msg['Reply-To'] = payload.email

    def send_via_sendgrid():
        if not settings.sendgrid_api_key:
            return False, "no_sendgrid_key"

        url = "https://api.sendgrid.com/v3/mail/send"
        headers = {
            "Authorization": f"Bearer {settings.sendgrid_api_key}",
            "Content-Type": "application/json",
        }
        data = {
            "personalizations": [{"to": [{"email": settings.smtp_recipient}], "subject": msg['Subject']}],
            "from": {"email": settings.smtp_user},
            "reply_to": {"email": payload.email},
            "content": [{"type": "text/plain", "value": msg.get_content()}],
        }
        try:
            resp = requests.post(url, headers=headers, json=data, timeout=15)
            if resp.status_code in (200, 202):
                return True, None
            return False, f"sendgrid_status_{resp.status_code}: {resp.text}"
        except Exception as e:
            return False, str(e)

    try:
        if settings.smtp_port == 465:
            with smtplib.SMTP_SSL(settings.smtp_server, settings.smtp_port, timeout=30) as server:
                server.login(settings.smtp_user, settings.smtp_password)
                server.send_message(msg)
        else:
            with smtplib.SMTP(settings.smtp_server, settings.smtp_port, timeout=30) as server:
                if server.has_extn("STARTTLS"):
                    server.starttls()
                server.login(settings.smtp_user, settings.smtp_password)
                server.send_message(msg)
    except Exception as exc:
        logger.exception("Échec de l'envoi SMTP: %s", exc)
        try:
            tb = traceback.format_exc()
            print("[SMTP ERROR TRACEBACK]", tb, file=sys.stderr)
        except Exception:
            logger.exception("Erreur lors de l'écriture du traceback")

        # If network errors (outbound blocked) or other failures, try SendGrid fallback
        if settings.sendgrid_api_key:
            ok, info = send_via_sendgrid()
            if ok:
                return {"status": "accepted_via_sendgrid"}
            logger.error("SendGrid fallback failed: %s", info)

        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Impossible d'envoyer l'e-mail. Vérifiez la configuration SMTP et vos informations d'identification.",
        ) from exc

    return {"status": "accepted"}

# Create uploads directory if it doesn't exist
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.post("/api/upload", dependencies=[Depends(get_current_admin)])
async def upload_image(file: UploadFile = File(...)):
    allowed_mime_prefixes = ("image/",)
    allowed_exact_mimes = {"application/pdf"}
    filename = file.filename or "upload"
    content_type = (file.content_type or "").lower()
    if not content_type.startswith(allowed_mime_prefixes) and content_type not in allowed_exact_mimes:
        raise HTTPException(status_code=400, detail="Seules les images et les fichiers PDF sont autorisés.")

    ext = filename.split(".")[-1].lower() if "." in filename else "bin"
    if content_type == "application/pdf" or ext == "pdf":
        ext = "pdf"
    elif not content_type.startswith("image/"):
        ext = "bin"
    unique_filename = f"{uuid.uuid4().hex}.{ext}"
    file_path = os.path.join("uploads", unique_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"url": f"/uploads/{unique_filename}"}

# Trigger reload now

