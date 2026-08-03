import streamlit as st

import database.database as db

st.set_page_config(
    page_title="Study Helper",
    layout="centered"
)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:

    st.title("Study Helper")

    st.markdown("### Login")

    student_id = st.text_input(
        "Student ID"
    )

    if st.button("Login"):

        user = db.login(student_id)

        if user:

            st.session_state.logged_in = True

            st.session_state.student_id = user[0]
            st.session_state.name = user[1]
            st.session_state.role = user[2]

            st.success("Login Successful!")

            st.rerun()

        else:

            st.error("Student ID not found.")

else:

    st.success(f"Welcome {st.session_state.name}")

    st.write("Role:", st.session_state.role)

    if st.button("Logout"):

        st.session_state.clear()

        st.rerun()