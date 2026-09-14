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

        safe_content = html.escape(
            content
        ).replace("\n", "<br>")

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

        try:

            with st.spinner(
                "Study Helper is thinking..."
            ):

                response = generate_response(
                    qwen_messages
                )

        except Exception as e:

            st.error(
                f"AI error: {repr(e)}"
            )

            st.exception(e)

            return

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response
            }
        )

        st.rerun()