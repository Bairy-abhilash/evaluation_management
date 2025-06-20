import streamlit as st
import pandas as pd
import datetime

# Initialize session state for evaluation data
if 'eval_data' not in st.session_state:
    st.session_state.eval_data = pd.DataFrame(columns=[
        "Student Name", "Subject", "Marks", "Grade", "Evaluation Date"
    ])

def calculate_grade(marks):
    if marks >= 90:
        return 'A'
    elif marks >= 75:
        return 'B'
    elif marks >= 60:
        return 'C'
    elif marks >= 40:
        return 'D'
    else:
        return 'F'

def main():
    st.set_page_config(page_title="Evaluation Management System", layout="centered")
    st.title("📝 Evaluation Management System")

    menu = ["Add Evaluation", "View Records", "Search Records", "Filter by Grade"]
    choice = st.sidebar.radio("📋 Menu", menu)

    df = st.session_state.eval_data

    # 1️⃣ Add Evaluation
    if choice == "Add Evaluation":
        st.subheader("➕ Add Evaluation Record")
        name = st.text_input("Student Name")
        subject = st.text_input("Subject")
        marks = st.number_input("Marks Obtained", min_value=0, max_value=100, step=1)

        if st.button("Add Record"):
            grade = calculate_grade(marks)
            new_entry = {
                "Student Name": name,
                "Subject": subject,
                "Marks": marks,
                "Grade": grade,
                "Evaluation Date": datetime.date.today()
            }
            st.session_state.eval_data = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
            st.success(f"✅ Record Added! Grade: {grade}")

    # 2️⃣ View Records
    elif choice == "View Records":
        st.subheader("📋 All Evaluation Records")
        if df.empty:
            st.info("No evaluation records yet.")
        else:
            st.dataframe(df)

    # 3️⃣ Search Records
    elif choice == "Search Records":
        st.subheader("🔍 Search by Student Name or Subject")
        term = st.text_input("Enter name or subject to search")
        if term:
            results = df[
                df["Student Name"].str.contains(term, case=False) |
                df["Subject"].str.contains(term, case=False)
            ]
            st.dataframe(results if not results.empty else pd.DataFrame(columns=df.columns))

    # 4️⃣ Filter by Grade
    elif choice == "Filter by Grade":
        st.subheader("🎯 Filter Records by Grade")
        grade_options = ["All"] + sorted(df["Grade"].unique().tolist())
        selected_grade = st.selectbox("Select Grade", grade_options)

        filtered_df = df.copy()
        if selected_grade != "All":
            filtered_df = filtered_df[filtered_df["Grade"] == selected_grade]

        if filtered_df.empty:
            st.warning("No records found for selected grade.")
        else:
            st.dataframe(filtered_df)

if __name__ == "__main__":
    main()
