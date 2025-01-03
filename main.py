import streamlit as st

def main():
    # Initialize session state
    if "responses" not in st.session_state:
        st.session_state["responses"] = []
    if "current_question" not in st.session_state:
        st.session_state["current_question"] = "Loading question..."
    if "quiz_question" not in st.session_state:
        st.session_state["quiz_question"] = "What is your favorite color?"
    if "quiz_answers" not in st.session_state:
        st.session_state["quiz_answers"] = ["Red", "Blue", "Green", "Yellow"]
    # Set up pages
    admin_page = st.Page("admin.py", title="Admin", icon=":material/add_circle:")
    quiz_page = st.Page("quiz.py", title="Quiz", icon=":material/add_circle:")
    cloud_page = st.Page("cloud.py", title="Word Cloud", icon=":material/add_circle:")

    pg = st.navigation([admin_page, quiz_page, cloud_page])
    st.set_page_config(page_title="Accelerate SL teach", page_icon=":material/edit:")
    pg.run()

main()