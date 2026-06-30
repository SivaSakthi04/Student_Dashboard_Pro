import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(
    page_title="Students",
    layout="wide"
)

# ---------------- DATABASE ----------------

conn = sqlite3.connect("students.db", check_same_thread=False)
cur = conn.cursor()

st.title("👨‍🎓 Student Management")

# ---------------- TOTAL STUDENTS ----------------

count = cur.execute(
    "SELECT COUNT(*) FROM students"
).fetchone()[0]

st.info(f"👨‍🎓 Total Students : {count}")

st.divider()

# ---------------- ADD STUDENT ----------------

st.subheader("➕ Add Student")

with st.form("add_student_form"):

    name = st.text_input("Student Name")

    department = st.selectbox(
        "Department",
        [
            "MCA",
            "BCA",
            "B.Sc CS",
            "MBA",
            "B.Com"
        ]
    )

    cgpa = st.number_input(
        "CGPA",
        min_value=0.0,
        max_value=10.0,
        step=0.1
    )

    status = st.selectbox(
        "Placement Status",
        [
            "Placed",
            "Not Placed"
        ]
    )

    email = st.text_input("Email")

    add_btn = st.form_submit_button("➕ Add Student")

    if add_btn:

        if name.strip() == "" or email.strip() == "":

            st.error("Please fill all fields.")

        else:

            cur.execute(
                """
                INSERT INTO students
                (name,department,cgpa,status,email)
                VALUES(?,?,?,?,?)
                """,
                (
                    name,
                    department,
                    cgpa,
                    status,
                    email
                )
            )

            conn.commit()

            st.success("Student Added Successfully")

            st.rerun()

st.divider()

# ---------------- LOAD DATA ----------------

df = pd.read_sql_query(
    "SELECT * FROM students ORDER BY id DESC",
    conn
)

# ---------------- SEARCH ----------------

left, right = st.columns(2)

with left:

    search = st.text_input("🔍 Search Student")

with right:

    departments = ["All"] + sorted(
        df["department"].unique().tolist()
    )

    selected_dept = st.selectbox(
        "Department Filter",
        departments
    )

if search:

    df = df[
        df["name"].str.contains(
            search,
            case=False
        )
    ]

if selected_dept != "All":

    df = df[
        df["department"] == selected_dept
    ]

st.subheader("📋 Student List")

st.dataframe(
    df,
    width="stretch"
)
st.divider()

# ---------------- EDIT STUDENT ----------------

st.subheader("✏️ Edit Student")

if not df.empty:

    selected_id = st.selectbox(
        "Select Student ID",
        df["id"].tolist(),
        key="edit_student"
    )

    row = df[df["id"] == selected_id].iloc[0]

    with st.form("edit_student_form"):

        edit_name = st.text_input(
            "Name",
            value=row["name"]
        )

        edit_department = st.selectbox(
            "Department",
            ["MCA","BCA","B.Sc CS","MBA","B.Com"],
            index=["MCA","BCA","B.Sc CS","MBA","B.Com"].index(row["department"])
            if row["department"] in ["MCA","BCA","B.Sc CS","MBA","B.Com"] else 0
        )

        edit_cgpa = st.number_input(
            "CGPA",
            min_value=0.0,
            max_value=10.0,
            value=float(row["cgpa"])
        )

        edit_status = st.selectbox(
            "Placement Status",
            ["Placed","Not Placed"],
            index=0 if row["status"]=="Placed" else 1
        )

        edit_email = st.text_input(
            "Email",
            value=row["email"]
        )

        update_btn = st.form_submit_button("Update Student")

        if update_btn:

            cur.execute("""
            UPDATE students
            SET
                name=?,
                department=?,
                cgpa=?,
                status=?,
                email=?
            WHERE id=?
            """,
            (
                edit_name,
                edit_department,
                edit_cgpa,
                edit_status,
                edit_email,
                selected_id
            ))

            conn.commit()

            st.success("✅ Student Updated Successfully")

            st.rerun()

st.divider()

# ---------------- DELETE ----------------

st.subheader("🗑 Delete Student")

if not df.empty:

    delete_id = st.selectbox(
        "Select Student ID",
        df["id"].tolist(),
        key="delete_student"
    )

    confirm = st.checkbox(
        "I confirm I want to delete this student."
    )

    if st.button("Delete Student"):

        if confirm:

            cur.execute(
                "DELETE FROM students WHERE id=?",
                (delete_id,)
            )

            conn.commit()

            st.success("Student Deleted Successfully")

            st.rerun()

        else:

            st.warning("Please confirm before deleting.")

st.divider()

# ---------------- DOWNLOAD ----------------

csv = df.to_csv(index=False)

st.download_button(
    label="📥 Download Students CSV",
    data=csv,
    file_name="students.csv",
    mime="text/csv"
)

conn.close()