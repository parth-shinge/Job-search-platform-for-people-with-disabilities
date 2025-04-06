import streamlit as st
from utils.data_manager import get_user_profile_by_email, load_jobs

st.set_page_config(page_title="Job Search", page_icon="🔍")

st.title("Job Search 🔍")

# Check if user is logged in (email stored in session state)
if 'user_email' not in st.session_state:
    st.warning("Please log in to search for jobs")
    if st.button("Go to Login"):
        st.switch_page("pages/Login.py")
    st.stop()

user_email = st.session_state.user_email
user_profile = get_user_profile_by_email(user_email)

if user_profile:
    st.header("Welcome back, " + user_profile.get('first_name', 'User') + "!")
    
    # Job Search Filters
    st.sidebar.header("Filter Jobs")
    job_type = st.sidebar.multiselect(
        "Job Type",
        ["Full-time", "Part-time", "Remote", "Hybrid", "On-site"],
        default=user_profile.get('preferred_job_types', [])
    )
    location = st.sidebar.text_input("Location", value=user_profile.get('location', ''))
    
    # Load jobs from database
    jobs = load_jobs()
    
    # Filter jobs based on user input
    if job_type:
        jobs = [job for job in jobs if job.job_type in job_type]
    if location:
        jobs = [job for job in jobs if location.lower() in job.location.lower()]
    
    # Display jobs
    if jobs:
        for job in jobs:
            with st.expander(f"{job.title} at {job.company.name}"):
                st.write(f"Location: {job.location}")
                st.write(f"Job Type: {job.job_type}")
                st.write(f"Description: {job.description}")
                if st.button("Apply", key=f"apply_{job.id}"):
                    st.session_state.selected_job = job
                    st.switch_page("pages/Apply_Job.py")
    else:
        st.info("No jobs found matching your criteria.")
else:
    st.error("Error loading profile data. Please try again later.")