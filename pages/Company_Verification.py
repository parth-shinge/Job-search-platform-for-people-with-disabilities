import streamlit as st
from utils.data_manager import save_company_verification

st.set_page_config(page_title="Company Verification", page_icon="✓")

st.title("Company Verification ✓")

st.markdown("""
    <div role="region" aria-label="Verification information">
        <p>Get your company verified to show your commitment to inclusive hiring practices.</p>
    </div>
""", unsafe_allow_html=True)

with st.form("verification_form"):
    st.header("Company Information")
    
    company_name = st.text_input("Company Name", key="company_name")
    company_website = st.text_input("Company Website", key="company_website")
    
    col1, col2 = st.columns(2)
    with col1:
        contact_name = st.text_input("Contact Person Name", key="contact_name")
        contact_email = st.text_input("Contact Email", key="contact_email")
    
    with col2:
        contact_position = st.text_input("Contact Position", key="contact_position")
        contact_phone = st.text_input("Contact Phone", key="contact_phone")

    st.header("Accessibility Commitments")
    
    st.markdown("""
        <div role="region" aria-label="Accessibility commitments section">
            <p>Select all that apply to your organization:</p>
        </div>
    """, unsafe_allow_html=True)
    
    commitments = st.multiselect(
        "Select all that apply",
        [
            "Accessible workplace facilities",
            "Screen reader compatible systems",
            "Flexible work arrangements",
            "Dedicated HR support for disabilities",
            "Regular accessibility training",
            "Adaptive equipment provision"
        ],
        key="commitments"
    )
    
    st.header("Documentation")
    
    documentation = st.multiselect(
        "Required Documents",
        [
            "Accessibility Policy",
            "Equal Employment Opportunity Statement",
            "Accommodation Request Process",
            "Employee Training Records"
        ],
        key="documentation"
    )
    
    additional_info = st.text_area(
        "Additional Information",
        help="Please provide any additional information about your company's commitment to accessibility",
        key="additional_info"
    )
    
    password = st.text_input("Password", type="password", key="password")
    
    terms = st.checkbox(
        "I confirm that all information provided is accurate and our company is committed to inclusive hiring practices.",
        key="terms"
    )
    
    submitted = st.form_submit_button("Submit Verification Request")

if submitted:
    if not terms:
        st.error("Please accept the terms to submit the verification request.")
    else:
        verification_data = {
            "company_name": company_name,
            "company_website": company_website,
            "contact_name": contact_name,
            "contact_email": contact_email,
            "contact_position": contact_position,
            "contact_phone": contact_phone,
            "commitments": commitments,
            "documentation": documentation,
            "additional_info": additional_info,
            "password": password
        }
        
        save_company_verification(verification_data)
        
        # Send verification email
        subject = "Company Verification Request Received"
        message = f"""
        Dear {company_name},

        Thank you for submitting your company verification request. Our team will review your application and contact you within 5 business days.

        Best regards,
        The Able Connect Team
        """
        