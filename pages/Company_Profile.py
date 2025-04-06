
import streamlit as st
from utils.data_manager import get_company_profile, update_company_profile, get_company_jobs
from utils.data_manager import get_applications_for_company, post_new_job, send_email_to_applicant
import json
from datetime import datetime

st.set_page_config(page_title="Company Profile", page_icon="🏢")

st.title("Company Profile 🏢")

# Check if company is logged in
if 'company_id' not in st.session_state:
    st.warning("Please Login to access the profile")
    if st.button("Go to Login"):
        st.switch_page("pages/Company_Login.py")
    st.stop()

company_id = st.session_state.company_id
company_data = get_company_profile(company_id)

if company_data:
    # Navigation bar
    st.sidebar.title("Company Dashboard")
    page = st.sidebar.radio(
        "Navigate to",
        ["Company Information", "Posted Jobs", "Job Applications", "Post New Job"]
    )
    
    if page == "Company Information":
        # Company Information
        st.header("Company Information")
        
        with st.form("company_profile_form"):
            company_name = st.text_input("Company Name", value=company_data.name, disabled=True)
            website = st.text_input("Website", value=company_data.website)
            
            # Company Description
            description = st.text_area(
                "Company Description",
                value=company_data.description if hasattr(company_data, 'description') else '',
                help="Describe your company's mission and commitment to inclusive hiring"
            )
            
            # Accessibility Features
            st.subheader("Workplace Accessibility")
            accessibility_features = st.multiselect(
                "Select available accessibility features",
                [
                    "Wheelchair Accessible",
                    "Screen Reader Compatible Systems",
                    "Flexible Work Hours",
                    "Remote Work Options",
                    "Assistive Technology",
                    "Sign Language Support",
                    "Quiet Workspaces",
                    "Ergonomic Equipment"
                ],
                default=company_data.accessibility_features if hasattr(company_data, 'accessibility_features') else []
            )
            
            # Company Culture
            st.subheader("Inclusive Workplace Culture")
            culture_points = st.text_area(
                "Describe your inclusive workplace culture",
                value=company_data.culture if hasattr(company_data, 'culture') else '',
                help="Highlight your company's commitment to diversity and inclusion"
            )
            
            if st.form_submit_button("Update Profile"):
                updated_data = {
                    'website': website,
                    'description': description,
                    'accessibility_features': accessibility_features,
                    'culture': culture_points
                }
                update_company_profile(company_id, updated_data)
                st.success("Company profile updated successfully!")
    
    elif page == "Posted Jobs":
        # Posted Jobs
        st.header("Posted Jobs")
        jobs = get_company_jobs(company_id)
        
        if jobs:
            for job in jobs:
                with st.expander(f"{job.title} - {job.job_type}"):
                    st.write(f"Location: {job.location}")
                    st.write(f"Posted: {job.posted_date.strftime('%B %d, %Y')}")
                    st.write("Accommodations:", ", ".join(job.accommodations) if job.accommodations else "None")
                    st.write("Description:", job.description)
                    
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Edit Job", key=f"edit_{job.id}"):
                            st.session_state.job_to_edit = job
                            st.rerun()
                    with col2:
                        if st.button("View Applications", key=f"apps_{job.id}"):
                            st.session_state.selected_job_id = job.id
                            st.rerun()
        else:
            st.info("No jobs posted yet.")
    
    elif page == "Job Applications":
        # Job Applications
        st.header("Job Applications")
        applications = get_applications_for_company(company_id)
        
        if applications:
            for app in applications:
                with st.expander(f"{app['user_name']} - {app['job_title']} - {app['applied_date'].strftime('%B %d, %Y')}"):
                    # Display applicant information
                    st.subheader("Applicant Information")
                    st.write(f"Name: {app['user_name']}")
                    st.write(f"Email: {app['user_email']}")
                    st.write(f"Status: {app['status'].capitalize()}")
                    
                    # Display resume
                    st.subheader("Resume")
                    if app['user_resume']:
                        resume = app['user_resume']
                        if 'first_name' in resume and 'last_name' in resume:
                            st.write(f"Full Name: {resume.get('first_name', '')} {resume.get('last_name', '')}")
                        if 'summary' in resume:
                            st.write("Summary:", resume.get('summary', ''))
                        if 'skills' in resume:
                            st.write("Skills:", ", ".join(resume.get('skills', [])))
                        if 'experience' in resume:
                            st.subheader("Experience")
                            for exp in resume.get('experience', []):
                                st.write(f"{exp.get('title', '')} at {exp.get('company', '')}")
                                st.write(f"{exp.get('start_date', '')} - {exp.get('end_date', '')}")
                                st.write(exp.get('description', ''))
                        if 'education' in resume:
                            st.subheader("Education")
                            for edu in resume.get('education', []):
                                st.write(f"{edu.get('degree', '')} from {edu.get('institution', '')}")
                                st.write(f"{edu.get('start_date', '')} - {edu.get('end_date', '')}")
                    else:
                        st.warning("No resume data available")
                    
                    # Email applicant
                    st.subheader("Contact Applicant")
                    with st.form(key=f"email_form_{app['application_id']}"):
                        email_subject = st.text_input("Subject", value=f"Regarding your application for {app['job_title']}")
                        email_body = st.text_area("Message")
                        status_options = ["reviewing", "interview", "selected", "rejected"]
                        new_status = st.selectbox("Update Status", options=status_options, index=0)
                        
                        if st.form_submit_button("Send Email"):
                            email_data = {
                                'subject': email_subject,
                                'message': email_body,
                                'status': new_status
                            }
                            if send_email_to_applicant(app['application_id'], email_data):
                                st.success("Email sent successfully!")
                            else:
                                st.error("Failed to send email")
        else:
            st.info("No applications received yet.")
    
    elif page == "Post New Job":
        # Post New Job
        st.header("Post a New Job")
        
        with st.form("post_job_form"):
            job_title = st.text_input("Job Title")
            job_description = st.text_area("Job Description")
            job_requirements = st.text_area("Job Requirements")
            
            col1, col2 = st.columns(2)
            with col1:
                job_type = st.selectbox(
                    "Job Type",
                    ["Full-time", "Part-time", "Contract", "Internship", "Remote"]
                )
            
            with col2:
                job_location = st.text_input("Location")
            
            # Accommodations
            st.subheader("Available Accommodations")
            accommodations = st.multiselect(
                "Select all accommodations available for this position",
                [
                    "Visual Impairment",
                    "Hearing Impairment",
                    "Mobility Support",
                    "Cognitive Support",
                    "Remote Work",
                    "Flexible Hours",
                    "Assistive Technology",
                    "Sign Language"
                ]
            )
            
            if st.form_submit_button("Post Job"):
                if not job_title or not job_description or not job_requirements:
                    st.error("Please fill in all required fields")
                else:
                    job_data = {
                        'title': job_title,
                        'company_id': company_id,
                        'description': job_description,
                        'requirements': job_requirements,
                        'job_type': job_type,
                        'location': job_location,
                        'accommodations': accommodations
                    }
                    try:
                        post_new_job(job_data)
                        st.success("Job posted successfully!")
                    except Exception as e:
                        st.error(f"Error posting job: {str(e)}")

else:
    st.error("Error loading company profile data. Please try again later.")
