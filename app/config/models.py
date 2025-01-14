from sqlalchemy import Column, DateTime, Integer, String, func

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
