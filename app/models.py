import datetime
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid
from app.database import Base


class VerificationRequest(Base):
    __tablename__ = "verification_requests"

    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    phone_number = sa.Column(sa.String, index=True, nullable=False)
    request_id = sa.Column(sa.String, unique=True, index=True, nullable=True)
    status = sa.Column(sa.String, default="pending", index=True)
    created_at = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)
    expires_at = sa.Column(sa.DateTime, nullable=True)
    payload = sa.Column(sa.Text, nullable=True)
    raw_response = sa.Column(JSONB, nullable=True)


