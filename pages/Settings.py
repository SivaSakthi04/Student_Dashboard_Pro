import streamlit as st
import sqlite3

st.set_page_config(page_title="Settings", layout="wide")

st.title("⚙ Settings")

conn = sqlite3.connect("students.db")
cur = conn.cursor()

st.subheader("🔐 Change Admin Password")

old = st.text_input("Old Password", type="password")
new = st.text_input("New Password", type="password")
confirm = st.text_input("Confirm Password", type="password")

if st.button("Update Password"):

    admin = cur.execute(
        "SELECT * FROM admin"
    ).fetchone()

    if admin[1] != old:
        st.error("Old Password Incorrect")

    elif new != confirm:
        st.error("Passwords do not match")

    else:

        cur.execute(
            "UPDATE admin SET password=? WHERE username=?",
            (new, admin[0])
        )

        conn.commit()

        st.success("Password Updated Successfully")

st.divider()

st.subheader("Logout")

if st.button("🚪 Logout"):

    st.session_state["login"] = False

    st.success("Logged Out")

    st.switch_page("app.py")

conn.close()