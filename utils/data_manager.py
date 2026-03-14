from sqlalchemy.orm import joinedload
from .models import Company, Job, User, JobApplication, Session
import json
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

def get_db_session():
    """Get database session"""
    return Session()


def _safe_json_loads(value, default):
    """Safely parse JSON text values stored in the database."""
    if value is None:
        return default
    if isinstance(value, (dict, list)):
        return value
    try:
        return json.loads(value)
    except (TypeError, json.JSONDecodeError):
        return default

def load_jobs():
    """Load jobs from database with eager loading for related company"""
    session = get_db_session()
    try:
        jobs = session.query(Job).options(joinedload(Job.company)).all()
        return jobs
    except Exception as e:
        print(f"Error loading jobs: {str(e)}")
        raise
    finally:
        session.close()

def load_companies():
    """Load companies from database"""
    try:
        session = get_db_session()
        companies = session.query(Company).all()
        return companies
    except Exception as e:
        print(f"Error loading companies: {str(e)}")
        raise
    finally:
        session.close()

def save_company_verification(verification_data):
    session = get_db_session()
    try:
        company = Company(
            name=verification_data['company_name'],
            website=verification_data['company_website'],
            contact_name=verification_data['contact_name'],
            contact_email=verification_data['contact_email'],
            contact_position=verification_data['contact_position'],
            contact_phone=verification_data['contact_phone'],
            commitments=verification_data['commitments'],
            documentation=verification_data['documentation'],
            additional_info=verification_data['additional_info'],
            password=verification_data['password'],
            verified=False,
            verification_status='pending'
        )
        session.add(company)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def get_company_by_email(email):
    """Get company by email"""
    session = get_db_session()
    try:
        company = session.query(Company).filter_by(contact_email=email).first()
        return company
    except Exception as e:
        print(f"Error fetching company by email: {str(e)}")
        return None
    finally:
        session.close()

def check_password(stored_password, provided_password):
    """Check if the provided password matches the stored password"""
    return check_password_hash(stored_password, provided_password)

def get_company_profile(company_id):
    """Get company profile data"""
    session = get_db_session()
    try:
        company = session.query(Company).filter_by(id=company_id).first()
        return company
    except Exception as e:
        print(f"Error fetching company profile: {str(e)}")
        return None
    finally:
        session.close()

def update_company_profile(company_id, profile_data):
    """Update company profile"""
    session = get_db_session()
    try:
        company = session.query(Company).filter_by(id=company_id).first()
        if company:
            company.website = profile_data['website']
            company.description = profile_data['description']
            company.accessibility_features = profile_data['accessibility_features']
            company.culture = profile_data['culture']
            session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def get_company_jobs(company_id):
    """Get jobs posted by a company"""
    session = get_db_session()
    try:
        jobs = session.query(Job).filter_by(company_id=company_id).all()
        for job in jobs:
            job.accommodations = _safe_json_loads(job.accommodations, [])
        return jobs
    except Exception as e:
        print(f"Error fetching company jobs: {str(e)}")
        return []
    finally:
        session.close()

def get_applications_for_company(company_id):
    """Get job applications for a company in a UI-friendly format."""
    session = get_db_session()
    try:
        applications = session.query(JobApplication).options(
            joinedload(JobApplication.user),
            joinedload(JobApplication.job).joinedload(Job.company)
        ).filter(JobApplication.job.has(company_id=company_id)).all()

        results = []
        for app in applications:
            resume_payload = _safe_json_loads(app.user.resume_data if app.user else None, {})
            user_name = app.user.name if app.user and app.user.name else "Unknown"
            user_email = app.user.email if app.user else ""
            job_title = app.job.title if app.job else "Unknown Role"

            results.append({
                "application_id": app.id,
                "job_id": app.job_id,
                "job_title": job_title,
                "user_name": user_name,
                "user_email": user_email,
                "user_resume": resume_payload,
                "status": app.status,
                "applied_date": app.applied_date,
            })

        return results
    except Exception as e:
        print(f"Error fetching applications for company: {str(e)}")
        return []
    finally:
        session.close()

