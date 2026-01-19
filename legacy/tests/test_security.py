import pytest
from backend.app.core.database import encrypt_data, decrypt_data
from backend.app.services.privacy import deidentify_text

def test_encryption_decryption():
    original_text = "Sensitive Patient Note"
    encrypted = encrypt_data(original_text)
    assert encrypted != original_text
    decrypted = decrypt_data(encrypted)
    assert decrypted == original_text

def test_deidentification():
    text_with_pii = "Patient John Doe (SSN: 123-45-6789) can be reached at john.doe@email.com"
    scrubbed = deidentify_text(text_with_pii)
    assert "john.doe@email.com" not in scrubbed
    assert "123-45-6789" not in scrubbed
    assert "[SSN]" in scrubbed
    assert "[EMAIL]" in scrubbed

def test_audit_logging_integrity():
    # This would typically involve mocking the DB and checking if log_audit_event was called
    # For now, we verify the service exists and can be imported
    from backend.app.services.audit import log_audit_event
    assert callable(log_audit_event)

def test_secure_auth_stub():
    from backend.app.core.auth import create_access_token
    token = create_access_token({"sub": "doctor123"})
    assert isinstance(token, str)
    assert len(token) > 0
