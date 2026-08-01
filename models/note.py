from uuid import uuid4

from database import Base
from sqlalchemy import Column, String, Boolean, UUID, DateTime, func


class Note(Base):
    __tablename__ = "Notes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)

    title = Column(String, nullable=True)
    content = Column(String, nullable=False)
    copy_to_clipboard = Column(Boolean, default=False)

    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())