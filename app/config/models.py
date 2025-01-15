from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import relationship

from .database import Base


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)

    # Use `default` to set the value in Python before insert,
    # `server_default` lets the DB set it during insert.
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    users = relationship("User", back_populates="role")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    first_name = Column(String(75), nullable=False)
    last_name = Column(String(75), nullable=True)
    email = Column(String(100), nullable=False)
    mobile_no = Column(String(15), nullable=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)

    otp = Column(String(4), nullable=True)
    otp_secret_key = Column(String(32), nullable=True)
    is_otp_verified = Column(Boolean, default=False)
    otp_count = Column(Integer, default=0)
    resent_otp_count = Column(Integer, default=0)
    last_otp_sent_at = Column(DateTime, nullable=True)
    last_verified_at = Column(DateTime, nullable=True)
    is_reset_resent_otp_count = Column(Boolean, nullable=True)

    encrypted_password = Column(Text, nullable=True)
    access_token = Column(Text, nullable=True)

    sign_in_count = Column(Integer, default=0)
    current_sign_in_ip = Column(String(50), nullable=True)
    last_sign_in_ip = Column(String(50), nullable=True)
    current_sign_in_at = Column(DateTime, nullable=True)
    last_sign_in_at = Column(DateTime, nullable=True)

    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    updated_by = Column(Integer, ForeignKey("users.id"), nullable=True)

    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, server_default=func.now(), server_onupdate=func.now(), nullable=False
    )
    deleted_at = Column(DateTime, nullable=True)

    # Relationships
    role = relationship("Role", back_populates="users")
