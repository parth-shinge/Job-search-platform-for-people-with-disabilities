import streamlit as st
from utils.data_manager import get_company_by_email

st.set_page_config(page_title="Company Login", page_icon="🔒")

st.title("Company Login 🔒")

email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Login"):
    st.write(f"Email: {email}")
    st.write(f"Password: {password}")
    
    company = get_company_by_email(email)
    st.write(f"Fetched Company: {company}")
    
    if company:
        st.write(f"Stored Password: {company.password}")
        if company.password == password:
            st.session_state.company_id = company.id
            st.success("Login successful!")
            st.switch_page("pages/Company_Profile.py")
        else:
            st.error("Invalid email or password")
    else:
        st.error("Invalid email or password")