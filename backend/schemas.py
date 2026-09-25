from pydantic import BaseModel, Field
from datetime import datetime


# Схема для создания нового сообщения (то, что присылает клиент)
class MessageCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Имя автора")
    text: str = Field(..., min_length=1, description="Текст сообщения")


# Схема для ответа (то, что отдаёт сервер)
class MessageResponse(BaseModel):
    id: int
    name: str
    text: str
    created_at: datetime

    # Это позволяет Pydantic читать данные из объектов SQLAlchemy (у которых поля — это атрибуты, а не dict)
    class Config:
        from_attributes = True
