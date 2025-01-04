import streamlit as st

def main():
    # Initialize session state
    if "responses" not in st.session_state:
        st.session_state["responses"] = []
    if "current_question" not in st.session_state:
        st.session_state["current_question"] = "Loading question..."
    if "poll_question" not in st.session_state:
        st.session_state["poll_question"] = "What is your favorite color?"
    if "poll_answers" not in st.session_state:
        st.session_state["poll_answers"] = ["Red", "Blue", "Green", "Yellow"]
    # Initialize session state for multiple questions
    if "quiz_data" not in st.session_state:
        st.session_state["quiz_data"] = {
            "Question 1": {
                "question": "What is the capital of France?",
                "options": ["Paris", "London", "Berlin", "Rome"],
                "correct_answer": "Paris",
            },
            "Question 2":{
                "question": "What is 2 + 2?",
                "options": ["3", "4", "5", "6"],
                "correct_answer": "4",
            },
            "Question 3":{
                "question": "Which planet is known as the Red Planet?",
                "options": ["Earth", "Mars", "Jupiter", "Venus"],
                "correct_answer": "Mars",
            },
        }

    # Set up pages
    admin_page = st.Page("admin.py", title="Admin", icon=":material/home:")
    poll_page = st.Page("poll.py", title="Poll", icon=":material/home:")
    quiz_page = st.Page("quiz.py", title="Quiz", icon=":material/help:")
    cloud_page = st.Page("cloud.py", title="Word Cloud", icon=":material/cloud:")

    pg = st.navigation([admin_page, poll_page, quiz_page, cloud_page])
    st.set_page_config(page_title="Accelerate SL teach", page_icon=":material/edit:")
    pg.run()

main()