def post_new_job(job_data, company_id=None):
    """Post a new job for a company."""
    session = get_db_session()
    try:
        resolved_company_id = company_id if company_id is not None else job_data.get('company_id')
        if resolved_company_id is None:
            raise ValueError("company_id is required to post a job")

        job = Job(
            company_id=resolved_company_id,
            title=job_data['title'],
            location=job_data['location'],
            job_type=job_data['job_type'],
            accommodations=json.dumps(job_data.get('accommodations', [])),
            description=job_data.get('description', ''),
            requirements=job_data.get('requirements', ''),
            posted_date=datetime.utcnow()
        )
        session.add(job)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error posting new job: {str(e)}")
        raise
    finally:
        session.close()

def send_email_to_applicant(application_id, email_data):
    """Placeholder notification flow that also updates application status."""
    session = get_db_session()
    try:
        application = session.query(JobApplication).filter_by(id=application_id).first()
        if not application:
            return False

        if isinstance(email_data, dict) and email_data.get("status"):
            application.status = email_data["status"]
            session.commit()

        return True
    except Exception as e:
        session.rollback()
        print(f"Error sending email: {str(e)}")
        return False
    finally:
        session.close()

def get_user_profile(email, password):
    """Get user profile by email and verify password"""
    session = get_db_session()
    try:
        user = session.query(User).filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            return json.loads(user.resume_data)
        return None
    except Exception as e:
        print(f"Error fetching user profile: {str(e)}")
        return None
    finally:
        session.close()

def get_user_profile_by_email(email):
    """Get user profile by email without verifying password"""
    session = get_db_session()
    try:
        user = session.query(User).filter_by(email=email).first()
        if user:
            return json.loads(user.resume_data)
        return None
    except Exception as e:
        print(f"Error fetching user profile: {str(e)}")
        return None
    finally:
        session.close()

def create_user_if_not_exists(username, email, password, profile_data):
    session = get_db_session()
    try:
        user = session.query(User).filter_by(email=email).first()
        if user:
            return False
        hashed_password = generate_password_hash(password)
        new_user = User(
            username=username,
            email=email,
            name=f"{profile_data.get('first_name', '')} {profile_data.get('last_name', '')}".strip(),
            password=hashed_password,
            resume_data=json.dumps(profile_data),
            created_at=datetime.utcnow()
        )
        session.add(new_user)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def update_user_profile(email, profile_data):
    """Update user profile"""
    session = get_db_session()
    try:
        user = session.query(User).filter_by(email=email).first()
        if user:
            user.name = f"{profile_data['first_name']} {profile_data['last_name']}"
            user.resume_data = json.dumps(profile_data)
            session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def save_job_application(application_data, job_id):
    """Save job application"""
    session = get_db_session()
    try:
        # Create or update user
        user = session.query(User).filter_by(email=application_data['email']).first()
        if not user:
            raise ValueError("User account not found. Please register and log in before applying.")

        # Create application
        application = JobApplication(
            user_id=user.id,
            job_id=job_id,
            status='applied',
            applied_date=datetime.utcnow(),
            resume=application_data.get('resume'),  # Save the resume file content
            cover_letter=application_data.get('cover_letter'),  # Save the cover letter
            additional_notes=application_data.get('additional_notes')  # Save additional notes
        )

        session.add(application)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def get_job_applications(user_email):
    """Get job applications for a user"""
    session = get_db_session()
    try:
        user = session.query(User).filter_by(email=user_email).first()
        if user:
            applications = session.query(JobApplication).options(
                joinedload(JobApplication.job).joinedload(Job.company)
            ).filter_by(user_id=user.id).all()
            return applications
        return []
    except Exception as e:
        print(f"Error loading job applications: {str(e)}")
        raise
    finally:
        session.close()
