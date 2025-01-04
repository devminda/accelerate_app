import os
import streamlit as st

from functions import set_background_image, reset_responses
from firebase_functions import question_doc, quiz_doc, poll_doc, responses_collection_cloud, responses_collection_poll



def admin_page():
    # Admin access control (hardcoded admin password)
       
    admin_password = "admin123"  # Hardcoded password for the admin
    entered_password = st.text_input("Enter Admin Password", type="password")

    if entered_password == admin_password:
        st.success("Password Correct! You can now set a new question and quiz.")
        new_question = st.text_input("Set a New Question for Word Cloud")
        if st.button("Update Word Cloud Question"):
            question_doc.set({"question": new_question})
            reset_responses(responses_collection_cloud)  # Clear old responses when updating the question
            st.session_state["responses"] = []  # Clear session state responses
            st.success("Word Cloud question updated successfully!")

        new_poll_question = st.text_input("Set a New Poll Question")
        poll_answers = []
        for i in range(4):
            answer = st.text_input(f"Set Answer {i+1}")
            poll_answers.append(answer)

        if st.button("Update Poll Question and Answers"):
            poll_doc.set({"question": new_poll_question, "answers": poll_answers})
            st.session_state["poll_question"] = new_poll_question
            st.session_state["poll_answers"] = poll_answers
            reset_responses(responses_collection_poll)
            st.success("Poll question and answers updated successfully!")
        
        # Select a question to edit
        question_index = st.selectbox(
            "Select Question to Edit",
            range(5),
            format_func=lambda i: f"Question {i + 1}",
        )

        # Edit selected question
        print( "we are here",st.session_state["quiz_data"])
        selected_question = st.session_state["quiz_data"][f"Question {question_index + 1}"]
        new_question = st.text_input("Edit Question", selected_question["question"])
        option_1 = st.text_input("Option 1", selected_question["options"][0])
        option_2 = st.text_input("Option 2", selected_question["options"][1])
        option_3 = st.text_input("Option 3", selected_question["options"][2])
        option_4 = st.text_input("Option 4", selected_question["options"][3])
        correct_answer = st.selectbox(
            "Select Correct Answer", [option_1, option_2, option_3, option_4]
        )

        if st.button("Update Question"):
            # Update the question data
            quiz_doc.set({f"Question {question_index + 1}":{'question':new_question,'options':[option_1, option_2, option_3, option_4],'correct_answer':correct_answer}}, merge=True)
            # reset_responses(quiz_doc)
            selected_question["question"] = new_question
            selected_question["options"] = [option_1, option_2, option_3, option_4]
            selected_question["correct_answer"] = correct_answer
            

            st.success("Question updated successfully!")
    else:
        st.warning("Incorrect password. You cannot update the questions.")
    

# Set the background image
image_path = os.path.join("images", "image.jpg")  # Specify the path to your image
set_background_image(image_path)
# Run the admin page
admin_page()
