import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Placement Drives", layout="wide")

st.title("📅 Placement Drive Management")

import os

db_path = os.path.abspath("students.db")

st.write("Database Path:", db_path)
st.write("Current Working Directory:", os.getcwd())
st.write("Database Path:", db_path)

conn = sqlite3.connect(db_path)

cur = conn.cursor()
tables = pd.read_sql_query(
    "SELECT name FROM sqlite_master WHERE type='table'",
    conn
)

st.write("Tables in DB")
st.dataframe(tables)

st.subheader("➕ Add Placement Drive")

with st.form("drive_form"):

    company = st.text_input("Company Name")

    drive_date = st.date_input("Drive Date")

    eligibility = st.number_input(
        "Minimum CGPA",
        min_value=0.0,
        max_value=10.0,
        step=0.1
    )

    venue = st.text_input("Venue")

    submit = st.form_submit_button("Add Drive")

    if submit:

        cur.execute("""
        INSERT INTO drives
        (company,drive_date,eligibility,venue)
        VALUES(?,?,?,?)
        """,
        (
            company,
            str(drive_date),
            eligibility,
            venue
        ))

        conn.commit()

        st.success("Drive Added Successfully")

        st.rerun()

st.divider()

df = pd.read_sql_query(
    "SELECT * FROM drives",
    conn
)

st.dataframe(df, width="stretch")

conn.close()