import streamlit as st
import sqlite3
import pandas as pd
from io import BytesIO
from openpyxl import Workbook

st.set_page_config(page_title="Reports", layout="wide")

st.title("📑 Reports")

conn = sqlite3.connect("students.db")

students = pd.read_sql_query("SELECT * FROM students", conn)
companies = pd.read_sql_query("SELECT * FROM companies", conn)

st.subheader("Student Report")

st.dataframe(students, width="stretch")

csv = students.to_csv(index=False)

st.download_button(
    "📥 Download Student CSV",
    csv,
    file_name="students.csv",
    mime="text/csv"
)

st.divider()

st.subheader("Company Report")

st.dataframe(companies, width="stretch")

company_csv = companies.to_csv(index=False)

st.download_button(
    "📥 Download Company CSV",
    company_csv,
    file_name="companies.csv",
    mime="text/csv"
)

st.divider()

st.subheader("Download Excel Report")

wb = Workbook()

ws = wb.active
ws.title = "Students"

ws.append(list(students.columns))

for row in students.values.tolist():
    ws.append(row)

ws2 = wb.create_sheet("Companies")

ws2.append(list(companies.columns))

for row in companies.values.tolist():
    ws2.append(row)

buffer = BytesIO()

wb.save(buffer)

buffer.seek(0)

st.download_button(
    "📥 Download Excel",
    buffer,
    file_name="Placement_Report.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

conn.close()