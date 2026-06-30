import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Companies", layout="wide")

st.title("🏢 Company Management")

conn = sqlite3.connect("students.db", check_same_thread=False)
cur = conn.cursor()

st.subheader("➕ Add Company")

with st.form("company_form"):

    company = st.text_input("Company Name")

    role = st.text_input("Job Role")

    package = st.number_input(
        "Package (LPA)",
        min_value=0.0,
        step=0.5
    )

    location = st.text_input("Location")

    submit = st.form_submit_button("Add Company")

    if submit:

        cur.execute("""
        INSERT INTO companies
        (company_name,role,package,location)
        VALUES(?,?,?,?)
        """,
        (
            company,
            role,
            package,
            location
        ))

        conn.commit()

        st.success("Company Added Successfully")

        st.rerun()

st.divider()

df = pd.read_sql_query(
    "SELECT * FROM companies ORDER BY id DESC",
    conn
)

st.dataframe(
    df,
    width="stretch"
)

st.divider()

csv = df.to_csv(index=False)

st.download_button(
    "📥 Download Company List",
    csv,
    file_name="companies.csv",
    mime="text/csv"
)

conn.close()