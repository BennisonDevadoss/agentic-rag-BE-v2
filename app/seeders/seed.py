import os
import sys

# Example directory path
directory_path = os.getcwd()

# Get the parent directory
parent_directory = os.path.dirname(directory_path)

sys.path.append(directory_path)
sys.path.append(parent_directory)

from sqlalchemy import func
from sqlalchemy.orm import Session

from role_data import ROLES
from user_data import USERS
from config.models import Role, User
from utils.password_utils import get_password_hash
from config.database import SessionLocal


def seed_roles(roles: list[Role], db: Session) -> None:
    for role in roles:
        # Check if the role with the same name already exists in the database
        existing_record = db.query(Role).filter(Role.name == role.name).first()

        if existing_record:
            existing_record.name = role.name
            existing_record.updated_at = func.now()
        else:
            db.add(role)

    db.commit()


def seed_users(users: list[User], db: Session) -> None:
    for user in users:
        # Hash password before inserting or updating user
        user.encrypted_password = get_password_hash("Test@123")

        # Check if the user with the same email already exists in the database
        existing_record = db.query(User).filter(User.email == user.email).first()

        if existing_record:
            existing_record.first_name = user.first_name
            existing_record.last_name = user.last_name
            existing_record.role_id = user.role_id
            existing_record.is_email_verified = user.is_email_verified
            existing_record.encrypted_password = user.encrypted_password
            existing_record.updated_at = func.now()
        else:
            db.add(user)

    db.commit()


def seed() -> None:
    with SessionLocal() as db:
        seed_roles(ROLES, db)
        seed_users(USERS, db)


if __name__ == "__main__":
    seed()
