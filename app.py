import streamlit as st
import database.database as db

# Page configuration
st.set_page_config(
    page_title="Study Helper",
    layout="wide"
)

# Initialize database
db.initialize_database()

# Session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "dashboard"

if "selected_assignment" not in st.session_state:
    st.session_state.selected_assignment = None

# Login page
if not st.session_state.logged_in:

    st.title("Study Helper")

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


# Main application
else:

    # Sidebar
    with st.sidebar:

        st.title("Study Helper")

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
            st.rerun()

        if st.button(
            "AI Assistant",
            use_container_width=True
        ):

            st.session_state.page = "ai"
            st.rerun()

        st.divider()

        if st.button(
            "Logout",
            use_container_width=True
        ):

            st.session_state.clear()
            st.rerun()

    # Dashboard
    if st.session_state.page == "dashboard":

        st.title(
            f"Good to see you, {st.session_state.name}!"
        )

        # Check user permissions
        can_manage_assignments = (
            st.session_state.role
            in ["helper", "leader", "teacher"]
        )

        # Add assignment button
        if can_manage_assignments:

            if st.button(
                "Add Assignment",
                use_container_width=True
            ):

                st.session_state.page = "create_assignment"
                st.rerun()

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
                        f"**Subject:** {subject}"
                    )

                    st.write(
                        f"**Due:** {due_date}"
                    )

                    if description:

                        st.write(description)

                    st.caption(
                        f"Created by: {created_by}"
                    )

                    col1, col2 = st.columns(2)

                    with col1:

                        if st.button(
                            "View Details",
                            key=f"view_{assignment_id}",
                            use_container_width=True
                        ):

                            st.session_state.selected_assignment = assignment_id
                            st.session_state.page = "assignment"

                            st.rerun()

                    with col2:

                        if can_manage_assignments:

                            if st.button(
                                "Delete",
                                key=f"delete_{assignment_id}",
                                use_container_width=True
                            ):

                                st.session_state.delete_assignment = assignment_id
                                st.rerun()

        # Delete confirmation
        if "delete_assignment" in st.session_state:

            assignment_id = st.session_state.delete_assignment

            st.divider()

            st.warning(
                "Are you sure you want to delete this assignment?"
            )

            col1, col2 = st.columns(2)

            with col1:

                if st.button(
                    "Yes, Delete",
                    use_container_width=True
                ):

                    db.delete_assignment(
                        assignment_id
                    )

                    del st.session_state.delete_assignment

                    st.success(
                        "Assignment deleted."
                    )

                    st.rerun()

            with col2:

                if st.button(
                    "Cancel",
                    use_container_width=True
                ):

                    del st.session_state.delete_assignment

                    st.rerun()


    # Create assignment page
    elif st.session_state.page == "create_assignment":

        # Security check
        if st.session_state.role not in [
            "helper",
            "leader",
            "teacher"
        ]:

            st.error(
                "You don't have permission to create assignments."
            )

            if st.button("Back to Dashboard"):

                st.session_state.page = "dashboard"
                st.rerun()

        else:

            st.title("Create Assignment")

            title = st.text_input(
                "Assignment Name"
            )

            subject = st.text_input(
                "Subject"
            )

            description = st.text_area(
                "Description"
            )

            due_date = st.date_input(
                "Submission Date"
            )

            due_time = st.time_input(
                "Submission Time"
            )

            st.divider()

            col1, col2 = st.columns(2)

            with col1:

                if st.button(
                    "Create Assignment",
                    use_container_width=True
                ):

                    if title == "" or subject == "":

                        st.warning(
                            "Please enter an assignment name and subject."
                        )

                    else:

                        due_datetime = (
                            f"{due_date} {due_time}"
                        )

                        db.create_assignment(
                            title=title,
                            subject=subject,
                            description=description,
                            due_date=due_datetime,
                            created_by=st.session_state.student_id
                        )

                        st.success(
                            "Assignment created successfully!"
                        )

                        st.session_state.page = "dashboard"

                        st.rerun()

            with col2:

                if st.button(
                    "Cancel",
                    use_container_width=True
                ):

                    st.session_state.page = "dashboard"
                    st.rerun()


    # Assignment details
    elif st.session_state.page == "assignment":

        assignment_id = st.session_state.selected_assignment

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
                f"### {subject}"
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

            if st.session_state.role in [
                "helper",
                "leader",
                "teacher"
            ]:

                if st.button(
                    "Delete Assignment"
                ):

                    st.session_state.delete_from_details = assignment_id
                    st.rerun()

            if "delete_from_details" in st.session_state:

                st.warning(
                    "Are you sure you want to delete this assignment?"
                )

                col1, col2 = st.columns(2)

                with col1:

                    if st.button(
                        "Yes, Delete",
                        use_container_width=True
                    ):

                        db.delete_assignment(
                            st.session_state.delete_from_details
                        )

                        del st.session_state.delete_from_details

                        st.session_state.page = "dashboard"
                        st.session_state.selected_assignment = None

                        st.rerun()

                with col2:

                    if st.button(
                        "Cancel",
                        use_container_width=True
                    ):

                        del st.session_state.delete_from_details

                        st.rerun()

            if st.button(
                "Back to Dashboard"
            ):

                st.session_state.page = "dashboard"
                st.rerun()

        else:

            st.error(
                "Assignment not found."
            )

            if st.button(
                "Back to Dashboard"
            ):

                st.session_state.page = "dashboard"
                st.rerun()


    # AI page
    elif st.session_state.page == "ai":

        st.title("AI Assistant")

        st.info(
            "GO BACK TO HOMEPAGE NOW NOT DONE BRO"
        )