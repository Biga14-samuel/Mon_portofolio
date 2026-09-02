import smtplib
from email.message import EmailMessage
from fastapi import (
    Depends, FastAPI, HTTPException, Request, Response, status,
    UploadFile, File,
)
import logging
import requests

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
from .models import Item, Tag, Testimonial

Base.metadata.create_all(bind=engine)
try:
    with engine.begin() as conn:
        conn.exec_driver_sql("ALTER TYPE item_type ADD VALUE IF NOT EXISTS 'blog'")
except Exception as exc:
    logger.debug("Type item_type 'blog' déjà existant ou non supporté: %s", exc)

from .schemas import (
    ContactRequest,
    ItemCreate,
    ItemRead,
    ItemType,
    ItemUpdate,
    LoginRequest,
    TagCreate,
    TagRead,
    TestimonialCreate,
    TestimonialRead,
    TestimonialUpdate,
    TokenResponse,
)

app = FastAPI(title="Portfolio API", version="1.0.0")
settings = get_settings()

# Setup Rate Limiter
limiter = Limiter(key_func=get_client_ip)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_origin_regex=r"^https://[a-zA-Z0-9-]+\.vercel\.app$",
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


import secrets as _secrets


@app.post("/api/login", response_model=TokenResponse)
def login(
    request: Request,
    payload: LoginRequest,
    settings: Settings = Depends(get_settings),
) -> TokenResponse:
    check_rate_limit(request)
    valid_username = _secrets.compare_digest(
        payload.username, settings.admin_username
    )
    valid_password = verify_password(payload.password, settings.admin_password_hash)
    if not valid_username or not valid_password:
        register_failed_attempt(request)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants invalides.",
        )

    clear_failed_attempts(request)
    return TokenResponse(
        access_token=create_access_token(settings.admin_username, settings)
    )


@app.get("/api/items", response_model=list[ItemRead])
def list_items(type: ItemType | None = None, db: Session = Depends(get_db)) -> list[Item]:
    query = select(Item).order_by(Item.display_order.asc(), Item.created_at.desc(), Item.id.desc())
    if type is not None:
        query = query.where(Item.type == type)
    return list(db.scalars(query))

from .veille import get_veille_payload


@app.get("/api/veille")
def get_veille(limit: int = 8) -> dict[str, object]:
    return get_veille_payload(app.state, limit)


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


def _is_admin_request(request: Request) -> bool:
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return False
    token = auth_header.split(" ", 1)[1].strip()
    try:
        from jose import jwt
        app_settings = get_settings()
        payload = jwt.decode(token, app_settings.jwt_secret, algorithms=["HS256"])
        username = payload.get("sub")
        return bool(username and _secrets.compare_digest(username, app_settings.admin_username))
    except Exception:
        return False


@app.get("/api/testimonials", response_model=list[TestimonialRead])
def list_testimonials(request: Request, db: Session = Depends(get_db)) -> list[Testimonial]:
    # If admin token is provided, return all testimonials (including non-visible ones for moderation).
    query = select(Testimonial).order_by(Testimonial.created_at.desc())
    if not _is_admin_request(request):
        query = query.where(Testimonial.is_visible.is_(True))
        
    return list(db.scalars(query))


