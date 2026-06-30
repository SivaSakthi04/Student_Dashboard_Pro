import streamlit as st
from login import login

# Page Configuration
st.set_page_config(
    page_title="Student Dashboard",
    layout="wide"
)

# Load CSS
with open("assets/style.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

# Login Session
if "login" not in st.session_state:
    st.session_state["login"] = False

# Show Login or Dashboard
if not st.session_state["login"]:
    login()
else:
    st.switch_page("pages/Dashboard.py")