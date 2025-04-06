import streamlit as st
from utils.data_manager import create_user_if_not_exists

st.set_page_config(page_title="Register", page_icon="📝")

st.title("Create Account 📝")

st.markdown("""
    <div role="region" aria-label="Registration information">
        <p>Create your account to apply for jobs and manage your profile.</p>
    </div>
""", unsafe_allow_html=True)

# Registration Form
with st.form("registration_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        username = st.text_input("Username", key="reg_username")
        first_name = st.text_input("First Name", key="reg_first_name")
    
    with col2:
        email = st.text_input("Email Address", key="reg_email")
        last_name = st.text_input("Last Name", key="reg_last_name")
    
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    
    # Terms and conditions
    agree = st.checkbox("I agree to the Terms and Conditions")
    
    submit_button = st.form_submit_button("Register")
    
    if submit_button:
        # Validate form
        if not username:
            st.error("Please enter your username")
        elif not email or '@' not in email or '.' not in email:
            st.error("Please enter a valid email address")
        elif not password or not confirm_password:
            st.error("Please enter and confirm your password")
        elif password != confirm_password:
            st.error("Passwords do not match")
        elif not agree:
            st.error("You must agree to the Terms and Conditions")
        else:
            # Try to create user
            profile_data = {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "username": username
            }
            
            try:
                user_created = create_user_if_not_exists(username, email, password, profile_data)
                
                if user_created:
                    st.success("Account created successfully! Redirecting to your profile...")
                    st.experimental_set_query_params(page="user_profile", user_email=email)
                else:
                    st.warning("An account with this email already exists.")
                    if st.button("Go to Login"):
                     st.experimental_set_query_params(page="login")
            except Exception as e:
                st.error(f"Error creating account: {str(e)}")

# Option to login
st.markdown("---")
st.markdown("Already have an account?")
if st.button("Login"):
    st.experimental_set_query_params(page="login")

# Add keyboard navigation help
st.sidebar.markdown("""
    <div role="complementary" aria-label="Keyboard shortcuts">
        <h4>Keyboard Shortcuts</h4>
        <ul>
            <li>Tab: Navigate through elements</li>
            <li>Space/Enter: Select/Activate</li>
            <li>Esc: Clear selection</li>
        </ul>
    </div>
""", unsafe_allow_html=True)