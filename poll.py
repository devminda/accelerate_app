# Quiz Page - Display quiz and dynamic bar graph
import os
import streamlit as st
import matplotlib.pyplot as plt

from functions import set_background_image, fetch_responses, fetch_quiz_data
from firebase_functions import responses_collection_poll, poll_doc


def poll_page():
    st.subheader("Poll Page")    
    
    st.session_state["poll_question"], st.session_state["poll_answers"] = fetch_quiz_data(poll_doc)

    poll_question = st.session_state["poll_question"]
    choices = st.session_state["poll_answers"]

    # Allow user to choose an answer
    user_answer = st.radio(poll_question, choices)

    if st.button("Submit Poll Answer"):
        if user_answer:
            responses_collection_poll.add({"response": user_answer})
            st.success(f"Your answer '{user_answer}' has been recorded!")

    # Display dynamic bar graph for quiz responses
    responses = fetch_responses(responses_collection_poll)
    answers_count = {choice: responses.count(choice) for choice in choices}

    fig, ax = plt.subplots()
    ax.bar(answers_count.keys(), answers_count.values(), color=['red', 'blue', 'green', 'yellow'])
    ax.set_xlabel("Answers")
    ax.set_ylabel("Count")
    ax.set_title("Poll Answer Distribution")
    st.pyplot(fig)

# Set the background image
image_path = os.path.join("images", "cloudhd.jpeg")  # Specify the path to your image
set_background_image(image_path)

poll_page()