import re
import hashlib

def deidentify_text(text: str) -> str:
    """
    Simple de-identification tool to remove potential PII/PHI.
    In a real HIPAA-compliant system, this would use a more robust NER model.
    """
    # Remove potential names (simplified), dates, and IDs
    # This is a placeholder for a more complex HIPAA-compliant de-id process
    
    # Hide dates
    text = re.sub(r'\d{2}/\d{2}/\d{4}', '[DATE]', text)
    # Hide SSN-like patterns
    text = re.sub(r'\d{3}-\d{2}-\d{4}', '[SSN]', text)
    # Hide email addresses
    text = re.sub(r'\S+@\S+', '[EMAIL]', text)
    
    return text

def secure_hash(patient_id: str) -> str:
    """
    Hashes patient ID for secure, anonymous tracking.
    """
    return hashlib.sha256(patient_id.encode()).hexdigest()
