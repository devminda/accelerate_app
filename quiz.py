# Quiz Page - Display quiz and dynamic bar graph
import streamlit as st
import matplotlib.pyplot as plt

from functions import set_background_image, fetch_responses, fetch_quiz_data
from firebase_functions import responses_collection, quiz_doc


def quiz_page():
    st.subheader("Quiz Page")
    
    fetch_quiz_data(quiz_doc)
    
    quiz_question = st.session_state["quiz_question"]
    choices = st.session_state["quiz_answers"]

    # Allow user to choose an answer
    user_answer = st.radio(quiz_question, choices)

    if st.button("Submit Quiz Answer"):
        if user_answer:
            responses_collection.add({"response": user_answer})
            st.success(f"Your answer '{user_answer}' has been recorded!")

    # Display dynamic bar graph for quiz responses
    responses = fetch_responses(responses_collection)
    answers_count = {choice: responses.count(choice) for choice in choices}

    fig, ax = plt.subplots()
    ax.bar(answers_count.keys(), answers_count.values(), color=['red', 'blue', 'green', 'yellow'])
    ax.set_xlabel("Answers")
    ax.set_ylabel("Count")
    ax.set_title("Quiz Answer Distribution")
    st.pyplot(fig)

quiz_page()