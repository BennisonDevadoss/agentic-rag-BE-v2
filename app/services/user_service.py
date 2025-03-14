from sqlalchemy.orm import Session

from config.models import User
from exceptions.custom_errors import NotFoundException


def get_user_by_email(email: str, db: Session) -> User:
    user = db.query(User).filter(User.email == email, User.deleted_at.is_(None)).first()
    if not user:
        raise NotFoundException("User not found")
    return user
