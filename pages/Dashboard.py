import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Student Dashboard",
    layout="wide"
)

st.title("🎓 Student Placement Dashboard")
st.write("Welcome Admin 👋")

# ---------------- DATABASE ----------------

conn = sqlite3.connect("students.db")

students = pd.read_sql_query(
    "SELECT * FROM students",
    conn
)

try:
    companies = pd.read_sql_query(
        "SELECT * FROM companies",
        conn
    )
except:
    companies = pd.DataFrame()

conn.close()

# ---------------- KPI ----------------

total_students = len(students)

placed = len(
    students[students["status"] == "Placed"]
)

not_placed = len(
    students[students["status"] == "Not Placed"]
)

avg_cgpa = round(
    students["cgpa"].mean(),
    2
) if total_students else 0

placement_percentage = round(
    (placed / total_students) * 100,
    1
) if total_students else 0

total_companies = len(companies)

c1, c2, c3, c4 = st.columns(4)

c1.metric("👨‍🎓 Students", total_students)
c2.metric("✅ Placed", placed)
c3.metric("🏢 Companies", total_companies)
c4.metric("📈 Placement %", f"{placement_percentage}%")

c5, c6, c7, c8 = st.columns(4)

c5.metric("❌ Not Placed", not_placed)
c6.metric("⭐ Average CGPA", avg_cgpa)
c7.metric(
    "🏆 Highest CGPA",
    students["cgpa"].max() if total_students else 0
)
c8.metric("📚 Departments",
          students["department"].nunique() if total_students else 0)

st.divider()

# ---------------- CHARTS ----------------

left, right = st.columns(2)

with left:

    if total_students:

        dept = students.groupby(
            "department"
        ).size().reset_index(name="Students")

        fig = px.bar(
            dept,
            x="department",
            y="Students",
            color="department",
            title="Department Wise Students"
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

with right:

    if total_students:

        fig = px.pie(
            students,
            names="status",
            title="Placement Status"
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

st.divider()

# ---------------- LINE CHART ----------------

if total_students:

    line = students.groupby(
        "department"
    )["cgpa"].mean().reset_index()

    fig = px.line(
        line,
        x="department",
        y="cgpa",
        markers=True,
        title="Average CGPA by Department"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

# ---------------- COMPANY PACKAGE ----------------

if not companies.empty:

    st.subheader("🏢 Company Packages")

    fig = px.bar(
        companies,
        x="company_name",
        y="package",
        color="company_name"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

# ---------------- TOP STUDENTS ----------------

st.subheader("🏆 Top Students")

if total_students:

    top = students.sort_values(
        by="cgpa",
        ascending=False
    )

    st.dataframe(
        top.head(10),
        width="stretch"
    )

# ---------------- ALL STUDENTS ----------------

st.subheader("📋 All Students")

st.dataframe(
    students,
    width="stretch"
)