# checkout_shield/database.py
from sqlalchemy import create_engine, Column, String, Float, Boolean, Integer
from sqlalchemy.orm import declarative_base, sessionmaker
from checkout_shield.config import settings

engine = create_engine(settings.database_url, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class AssessmentRecord(Base):
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String, unique=True, index=True)
    user_email = Column(String, index=True)
    amount = Column(Float)
    is_approved = Column(Boolean)
    risk_level = Column(String)
    risk_score = Column(Integer)

# Create tables
Base.metadata.create_all(bind=engine)

# Dependency to inject DB session into routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()