@app.post("/api/testimonials", response_model=TestimonialRead, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
def create_testimonial(
    request: Request, payload: TestimonialCreate, db: Session = Depends(get_db)
) -> Testimonial:
    _ = request.client  # Explicitly reference request for linter while satisfying slowapi
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


def _build_contact_email(payload: ContactRequest, settings: Settings) -> EmailMessage:
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
    return msg


def _send_via_sendgrid(
    msg: EmailMessage,
    payload: ContactRequest,
    settings: Settings,
) -> tuple[bool, str | None]:
    if not settings.sendgrid_api_key:
        return False, "no_sendgrid_key"
    url = "https://api.sendgrid.com/v3/mail/send"
    headers = {
        "Authorization": f"Bearer {settings.sendgrid_api_key}",
        "Content-Type": "application/json",
    }
    data = {
        "personalizations": [
            {"to": [{"email": settings.smtp_recipient}], "subject": msg['Subject']}
        ],
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


def _send_via_smtp(msg: EmailMessage, settings: Settings) -> None:
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


@app.post("/api/contact", status_code=status.HTTP_202_ACCEPTED)
@limiter.limit("3/minute")
def send_contact_email(
    request: Request,
    payload: ContactRequest,
    settings: Settings = Depends(get_settings),
) -> dict[str, str]:
    _ = request.client  # Explicitly reference request for linter while satisfying slowapi
    if not settings.smtp_user or not settings.smtp_password or not settings.smtp_recipient:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="L'envoi d'email n'est pas encore configuré (SMTP manquant).",
        )

    msg = _build_contact_email(payload, settings)

    try:
        _send_via_smtp(msg, settings)
    except Exception as exc:
        logger.exception("Échec de l'envoi SMTP: %s", exc)
        if settings.sendgrid_api_key:
            ok, info = _send_via_sendgrid(msg, payload, settings)
            if ok:
                return {"status": "accepted_via_sendgrid"}
            logger.error("SendGrid fallback failed: %s", info)

        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=(
                "Impossible d'envoyer l'e-mail. "
                "Vérifiez la configuration SMTP et vos identifiants."
            ),
        ) from exc

    return {"status": "accepted"}

# Create uploads directory if it doesn't exist
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

def _upload_to_supabase(
    file_bytes: bytes,
    unique_filename: str,
    content_type: str,
    settings: Settings,
) -> str:
    raw_url = (settings.supabase_url or "").strip().rstrip("/")
    if "/rest" in raw_url:
        raw_url = raw_url.split("/rest")[0].rstrip("/")
    supabase_url = raw_url
    bucket = (settings.supabase_bucket or "portfolio-uploads").strip().strip("/")
    upload_endpoint = f"{supabase_url}/storage/v1/object/{bucket}/{unique_filename}"
    headers = {
        "Authorization": f"Bearer {settings.supabase_key.strip()}",
        "apikey": settings.supabase_key.strip(),
        "Content-Type": content_type,
    }
    resp = requests.post(upload_endpoint, data=file_bytes, headers=headers, timeout=20)
    if resp.status_code in (200, 201):
        public_url = f"{supabase_url}/storage/v1/object/public/{bucket}/{unique_filename}"
        logger.info("Fichier uploadé avec succès sur Supabase Storage: %s", public_url)
        return public_url

    logger.error("Erreur Supabase Storage (%s): %s", resp.status_code, resp.text)
    raise HTTPException(status_code=500, detail=f"Erreur d'upload Supabase: {resp.text}")


@app.post("/api/upload", dependencies=[Depends(get_current_admin)])
async def upload_image(file: UploadFile = File(...), settings: Settings = Depends(get_settings)):
    ALLOWED_EXTENSIONS = {
        "image/jpeg": "jpg",
        "image/jpg": "jpg",
        "image/png": "png",
        "image/gif": "gif",
        "image/webp": "webp",
        "application/pdf": "pdf",
    }
    content_type = (file.content_type or "").lower()
    if content_type not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Type de fichier non autorisé. Seules les images (JPEG, PNG, GIF, WEBP) et PDF sont acceptés.",
        )

    ext = ALLOWED_EXTENSIONS[content_type]
    unique_filename = f"{uuid.uuid4().hex}.{ext}"

    if settings.supabase_url and settings.supabase_key:
        file_bytes = await file.read()
        public_url = _upload_to_supabase(file_bytes, unique_filename, content_type, settings)
        return {"url": public_url}

    # Fallback disque local
    file_path = os.path.join("uploads", unique_filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"url": f"/uploads/{unique_filename}"}

