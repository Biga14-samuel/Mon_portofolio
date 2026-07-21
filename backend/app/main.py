from fastapi import Depends, FastAPI, HTTPException, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.orm import Session

from .auth import (
    check_rate_limit,
    clear_failed_attempts,
    create_access_token,
    get_current_admin,
    register_failed_attempt,
    verify_password,
)
from .config import Settings, get_settings
from .database import get_db
from .models import ITEM_TYPES, Item
from .schemas import ItemCreate, ItemRead, ItemType, ItemUpdate, LoginRequest, TokenResponse

app = FastAPI(title="Portfolio API", version="1.0.0")
settings = get_settings()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)


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
    query = select(Item).order_by(Item.created_at.desc(), Item.id.desc())
    if type is not None:
        query = query.where(Item.type == type)
    return list(db.scalars(query))


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
