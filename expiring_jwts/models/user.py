from sqlalchemy import Column, Integer, String,TIMESTAMP
from datetime import datetime
from expiring_jwts.models import Base
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)
    modified_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)