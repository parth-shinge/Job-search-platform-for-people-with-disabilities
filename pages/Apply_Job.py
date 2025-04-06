import streamlit as st
from utils.data_manager import get_user_profile_by_email, save_job_application
import json

st.set_page_config(page_title="Apply for Job", page_icon="📝")

# Check if user is logged in and a job is selected
if 'user_email' not in st.session_state or 'selected_job' not in st.session_state:
    st.warning("Please select a job to apply for")
    if st.button("Browse Jobs"):
        st.switch_page("pages/Job_Search.py")
    st.stop()

# Get user profile and selected job
user_email = st.session_state.user_email
user_profile = get_user_profile_by_email(user_email)
selected_job = st.session_state.selected_job

if not user_profile:
    st.error("Error loading user profile")
    st.stop()

st.title("Apply for Job 📝")

# Display job details
st.header("Selected Position")
st.write(f"**Position:** {selected_job['title'] if isinstance(selected_job, dict) else selected_job.title}")
st.write(f"**Location:** {selected_job['location'] if isinstance(selected_job, dict) else selected_job.location}")
st.write(f"**Type:** {selected_job['job_type'] if isinstance(selected_job, dict) else selected_job.job_type}")

# File uploader for resume
uploaded_resume = st.file_uploader("Upload Your Resume", type=["pdf", "docx"])

# Optional cover letter
cover_letter = st.text_area(
    "Cover Letter (Optional)",
    help="Add a personalized message to your application"
)

# Additional notes or accommodations
additional_notes = st.text_area(
    "Additional Notes (Optional)",
    help="Specify any additional information or required accommodations"
)

# Confirmation
st.info("By submitting this application, you confirm that all provided information is accurate.")

if st.button("Submit Application"):
    try:
        # Prepare application data
        application_data = {
            'first_name': user_profile.get('first_name', ''),
            'last_name': user_profile.get('last_name', ''),
            'email': user_profile.get('email', ''),
            'phone': user_profile.get('phone', ''),
            'location': user_profile.get('location', ''),
            'cover_letter': cover_letter,
            'additional_notes': additional_notes
        }
        
        # Save uploaded resume
        if uploaded_resume is not None:
            application_data['resume'] = uploaded_resume.getvalue()
        
        # Save application
        job_id = selected_job['id'] if isinstance(selected_job, dict) else selected_job.id
        save_job_application(application_data, job_id)
        
        st.success("""
            Application submitted successfully! 
            You can track your application status in your profile.
        """)
        
        if st.button("View My Applications"):
            st.switch_page("pages/User_Profile.py")
            
    except Exception as e:
        st.error(f"Error submitting application: {str(e)}")