import streamlit as st
import database.database as db

# Page configuration
st.set_page_config(
    page_title="Study Helper",
    page_icon="📚",
    layout="wide"
)

# Initialize database
db.initialize_database()

# Session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "dashboard"

# Login page
if not st.session_state.logged_in:

    st.title("📚 Study Helper")

    st.markdown("### Login")

    student_id = st.text_input(
        "Student ID"
    )

    if st.button(
        "Login",
        use_container_width=True
    ):

        user = db.login(student_id)

        if user:

            st.session_state.logged_in = True
            st.session_state.student_id = user[0]
            st.session_state.name = user[1]
            st.session_state.role = user[2]

            st.rerun()

        else:

            st.error("Student ID not found.")

    # Sign up
    with st.expander("Don't have an account? Sign Up"):

        new_id = st.text_input(
            "Student ID",
            key="signup_id"
        )

        new_name = st.text_input(
            "Full Name",
            key="signup_name"
        )

        role = st.selectbox(
            "Role",
            [
                "Student",
                "Helper",
                "Leader",
                "Teacher"
            ],
            key="signup_role"
        )

        if st.button(
            "Create Account",
            use_container_width=True
        ):

            if new_id == "" or new_name == "":

                st.warning(
                    "Please fill in all fields."
                )

            elif db.login(new_id):

                st.error(
                    "Student ID already exists."
                )

            else:

                db.add_user(
                    student_id=new_id,
                    name=new_name,
                    role=role.lower()
                )

                st.success(
                    "Account created! You can now log in."
                )


# Dashboard
else:

    # Sidebar
    with st.sidebar:

        st.title("📚 Study Helper")

        st.divider()

        st.write(
            f"**{st.session_state.name}**"
        )

        st.caption(
            f"Role: {st.session_state.role.capitalize()}"
        )

        st.divider()

        if st.button(
            "Dashboard",
            use_container_width=True
        ):

            st.session_state.page = "dashboard"

        if st.button(
            "AI Assistant",
            use_container_width=True
        ):

            st.session_state.page = "ai"

        st.divider()

        if st.button(
            "Logout",
            use_container_width=True
        ):

            st.session_state.clear()
            st.rerun()

    # Dashboard page
    if st.session_state.page == "dashboard":

        st.title(
            f"How's it going, {st.session_state.name}?"
        )

        st.markdown("### Your Assignments")

        # Get assignments
        assignments = db.get_assignments()

        # No assignments
        if not assignments:

            st.info(
                "There are currently no assignments."
            )

        # Display assignments
        else:

            for assignment in assignments:

                assignment_id = assignment[0]
                title = assignment[1]
                subject = assignment[2]
                description = assignment[3]
                due_date = assignment[4]
                created_by = assignment[5]

                with st.container(border=True):

                    st.subheader(title)

                    st.write(
                        f"📘 **Subject:** {subject}"
                    )

                    st.write(
                        f"📅 **Due:** {due_date}"
                    )

                    if description:

                        st.write(description)

                    st.caption(
                        f"Created by: {created_by}"
                    )

                    if st.button(
                        "View Details",
                        key=f"assignment_{assignment_id}"
                    ):

                        st.session_state.selected_assignment = assignment_id
                        st.session_state.page = "assignment"

                        st.rerun()

    # AI page
    elif st.session_state.page == "ai":

        st.title("AI Assistant")

        st.info(
            "The AI Assistant will be added here later."
        )

    # Assignment details page
    elif st.session_state.page == "assignment":

        assignment_id = st.session_state.get(
            "selected_assignment"
        )

        assignment = db.get_assignment(
            assignment_id
        )

        if assignment:

            assignment_id = assignment[0]
            title = assignment[1]
            subject = assignment[2]
            description = assignment[3]
            due_date = assignment[4]
            created_by = assignment[5]

            st.title(title)

            st.write(
                f"### 📘 {subject}"
            )

            st.write(
                f"**Due:** {due_date}"
            )

            st.write(
                f"**Created by:** {created_by}"
            )

            st.divider()

            st.subheader("Description")

            if description:

                st.write(description)

            else:

                st.write(
                    "No description provided."
                )

            st.divider()

            if st.button("← Back to Dashboard"):

                st.session_state.page = "dashboard"

                st.rerun()

        else:

            st.error(
                "Assignment not found."
            )

            if st.button("← Back to Dashboard"):

                st.session_state.page = "dashboard"

                st.rerun()