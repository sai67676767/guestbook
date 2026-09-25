from sqlalchemy.orm import Session
from models import Message
from schemas import MessageCreate


def create_message(db: Session, data: MessageCreate) -> Message:
    """Создаёт новое сообщение в БД."""
    message = Message(name=data.name, text=data.text)
    db.add(message)
    db.commit()
    db.refresh(message)  # Чтобы получить id и created_at, сгенерированные БД
    return message


def get_messages(db: Session, skip: int = 0, limit: int = 100):
    """Возвращает список сообщений, отсортированных по дате (сначала новые)."""
    return (
        db.query(Message)
        .order_by(Message.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_message(db: Session, message_id: int):
    """Возвращает одно сообщение по id или None, если не найдено."""
    return db.query(Message).filter(Message.id == message_id).first()


def delete_message(db: Session, message_id: int) -> bool:
    """Удаляет сообщение по id. Возвращает True, если удалось."""
    message = get_message(db, message_id)
    if message is None:
        return False
    db.delete(message)
    db.commit()
    return True
