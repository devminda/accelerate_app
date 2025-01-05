# Quiz Page - Display quiz and dynamic bar graph
import os
import streamlit as st
import matplotlib.pyplot as plt

from functions import fetch_responses, fetch_quiz_data
from firebase_functions import responses_collection_poll, poll_doc


def poll_page():
    
    st.title("Polling Station")   
    
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

    # Display bar chart
    fig1, ax1 = plt.subplots(figsize=(8, 6))
    ax1.bar(
        answers_count.keys(),
        answers_count.values(),
        color=['lightcoral', 'lightblue', 'lightgreen', 'lightyellow'],
        edgecolor='gray',
        linewidth=1.2
    )
    ax1.set_xlabel("Answers", fontsize=14)
    ax1.set_ylabel("Count", fontsize=14)
    ax1.set_title("Poll Answer Distribution", fontsize=16, fontweight='bold', color='darkblue')
    ax1.set_xticks(range(len(answers_count)))
    ax1.set_xticklabels(answers_count.keys(), rotation=45, ha='right', fontsize=12)
    # st.pyplot(fig1)

    # Display bubble chart
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    x = range(len(answers_count))
    y = [1] * len(answers_count)
    bubble_sizes = [v * 200 for v in answers_count.values()]  # Scale bubble size

    ax2.scatter(
        x, y,
        s=bubble_sizes,
        color=['lightcoral', 'lightblue', 'lightgreen', 'lightyellow'],
        alpha=0.6,
        edgecolor='black'
    )
    ax2.set_xticks(x)
    ax2.set_xticklabels(answers_count.keys(), rotation=45, fontsize=12)
    ax2.set_yticks([])
    ax2.set_title("Bubble Chart: Answer Popularity", fontsize=16, fontweight='bold')
    # Display the plots side-by-side
    col1, col2 = st.columns(2)

    with col1:
        st.pyplot(fig1)

    with col2:
        st.pyplot(fig2)

poll_page()