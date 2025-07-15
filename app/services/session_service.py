from datetime import datetime, timezone

from sqlalchemy.orm import Session

from config.models import User
from dependencies.auth import create_access_token
from utils.password_utils import verify_password
from schemas.session_schema import UserSigninParams
from exceptions.custom_errors import UnauthorizedException


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email, User.deleted_at.is_(None)).first()


def signin_user(db: Session, params: UserSigninParams) -> tuple[User, str]:
    user = get_user_by_email(db, params.email)
    if not user:
        raise UnauthorizedException("Invalid username or password")
    if not user.is_email_verified:
        UnauthorizedException("Please accept invitation in your email")

    if not verify_password(params.password, user.encrypted_password):
        raise UnauthorizedException("Incorrect username or password")

    access_token = create_access_token(
        data={"email": user.email, "timestamp": str(datetime.now(timezone.utc))}
    )

    user.access_token = access_token
    user.is_currently_logged_in = True
    user.last_sign_in_at = user.current_sign_in_at
    user.current_sign_in_at = datetime.now(timezone.utc)
    user.last_sign_in_ip = user.current_sign_in_ip
    user.current_sign_in_ip = params.ip_address
    user.sign_in_count += 1
    db.commit()

    return user, access_token
