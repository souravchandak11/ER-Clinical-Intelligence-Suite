from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Session, create_engine
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres_password@db:5432/clinical_suite")
engine = create_engine(DATABASE_URL)

class AuditLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    user_id: str
    action: str  # e.g., "READ_PATIENT", "MODEL_INFERENCE", "LOGIN"
    resource_id: Optional[str] = None
    ip_address: Optional[str] = None
    details: Optional[str] = None

def log_audit_event(user_id: str, action: str, resource_id: Optional[str] = None, ip_address: Optional[str] = None, details: Optional[str] = None):
    try:
        with Session(engine) as session:
            log_entry = AuditLog(
                user_id=user_id,
                action=action,
                resource_id=resource_id,
                ip_address=ip_address,
                details=details
            )
            session.add(log_entry)
            session.commit()
    except Exception as e:
        # Fallback for local testing without DB
        print(f"[AUDIT LOG FAILURE] Action: {action}, Details: {e}")
