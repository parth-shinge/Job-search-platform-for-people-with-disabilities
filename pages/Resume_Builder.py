import streamlit as st
from utils.pdf_generator import generate_resume_pdf, get_template_1, get_template_2

st.set_page_config(page_title="Resume Builder", page_icon="📝")

st.title("Resume Builder 📝")

# Resume form
with st.form("resume_form"):
    st.header("Personal Information")
    
    col1, col2 = st.columns(2)
    with col1:
        first_name = st.text_input("First Name", key="first_name")
        email = st.text_input("Email", key="email")
        phone = st.text_input("Phone", key="phone")
    
    with col2:
        last_name = st.text_input("Last Name", key="last_name")
        location = st.text_input("Location", key="location")
        linkedin = st.text_input("LinkedIn URL (optional)", key="linkedin")
        picture = st.file_uploader("Upload Picture", type=["jpg", "jpeg", "png"], key="picture")

    st.header("Professional Summary")
    summary = st.text_area("Summary", height=100, key="summary",
                          help="Briefly describe your professional background and goals")

    st.header("Work Experience")
    num_experiences = st.number_input("Number of experiences", min_value=0, max_value=5, value=1)
    
    experiences = []
    for i in range(num_experiences):
        st.subheader(f"Experience {i+1}")
        exp_col1, exp_col2 = st.columns(2)
        with exp_col1:
            company = st.text_input("Company", key=f"company_{i}")
            position = st.text_input("Position", key=f"position_{i}")
        with exp_col2:
            start_date = st.date_input("Start Date", key=f"start_date_{i}")
            end_date = st.date_input("End Date", key=f"end_date_{i}")
        description = st.text_area("Description", key=f"description_{i}")
        experiences.append({
            "company": company,
            "position": position,
            "start_date": start_date,
            "end_date": end_date,
            "description": description
        })

    st.header("Education")
    num_education = st.number_input("Number of education entries", min_value=0, max_value=3, value=1)
    
    education = []
    for i in range(num_education):
        st.subheader(f"Education {i+1}")
        edu_col1, edu_col2 = st.columns(2)
        with edu_col1:
            institution = st.text_input("Institution", key=f"institution_{i}")
            degree = st.text_input("Degree", key=f"degree_{i}")
        with edu_col2:
            grad_date = st.date_input("Graduation Date", key=f"grad_date_{i}")
        education.append({
            "institution": institution,
            "degree": degree,
            "graduation_date": grad_date
        })

    st.header("Skills")
    skills = st.text_area("List your skills (one per line)", key="skills")

    # Template selection
    st.header("Choose Template")
    template = st.selectbox(
        "Resume Template",
        ["Professional", "Modern"],
        key="template"
    )

    submitted = st.form_submit_button("Generate Resume")

if submitted:
    # Prepare resume data
    resume_data = {
        "personal_info": {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone": phone,
            "location": location,
            "linkedin": linkedin,
            "picture": picture.getvalue() if picture else None
        },
        "summary": summary,
        "experiences": experiences,
        "education": education,
        "skills": [skill.strip() for skill in skills.split("\n") if skill.strip()]
    }

    # Generate PDF
    template_func = get_template_1 if template == "Professional" else get_template_2
    pdf_file = generate_resume_pdf(resume_data, template_func)
    
    # Offer download
    st.success("Resume generated successfully!")
    st.download_button(
        label="Download Resume PDF",
        data=pdf_file,
        file_name="resume.pdf",
        mime="application/pdf"
    )