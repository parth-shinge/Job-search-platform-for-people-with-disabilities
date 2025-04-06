import streamlit as st

st.set_page_config(
    page_title="Able Connect",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configure accessibility settings
st.markdown("""
    <style>
        .st.title {
            font-size: 2.5rem;
            font-weight: bold;
            color: #0066cc;
        }
        

        .stButton button {
            width: 100%;
            padding: 0.75rem;
            font-size: 1.1rem;
        }
        .st-bb {
            border: 2px solid #0066cc !important;
        }
        *:focus {
            outline: 3px solid #0066cc !important;
            outline-offset: 2px !important;
        }
    </style>
""", unsafe_allow_html=True)

st.image("logo.png", width=200)

st.title("Welcome to Able Connect! 🚀")


st.markdown("""
    <div role="main" aria-label="Welcome section">
        <h2>Find Your Perfect Career Match</h2>
        <p>We're committed to creating an inclusive job marketplace that works for everyone.</p>
    </div>
""", unsafe_allow_html=True)

st.image("b2.jpg", width=400)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        <div role="region" aria-label="Job seeker section">
            <h3>For Job Seekers</h3>
            <ul>
                <li>Search accessible job opportunities</li>
                <li>Create professional resumes</li>
                <li>Filter by accommodation types</li>
                <li>Download PDF resumes</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("Start Job Search", key="job_search"):
        st.switch_page("pages/Job_Search.py")

with col2:
    st.markdown("""
        <div role="region" aria-label="Employer section">
            <h3>For Employers</h3>
            <ul>
                <li>Post accessible job listings</li>
                <li>Get company verification</li>
                <li>Connect with diverse talent</li>
                <li>Showcase inclusive workplace</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("Verify Company", key="company_verify"):
        st.switch_page("pages/Company_Verification.py")

st.markdown("---")

st.markdown("""
    <div role="contentinfo" aria-label="Accessibility information">
        <h3>Accessibility Features</h3>
        <ul>
            <li>Screen reader optimized</li>
            <li>Keyboard navigation support</li>
            <li>High contrast mode available</li>
            <li>Clear typography and spacing</li>
        </ul>
    </div>
""", unsafe_allow_html=True)

