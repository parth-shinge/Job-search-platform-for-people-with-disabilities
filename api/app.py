from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
from flask_caching import Cache
import sys
import os
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from utils.models import Job, Company, User, JobApplication, Session
    logger.info("Successfully imported database models")
except Exception as e:
    logger.error(f"Failed to import database models: {str(e)}")
    raise

app = Flask(__name__)
CORS(app)

# Configure Flask-Caching
cache = Cache(app, config={
    'CACHE_TYPE': 'simple',
    'CACHE_DEFAULT_TIMEOUT': 300
})

# API versioning prefix
API_V1 = '/api/v1'

def get_db_session():
    return Session()

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# Health check endpoint
@app.route('/', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "Flask API is running"}), 200

# Job endpoints
@app.route(f'{API_V1}/jobs', methods=['GET'])
@cache.cached(timeout=60)  # Cache for 1 minute
def get_jobs():
    session = get_db_session()
    try:
        # Get query parameters
        location = request.args.get('location')
        job_type = request.args.get('job_type')
        accommodations = request.args.getlist('accommodations')

        # Build query
        query = session.query(Job)
        if location:
            query = query.filter(Job.location == location)
        if job_type:
            query = query.filter(Job.job_type == job_type)
        if accommodations:
            for acc in accommodations:
                query = query.filter(Job.accommodations.contains([acc]))

        jobs = query.all()
        return jsonify([{
            'id': job.id,
            'title': job.title,
            'company_id': job.company_id,
            'location': job.location,
            'job_type': job.job_type,
            'accommodations': job.accommodations,
            'description': job.description,
            'posted_date': job.posted_date.isoformat() if job.posted_date else None
        } for job in jobs])
    except Exception as e:
        logger.error(f"Error fetching jobs: {str(e)}")
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

# Company endpoints
@app.route(f'{API_V1}/companies', methods=['GET'])
@cache.cached(timeout=300)  # Cache for 5 minutes
def get_companies():
    session = get_db_session()
    try:
        companies = session.query(Company).all()
        return jsonify([{
            'id': company.id,
            'name': company.name,
            'website': company.website,
            'verified': company.verified,
            'verification_status': company.verification_status,
            'description': company.description,
            'accessibility_features': company.accessibility_features
        } for company in companies])
    except Exception as e:
        logger.error(f"Error fetching companies: {str(e)}")
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

@app.route(f'{API_V1}/companies/<int:company_id>/jobs', methods=['GET'])
def get_company_jobs(company_id):
    session = get_db_session()
    try:
        jobs = session.query(Job).filter_by(company_id=company_id).all()
        return jsonify([{
            'id': job.id,
            'title': job.title,
            'location': job.location,
            'job_type': job.job_type,
            'accommodations': job.accommodations,
            'description': job.description,
            'posted_date': job.posted_date.isoformat() if job.posted_date else None
        } for job in jobs])
    except Exception as e:
        logger.error(f"Error fetching company jobs: {str(e)}")
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

# Application endpoints
@app.route(f'{API_V1}/applications', methods=['POST'])
def submit_application():
    session = get_db_session()
    try:
        data = request.get_json()
        new_application = JobApplication(
            user_id=data['user_id'],
            job_id=data['job_id'],
            status='applied',
            applied_date=datetime.utcnow()
        )
        session.add(new_application)
        session.commit()
        return jsonify({'message': 'Application submitted successfully'}), 201
    except Exception as e:
        logger.error(f"Error submitting application: {str(e)}")
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

@app.route(f'{API_V1}/applications/<int:user_id>', methods=['GET'])
def get_user_applications(user_id):
    session = get_db_session()
    try:
        applications = session.query(JobApplication).filter_by(user_id=user_id).all()
        return jsonify([{
            'id': app.id,
            'job_id': app.job_id,
            'status': app.status,
            'applied_date': app.applied_date.isoformat() if app.applied_date else None
        } for app in applications])
    except Exception as e:
        logger.error(f"Error fetching user applications: {str(e)}")
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

if __name__ == '__main__':
    try:
        # Install Flask-Caching
        os.system('pip install flask-caching')

        port = int(os.environ.get('FLASK_PORT', 5001))
        logger.info(f"Starting Flask API on port {port}")
        app.run(host='0.0.0.0', port=port)
    except Exception as e:
        logger.error(f"Failed to start Flask API: {str(e)}")
        raise