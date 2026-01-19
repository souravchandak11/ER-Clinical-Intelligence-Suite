import os
from typing import Optional
from sqlmodel import SQLModel, create_engine, Session, Field
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres_password@db:5432/clinical_suite")
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", Fernet.generate_key().decode())

engine = create_engine(DATABASE_URL)
cipher_suite = Fernet(ENCRYPTION_KEY.encode())

def encrypt_data(data: str) -> str:
    if not data:
        return data
    return cipher_suite.encrypt(data.encode()).decode()

def decrypt_data(data: str) -> str:
    if not data:
        return data
    return cipher_suite.decrypt(data.encode()).decode()

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

# Example of an Encrypted Model
class PatientData(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name_encrypted: str
    dob_encrypted: str
    ssn_encrypted: str
    medical_history_encrypted: str

    @property
    def name(self):
        return decrypt_data(self.name_encrypted)
    
    @name.setter
    def name(self, value):
        self.name_encrypted = encrypt_data(value)

    # Similar properties would be added for other fields
