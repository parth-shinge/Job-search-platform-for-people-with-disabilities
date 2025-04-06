import streamlit as st
from utils.data_manager import get_user_profile_by_email, update_user_profile, get_job_applications
import json

st.set_page_config(page_title="User Profile", page_icon="👤")

st.title("User Profile 👤")

# Check if user is logged in (email stored in session state)
if 'user_email' not in st.session_state:
    st.warning("Please log in to view your profile")
    if st.button("Go to Login"):
        st.experimental_set_query_params(page="login")
    st.stop()

user_email = st.session_state.user_email
user_data = get_user_profile_by_email(user_email)

if user_data:
    # Profile Information
    st.header("Personal Information")
    
    with st.form("profile_form"):
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First Name", value=user_data.get('first_name', ''))
            email = st.text_input("Email", value=user_email, disabled=True)
        with col2:
            last_name = st.text_input("Last Name", value=user_data.get('last_name', ''))
            phone = st.text_input("Phone", value=user_data.get('phone', ''))
        
        location = st.text_input("Location", value=user_data.get('location', ''))
        
        # Accessibility Preferences
        st.subheader("Accessibility Preferences")
        accessibility_needs = st.multiselect(
            "Select your accessibility requirements",
            ["Screen Reader Support", "High Contrast", "Large Text", "Voice Navigation",
             "Keyboard Navigation", "Color Blind Support"],
            default=user_data.get('accessibility_needs', [])
        )
        
        # Job Preferences
        st.subheader("Job Preferences")
        preferred_job_types = st.multiselect(
            "Preferred Job Types",
            ["Full-time", "Part-time", "Remote", "Hybrid", "On-site"],
            default=user_data.get('preferred_job_types', [])
        )
        
        desired_role = st.text_input("Desired Role", value=user_data.get('desired_role', ''))
        
        if st.form_submit_button("Update Profile"):
            updated_data = {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'phone': phone,
                'location': location,
                'accessibility_needs': accessibility_needs,
                'preferred_job_types': preferred_job_types,
                'desired_role': desired_role
            }
            update_user_profile(email, updated_data)
            st.success("Profile updated successfully!")

    # Job Applications
    st.header("Your Job Applications")
    applications = get_job_applications(user_email)
    
    if applications:
        for idx, app in enumerate(applications):
            with st.expander(f"{app.job.title} at {app.job.company.name}"):
                st.write(f"Status: {app.status}")
                st.write(f"Applied: {app.applied_date.strftime('%B %d, %Y')}")
                st.write(f"Location: {app.job.location}")
                st.write(f"Job Type: {app.job.job_type}")
                if app.resume:
                    st.download_button(
                        label="Download Resume",
                        data=app.resume,
                        file_name=f"{app.job.title}_resume.pdf",
                        mime="application/pdf",
                        key=f"download_resume_{idx}"
                    )
                if app.cover_letter:
                    st.write("**Cover Letter:**")
                    st.write(app.cover_letter)
                if app.additional_notes:
                    st.write("**Additional Notes:**")
                    st.write(app.additional_notes)
    else:
        st.info("You haven't applied to any jobs yet.")
        if st.button("Browse Jobs"):
           st.switch_page("pages/Job_Search.py")
else:
    st.error("Error loading profile data. Please try again later.")
    