from pydantic import BaseModel, field_validator
import re


class UserCreate(BaseModel):
    login: str
    password: str

    @field_validator("login")
    @classmethod
    def validate_login(cls, v: str) -> str:
        if not (3 <= len(v) <= 32):
            raise ValueError("Логин: длина 3–32")
        if not re.match(r"^[a-zA-Z0-9._-]+$", v):
            raise ValueError("Логин: только латиница/цифры/._-")
        return v


class Message(BaseModel):
    message: str
