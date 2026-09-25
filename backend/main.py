from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import engine, get_db
from models import Base
from schemas import MessageCreate, MessageResponse
import crud


# Создаём таблицы в БД при старте приложения (если их ещё нет)
Base.metadata.create_all(bind=engine)


# Инициализируем FastAPI
app = FastAPI(title="Guestbook API", version="1.0.0")


# --- Эндпоинты ---

@app.get("/", tags=["Root"])
def root():
    """Простой эндпоинт для проверки, что бэкенд жив."""
    return {"message": "Guestbook API работает"}


@app.post("/messages", response_model=MessageResponse, status_code=status.HTTP_201_CREATED, tags=["Messages"])
def create_message(data: MessageCreate, db: Session = Depends(get_db)):
    """Создать новое сообщение в гостевой книге."""
    return crud.create_message(db, data)


@app.get("/messages", response_model=List[MessageResponse], tags=["Messages"])
def get_messages(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Получить список всех сообщений (сначала новые)."""
    return crud.get_messages(db, skip=skip, limit=limit)


@app.get("/messages/{message_id}", response_model=MessageResponse, tags=["Messages"])
def get_message(message_id: int, db: Session = Depends(get_db)):
    """Получить одно сообщение по id."""
    message = crud.get_message(db, message_id)
    if message is None:
        raise HTTPException(status_code=404, detail="Сообщение не найдено")
    return message


@app.delete("/messages/{message_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Messages"])
def delete_message(message_id: int, db: Session = Depends(get_db)):
    """Удалить сообщение по id."""
    success = crud.delete_message(db, message_id)
    if not success:
        raise HTTPException(status_code=404, detail="Сообщение не найдено")
    return None
