import html
import streamlit as st
import database.database as db

st.set_page_config(
    page_title="Study Helper",
    layout="wide"
)

db.initialize_database()


def ai_page():
    from ai.model import generate_response

    st.markdown(
        """
        <style>

        .stApp {
            background-color: #343541;
        }

        section[data-testid="stSidebar"] {
            background-color: #202123;
        }

        section[data-testid="stSidebar"] * {
            color: white;
        }

        .chat-message {
            padding: 20px;
            border-radius: 5px;
            margin-bottom: 10px;
            color: white;
        }

        .user-message {
            background-color: #343541;
        }

        .assistant-message {
            background-color: #444654;
        }

        .chat-name {
            font-weight: bold;
            margin-bottom: 8px;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("Study Helper")
    st.caption("AI Study Assistant")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:

        role = message["role"]
        content = message["content"]

        if role == "user":
            name = "You"
            css_class = "user-message"
        else:
            name = "Study Helper"
            css_class = "assistant-message"

        safe_content = html.escape(content).replace(
            "\n",
            "<br>"
        )

        st.markdown(
            f"""
            <div class="chat-message {css_class}">
                <div class="chat-name">{name}</div>
                <div>{safe_content}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    user_input = st.chat_input(
        "Message Study Helper..."
    )

    if user_input:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_input
            }
        )

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

        qwen_messages = [
            {
                "role": "system",
                "content": system_prompt
            }
        ]

        for message in st.session_state.messages:

            qwen_messages.append(
                {
                    "role": message["role"],
                    "content": message["content"]
                }
            )

        with st.spinner(
            "Study Helper is thinking..."
        ):

            try:

                response = generate_response(
                    qwen_messages
                )

            except Exception as e:

                st.error(
                    f"AI error: {e}"
                )

                return

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response
            }
        )

        st.rerun()


def dashboard_page():

    st.title("Dashboard")

    st.write(
        f"Welcome, {st.session_state.user[1]}"
    )

    st.divider()

    assignments = db.get_assignments()

    if not assignments:

        st.info(
            "No assignments yet."
        )

    else:

        for assignment in assignments:

            assignment_id = assignment[0]
            title = assignment[1]
            subject = assignment[2]
            description = assignment[3]
            due_date = assignment[4]

            with st.container(border=True):

                st.subheader(title)

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

                if st.button(
                    "View Assignment",
                    key=f"view_{assignment_id}"
                ):

                    st.session_state.selected_assignment = (
                        assignment_id
                    )

                    st.session_state.page = (
                        "assignment"
                    )

                    st.rerun()


def create_assignment_page():

    st.title("Create Assignment")

    title = st.text_input(
        "Assignment Title"
    )

    subject = st.text_input(
        "Subject"
    )

    description = st.text_area(
        "Description"
    )

    due_date = st.date_input(
        "Due Date"
    )

    if st.button(
        "Create Assignment"
    ):

        if not title or not subject:

            st.error(
                "Please enter a title and subject."
            )

            return

        db.create_assignment(
            title,
            subject,
            description,
            due_date,
            st.session_state.user[0]
        )

        st.success(
            "Assignment created successfully."
        )

        st.session_state.page = "dashboard"

        st.rerun()


def assignment_page():

    assignment_id = (
        st.session_state.selected_assignment
    )

    assignment = db.get_assignment(
        assignment_id
    )

    if not assignment:

        st.error(
            "Assignment not found."
        )

        return

    st.title(
        assignment[1]
    )

    st.write(
        f"**Subject:** {assignment[2]}"
    )

    st.write(
        f"**Due:** {assignment[4]}"
    )

    st.divider()

    if assignment[3]:

        st.write(
            assignment[3]
        )

    st.divider()

    role = st.session_state.user[2]

    if role in [
        "Helper",
        "Leader",
        "Teacher"
    ]:

        if st.button(
            "Delete Assignment",
            type="secondary"
        ):

            db.delete_assignment(
                assignment_id
            )

            st.session_state.page = (
                "dashboard"
            )

            st.rerun()

    if st.button(
        "Back to Dashboard"
    ):

        st.session_state.page = (
            "dashboard"
        )

        st.rerun()


def login_page():

    st.title("Study Helper")

    st.subheader("Login")

    student_id = st.text_input(
        "Student ID"
    )

    if st.button(
        "Login"
    ):

        if not student_id:

            st.error(
                "Please enter your student ID."
            )

            return

        user = db.login(
            student_id
        )

        if user:

            st.session_state.logged_in = True

            st.session_state.user = user

            st.session_state.page = (
                "dashboard"
            )

            st.rerun()

        else:

            st.error(
                "Student ID not found."
            )

    st.divider()

    st.subheader(
        "Don't have an account?"
    )

    if st.button(
        "Sign Up"
    ):

        st.session_state.auth_page = (
            "signup"
        )

        st.rerun()


def signup_page():

    st.title("Study Helper")

    st.subheader("Sign Up")

    student_id = st.text_input(
        "Student ID"
    )

    name = st.text_input(
        "Name"
    )

    role = st.selectbox(
        "Role",
        [
            "Student",
            "Teacher",
            "Leader",
            "Helper"
        ]
    )

    if st.button(
        "Create Account"
    ):

        if not student_id or not name:

            st.error(
                "Please fill in all fields."
            )

            return

        success = db.add_user(
            student_id,
            name,
            role
        )

        if success:

            st.success(
                "Account created successfully."
            )

            st.session_state.auth_page = (
                "login"
            )

            st.rerun()

        else:

            st.error(
                "Student ID already exists."
            )

    if st.button(
        "Back to Login"
    ):

        st.session_state.auth_page = (
            "login"
        )

        st.rerun()


# Initialize session state

if "logged_in" not in st.session_state:

    st.session_state.logged_in = False


if "user" not in st.session_state:

    st.session_state.user = None


if "auth_page" not in st.session_state:

    st.session_state.auth_page = "login"


if "page" not in st.session_state:

    st.session_state.page = "dashboard"


if "messages" not in st.session_state:

    st.session_state.messages = []


# Authentication

if not st.session_state.logged_in:

    if st.session_state.auth_page == "signup":

        signup_page()

    else:

        login_page()

    st.stop()


# Sidebar

with st.sidebar:

    st.title("Study Helper")

    st.write(
        f"**{st.session_state.user[1]}**"
    )

    st.write(
        st.session_state.user[2]
    )

    st.divider()

    if st.button(
        "Dashboard",
        use_container_width=True
    ):

        st.session_state.page = (
            "dashboard"
        )

        st.rerun()

    if st.button(
        "AI Assistant",
        use_container_width=True
    ):

        st.session_state.page = (
            "ai"
        )

        st.rerun()

    role = st.session_state.user[2]

    if role in [
        "Helper",
        "Leader",
        "Teacher"
    ]:

        if st.button(
            "New Assignment",
            use_container_width=True
        ):

            st.session_state.page = (
                "create"
            )

            st.rerun()

    st.divider()

    if st.button(
        "New Study Session",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.session_state.page = (
            "ai"
        )

        st.rerun()

    if st.button(
        "Logout",
        use_container_width=True
    ):

        st.session_state.logged_in = False

        st.session_state.user = None

        st.session_state.page = (
            "dashboard"
        )

        st.session_state.auth_page = (
            "login"
        )

        st.session_state.messages = []

        st.rerun()


# Page routing

if st.session_state.page == "dashboard":

    dashboard_page()

elif st.session_state.page == "ai":

    ai_page()

elif st.session_state.page == "create":

    create_assignment_page()

elif st.session_state.page == "assignment":

    assignment_page()