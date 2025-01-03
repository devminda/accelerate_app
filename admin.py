import os
import streamlit as st

from functions import set_background_image, reset_responses
from firebase_functions import question_doc, quiz_doc, responses_collection



def admin_page():
    # Admin access control (hardcoded admin password)
       
    admin_password = "admin123"  # Hardcoded password for the admin
    entered_password = st.text_input("Enter Admin Password", type="password")

    if entered_password == admin_password:
        st.success("Password Correct! You can now set a new question and quiz.")
        new_question = st.text_input("Set a New Question for Word Cloud")
        if st.button("Update Word Cloud Question"):
            question_doc.set({"question": new_question})
            reset_responses(responses_collection)  # Clear old responses when updating the question
            st.session_state["responses"] = []  # Clear session state responses
            st.success("Word Cloud question updated successfully!")

        new_quiz_question = st.text_input("Set a New Quiz Question")
        quiz_answers = []
        for i in range(4):
            answer = st.text_input(f"Set Answer {i+1}")
            quiz_answers.append(answer)

        if st.button("Update Quiz Question and Answers"):
            quiz_doc.set({"question": new_quiz_question, "answers": quiz_answers})
            st.session_state["quiz_question"] = new_quiz_question
            st.session_state["quiz_answers"] = quiz_answers
            st.success("Quiz question and answers updated successfully!")
    else:
        st.warning("Incorrect password. You cannot update the questions.")

# Set the background image
image_path = os.path.join("images", "image.jpg")  # Specify the path to your image
set_background_image(image_path)
# Run the admin page
admin_page()
