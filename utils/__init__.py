# Make utils directory a Python package
from .models import Job, Company, User, JobApplication, Session, engine
from .data_manager import (
    load_jobs,
    load_companies,
    save_company_verification,
    get_user_profile,
    update_user_profile,
    get_company_profile,
    update_company_profile,
    get_company_jobs,
    save_job_application,
    get_job_applications,
    get_applications_for_company,
    send_email_to_applicant,
    save_job_application

)
