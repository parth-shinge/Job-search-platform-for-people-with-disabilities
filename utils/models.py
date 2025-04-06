from dotenv import load_dotenv
import os
from sqlalchemy import (
    create_engine, Column, Integer, String, Boolean,
    ForeignKey, Text, DateTime, text, LargeBinary, ARRAY
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import logging
from sqlalchemy.pool import QueuePool
from sqlalchemy import Column, Integer, String, Boolean, Text, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create base class for declarative models
Base = declarative_base()

# Create engine with DATABASE_URL
database_url = os.getenv('DATABASE_URL')
if not database_url:
    raise ValueError("DATABASE_URL environment variable is not set")

try:
    engine = create_engine(
        database_url,
        pool_size=5,
        max_overflow=10,
        pool_timeout=30,
        pool_recycle=1800,
        pool_pre_ping=True,
        poolclass=QueuePool
    )
    logger.info("Database engine created successfully")
except Exception as e:
    logger.error(f"Error creating database engine: {str(e)}")
    raise

Session = sessionmaker(bind=engine)




class Company(Base):
    __tablename__ = 'companies'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    website = Column(String, nullable=False)
    contact_name = Column(String, nullable=False)
    contact_email = Column(String, nullable=False, unique=True)
    contact_position = Column(String, nullable=False)
    contact_phone = Column(String, nullable=False)
    commitments = Column(ARRAY(String), nullable=True)
    documentation = Column(ARRAY(String), nullable=True)
    additional_info = Column(Text, nullable=True)
    password = Column(String, nullable=False)
    verified = Column(Boolean, default=False)
    verification_status = Column(String, nullable=False)
    jobs = relationship("Job", back_populates="company")

class Job(Base):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    company_id = Column(Integer, ForeignKey('companies.id'))
    location = Column(String(100))
    job_type = Column(String(50))
    accommodations = Column(Text)  # Store as JSON string
    description = Column(Text)
    posted_date = Column(DateTime, default=datetime.utcnow)
    company = relationship("Company", back_populates="jobs")
    applications = relationship("JobApplication", back_populates="job")
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    name = Column(String(100))
    password = Column(String(255), nullable=False)
    resume_data = Column(Text)  # JSON string containing all profile data
    created_at = Column(DateTime, default=datetime.utcnow)
    applications = relationship("JobApplication", back_populates="user")

class JobApplication(Base):
    __tablename__ = 'job_applications'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    job_id = Column(Integer, ForeignKey('jobs.id'))
    status = Column(String(50), default='applied')
    applied_date = Column(DateTime, default=datetime.utcnow)
    resume = Column(LargeBinary)  # Field to store the resume file content
    cover_letter = Column(Text)  # Field to store the cover letter
    additional_notes = Column(Text)  # Field to store additional notes
    user = relationship("User", back_populates="applications")
    job = relationship("Job", back_populates="applications")

def init_db():
    """Initialize database tables"""
    try:
        Base.metadata.create_all(engine)  # Create missing tables
        logger.info("Database tables created successfully")

        # Verify connection
        with Session() as session:
            session.execute(text("SELECT 1"))
            logger.info("Database connection verified successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        raise

# Run only if executed directly (prevents auto-execution on imports)
if __name__ == "__main__":
    init_db()