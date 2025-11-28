from datetime import datetime, timezone

from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base, DeclarativeBase


Model: DeclarativeBase = declarative_base()


class BaseModel(Model):
    __abstract__ = True
    __schema_name__: str = None

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        server_default=func.now()
    )
    updated_at = Column(
        DateTime,
        nullable=True
    )

    def __str__(self):
        return f"<{self.__class__.__name__}>(created_at={self.created_at})"
