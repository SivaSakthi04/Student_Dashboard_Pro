import streamlit as st
import sqlite3

def login():

    st.title("🎓 Student Dashboard Login")

    username = st.text_input("Username")
    password = st.text_input("Password",type="password")

    if st.button("Login"):

        conn=sqlite3.connect("students.db")
        cur=conn.cursor()

        cur.execute(
            "SELECT * FROM admin WHERE username=? AND password=?",
            (username,password)
        )

        user=cur.fetchone()

        if user:
            st.session_state["login"]=True
            st.success("Login Successful")
            st.rerun()

        else:
            st.error("Invalid Username or Password")

        conn.close()