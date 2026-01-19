import re
from typing import List

# Simple PII regex patterns for demonstration
# In production, use specialized libraries like Presidio or scrubadub
PII_PATTERNS = [
    (r'\b\d{3}-\d{2}-\d{4}\b', "[SSN]"),  # SSN
    (r'\b\d{10}\b', "[PHONE]"),           # Phone (simple)
    (r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', "[EMAIL]"), # Email
    (r'\b\d{1,5}\s\w.\s(\b\w*\b\s){1,2}\w*\.\b', "[ADDRESS]") # Address (very simple)
]

def deidentify_text(text: str) -> str:
    """
    Scrubs PII from the input text before sending it to a model.
    """
    scrubbed_text = text
    for pattern, placeholder in PII_PATTERNS:
        scrubbed_text = re.sub(pattern, placeholder, scrubbed_text)
    return scrubbed_text

def apply_retention_policy(older_than_days: int = 30):
    """
    Stub for background task to delete old data according to hospital policy.
    """
    # In a real implementation, this would query the DB and delete old records
    print(f"Applying data retention policy: Scrambling/Deleting data older than {older_than_days} days.")
    pass

def flag_sensitive_content(text: str) -> List[str]:
    """
    Returns a list of detected sensitive data types.
    """
    found = []
    if re.search(r'\b\d{3}-\d{2}-\d{4}\b', text):
        found.append("SSN")
    # ... more flags
    return found
