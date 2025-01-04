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
            "Question 4": {
                "question": "What is the largest mammal in the world?",
                "options": ["Elephant", "Blue Whale", "Giraffe", "Hippopotamus"],
                "correct_answer": "Blue Whale",
            },
            "Question 5": {
                "question": "Which element has the chemical symbol 'O'?",
                "options": ["Oxygen", "Gold", "Silver", "Hydrogen"],
                "correct_answer": "Oxygen"
            },
        
        }

    # Set up pages
    main_page = st.Page("home.py", title="Home", icon=":material/home:")
    poll_page = st.Page("poll.py", title="Poll", icon=":material/how_to_vote:")
    quiz_page = st.Page("quiz.py", title="Quiz", icon=":material/quiz:")
    cloud_page = st.Page("cloud.py", title="Word Cloud", icon=":material/cloud:")
    admin_page = st.Page("admin.py", title="Admin", icon=":material/settings:")

    pg = st.navigation([main_page, poll_page, quiz_page, cloud_page, admin_page])
    st.set_page_config(page_title="Accelerate SL teach", page_icon=":material/cast_for_education:")
    pg.run()

main()