import streamlit as st
import database.database as db

st.set_page_config(
    page_title="Study Helper",
    layout="centered"
)

db.initialize_database()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------------- LOGIN ---------------- #

if not st.session_state.logged_in:

    st.title("📚 Study Helper")
    st.markdown("### Login")

    student_id = st.text_input("Student ID")

    if st.button("Login", use_container_width=True):

        user = db.login(student_id)

        if user:
            st.session_state.logged_in = True
            st.session_state.student_id = user[0]
            st.session_state.name = user[1]
            st.session_state.role = user[2]

            st.success(f"Welcome {user[1]}!")
            st.rerun()

        else:
            st.error("Student ID not found.")

    # ---------------- SIGN UP ---------------- #

    with st.expander("Don't have an account? Sign Up"):

        new_id = st.text_input("Student ID", key="signup_id")
        new_name = st.text_input("Full Name", key="signup_name")

        if st.button("Create Account", use_container_width=True):

            if new_id == "" or new_name == "":
                st.warning("Please fill in all fields.")

            elif db.login(new_id):
                st.error("Student ID already exists.")

            else:
                db.add_user(
                    student_id=new_id,
                    name=new_name,
                    role="student"
                )

                st.success("Account created! You can now log in.")

# ---------------- HOME ---------------- #

else:

    st.success(f"Welcome {st.session_state.name}")

    st.write("Role:", st.session_state.role)

    if st.button("Logout"):

        st.session_state.clear()
        st.rerun()