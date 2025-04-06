import streamlit as st
from utils.data_manager import get_user_profile

st.set_page_config(page_title="Login", page_icon="🔑")

st.title("Login 🔑")

# Check if user is already logged in
if 'user_email' in st.session_state:
    st.success(f"You are already logged in as {st.session_state.user_email}")
    if st.button("Go to Your Profile"):
        st.experimental_set_query_params(page="user_profile", user_email=st.session_state.user_email)
    if st.button("Logout"):
        del st.session_state['user_email']
        st.experimental_set_query_params(page="home")
    st.stop()

st.markdown("""
    <div role="region" aria-label="Login information">
        <p>Sign in to access your profile, applications, and job preferences.</p>
    </div>
""", unsafe_allow_html=True)

# Login Form
with st.form("login_form"):
    email = st.text_input("Email Address", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")
    
    submit_button = st.form_submit_button("Login")
    
    if submit_button and email and password:
        # Simple validation
        if '@' not in email or '.' not in email:
            st.error("Please enter a valid email address")
        else:
            # Check if user exists and password matches
            user_profile = get_user_profile(email, password)
            if user_profile is not None:
                # Set session state
                st.session_state['user_email'] = email
                st.success("Login successful! Redirecting to your profile...")
                st.switch_page("pages/User_Profile.py")
            else:
                st.error("Invalid email or password. Please try again.")
                if st.button("Go to Registration"):
                    st.switch_page("pages/Register.py")

# Option to register
st.markdown("---")
st.markdown("New to Inclusive Jobs? Create an account now.")
if st.button("Register"):
    st.switch_page("pages/Register.py")

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