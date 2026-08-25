import html
import streamlit as st
import database.database as db


# Page configuration
st.set_page_config(
    page_title="Study Helper",
    layout="wide"
)


# AI page
def ai_page():
    # Initialize chat history
    if "messages" not in st.session_state:

        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Hello! I'm your Study Helper. What subject or topic are we working on today?"
            }
        ]

    # AI page styling
    st.markdown(
        """
        <style>

        .stApp {
            background-color: #343541;
            color: #ececf1;
        }

        #MainMenu {
            visibility: hidden;
        }

        footer {
            visibility: hidden;
        }

        header {
            visibility: hidden;
        }

        section[data-testid="stSidebar"] {
            background-color: #202123;
        }

        .study-header {
            text-align: center;
            padding: 15px;
            font-size: 18px;
            font-weight: 600;
            color: #d1d5db;
            border-bottom: 1px solid rgba(0,0,0,0.1);
        }

        .message {
            display: flex;
            justify-content: center;
            padding: 24px 20px;
        }

        .message-ai {
            background-color: #444654;
        }

        .message-inner {
            width: 100%;
            max-width: 800px;
            display: flex;
            gap: 20px;
        }

        .avatar {
            width: 30px;
            height: 30px;
            min-width: 30px;
            border-radius: 4px;

            display: flex;
            align-items: center;
            justify-content: center;

            font-weight: bold;
            font-size: 14px;

            color: white;
        }

        .avatar-ai {
            background-color: #5436DA;
        }

        .avatar-user {
            background-color: #10a37f;
        }

        .message-content {
            flex: 1;
            line-height: 1.6;
            font-size: 16px;
            color: #ececf1;
            white-space: pre-wrap;
            overflow-wrap: anywhere;
        }

        div[data-testid="stChatInput"] {
            background-color: #40414F;
            border-radius: 12px;
            border: 1px solid rgba(32,33,35,0.5);
        }

        div[data-testid="stChatInput"] textarea {
            color: white;
        }

        div[data-testid="stSpinner"] {
            color: #ececf1;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

    # Header
    st.markdown(
        '<div class="study-header">Study Helper</div>',
        unsafe_allow_html=True
    )

    # Display chat messages
    for message in st.session_state.messages:

        safe_content = html.escape(
            message["content"]
        )

        if message["role"] == "assistant":

            st.markdown(
                f"""
                <div class="message message-ai">
                    <div class="message-inner">

                        <div class="avatar avatar-ai">
                            SH
                        </div>

                        <div class="message-content">
                            {safe_content}
                        </div>

                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                f"""
                <div class="message">
                    <div class="message-inner">

                        <div class="avatar avatar-user">
                            U
                        </div>

                        <div class="message-content">
                            {safe_content}
                        </div>

                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    # Chat input
    prompt = st.chat_input(
        "Message Study Helper..."
    )

    if prompt:

        # Add user message
        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        # System prompt
        system_prompt = """
You are Study Helper, an AI study assistant.

Your job is to help students understand their school subjects.

Explain concepts clearly and step-by-step.

When a student is struggling, break the problem into smaller parts.

Use examples when they are useful.

Do not unnecessarily give the answer to a homework question without explaining how to solve it.

Adapt your explanation to the student's level.

Be friendly, helpful, and concise.

If the student asks a simple question, give a simple answer.

If the student asks for a detailed explanation, provide a detailed explanation.
"""

        # Build conversation
        gemma_messages = [
            {
                "role": "system",
                "content": system_prompt
            }
        ]

        # Add conversation history
        for message in st.session_state.messages:

            gemma_messages.append(
                {
                    "role": message["role"],
                    "content": message["content"]
                }
            )

        # Generate response
        with st.spinner(
            "Study Helper is thinking..."
        ):

            try:

                response = generate_response(
                    gemma_messages
                )

            except Exception as e:

                st.error(
                    f"AI error: {e}"
                )

                return

        # Save response
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response
            }
        )

        st.rerun()


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

        user = db.login(
            student_id
        )

        if user:

            st.session_state.logged_in = True
            st.session_state.student_id = user[0]
            st.session_state.name = user[1]
            st.session_state.role = user[2]

            st.rerun()

        else:

            st.error(
                "Student ID not found."
            )


    # Sign up
    with st.expander(
        "Don't have an account? Sign Up"
    ):

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

            if new_id.strip() == "" or new_name.strip() == "":

                st.warning(
                    "Please fill in all fields."
                )

            elif db.login(new_id):

                st.error(
                    "Student ID already exists."
                )

            else:

                db.add_user(
                    student_id=new_id.strip(),
                    name=new_name.strip(),
                    role=role.lower()
                )

                st.success(
                    "Account created! You can now log in."
                )


# Main application
else:

    # Sidebar
    with st.sidebar:

        st.title(
            "Study Helper"
        )

        st.divider()

        st.write(
            f"**{st.session_state.name}**"
        )

        st.caption(
            f"Role: {st.session_state.role.capitalize()}"
        )

        st.divider()


        # Dashboard button
        if st.button(
            "Dashboard",
            use_container_width=True
        ):

            st.session_state.page = "dashboard"

            st.rerun()


        # AI Assistant button
        if st.button(
            "AI Assistant",
            use_container_width=True
        ):

            st.session_state.page = "ai"

            st.rerun()


        # New study session
        if st.session_state.page == "ai":

            st.divider()

            if st.button(
                "＋  New study session",
                use_container_width=True
            ):

                st.session_state.messages = [
                    {
                        "role": "assistant",
                        "content": "Hello! I'm your Study Helper. What subject or topic are we working on today?"
                    }
                ]

                st.rerun()


        st.divider()


        # Logout
        if st.button(
            "Logout",
            use_container_width=True
        ):

            st.session_state.clear()

            st.rerun()


    # AI page
    if st.session_state.page == "ai":

        ai_page()


    # Dashboard
    elif st.session_state.page == "dashboard":

        st.title(
            f"Good to see you, {st.session_state.name}!"
        )

        # Permissions
        can_manage_assignments = (
            st.session_state.role
            in [
                "helper",
                "leader",
                "teacher"
            ]
        )


        # Add assignment
        if can_manage_assignments:

            if st.button(
                "Add Assignment",
                use_container_width=True
            ):

                st.session_state.page = "create_assignment"

                st.rerun()


        st.markdown(
            "### Your Assignments"
        )


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


                with st.container(
                    border=True
                ):

                    st.subheader(
                        title
                    )

                    st.write(
                        f"**Subject:** {subject}"
                    )

                    st.write(
                        f"**Due:** {due_date}"
                    )

                    if description:

                        st.write(
                            description
                        )

                    st.caption(
                        f"Created by: {created_by}"
                    )


                    col1, col2 = st.columns(2)


                    # View details
                    with col1:

                        if st.button(
                            "View Details",
                            key=f"view_{assignment_id}",
                            use_container_width=True
                        ):

                            st.session_state.selected_assignment = assignment_id

                            st.session_state.page = "assignment"

                            st.rerun()


                    # Delete
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

            assignment_id = (
                st.session_state.delete_assignment
            )

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

            if st.button(
                "Back to Dashboard"
            ):

                st.session_state.page = "dashboard"

                st.rerun()


        else:

            st.title(
                "Create Assignment"
            )


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

                    if title.strip() == "" or subject.strip() == "":

                        st.warning(
                            "Please enter an assignment name and subject."
                        )

                    else:

                        due_datetime = (
                            f"{due_date} {due_time}"
                        )

                        db.create_assignment(
                            title=title.strip(),
                            subject=subject.strip(),
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

        assignment_id = (
            st.session_state.selected_assignment
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


            st.title(
                title
            )

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


            st.subheader(
                "Description"
            )


            if description:

                st.write(
                    description
                )

            else:

                st.write(
                    "No description provided."
                )


            st.divider()


            # Delete assignment
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


            # Delete confirmation
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


            # Back
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