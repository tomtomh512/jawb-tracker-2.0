from typing import Optional

from pydantic import BaseModel, ConfigDict
from datetime import date


class CertificationBase(BaseModel):
    name: str | None = None
    issuer: str | None = None
    issue_date: Optional[date] = None
    expiration_date: Optional[date] = None
    credential_id: str | None = None
    url: str | None = None


class CertificationCreate(CertificationBase):
    pass


class CertificationUpdate(CertificationBase):
    pass


class CertificationResponse(CertificationBase):
    id: int

    model_config = ConfigDict(from_attributes=True)