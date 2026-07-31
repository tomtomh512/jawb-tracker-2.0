from uuid import uuid4

from database import Base
from sqlalchemy import Column, String, Boolean, UUID


class Note(Base):
    __tablename__ = "Notes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)

    content = Column(String)
    is_linked = Column(Boolean, default=False)
    copy_to_clipboard = Column(Boolean, default=False)