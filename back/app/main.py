from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import logging
import re

from .db import get_db, engine
from .models import Base, User
from .schemas import UserCreate, Message
from .security import hash_password
from fastapi.middleware.cors import CORSMiddleware


logger = logging.getLogger("app")
logging.basicConfig(level=logging.INFO)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="MVP Registration")

origins = [
    "http://localhost:5173",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def validate_password_strength(password: str) -> None:
    if len(password) < 8:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Пароль: минимум 8 символов",
        )
    if not re.search(r"[a-z]", password):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Пароль должен содержать строчную букву",
        )
    if not re.search(r"[A-Z]", password):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Пароль должен содержать заглавную букву",
        )
    if not re.search(r"\d", password):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Пароль должен содержать цифру",
        )
    if not re.search(r"[^\w\s]", password):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Пароль должен содержать спецсимвол",
        )


@app.post("/api/register", response_model=Message)
def register_user(payload: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.login == payload.login).first()
    if existing:
        logger.warning("User registration conflict login=%s", payload.login)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Логин уже занят",
        )

    validate_password_strength(payload.password)

    user = User(
        login=payload.login,
        password_hash=hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    logger.info("User registered id=%s login=%s", user.id, user.login)
    return {"message": "user создан"}
