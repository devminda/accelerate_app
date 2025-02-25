import streamlit as st

from functions import reset_responses
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
        
        selected_question = st.session_state["quiz_data"][f"Question {question_index + 1}"]

        # Check if the question is a code snippet
        is_code = st.checkbox("Is this a code question?", value=selected_question.get("is_code", False))

        # Allow user to input question
        new_question = st.text_area("Edit Question", selected_question["question"])

        # Show language selection only if it's a code snippet
        language = None
        if is_code:
            language = st.selectbox(
                "Select Programming Language",
                ["Python", "JavaScript", "Java", "C++", "Other"],
                index=0 if "language" not in selected_question else 
                ["Python", "JavaScript", "Java", "C++", "Other"].index(selected_question["language"])
            )

        # Options for multiple choice
        option_1 = st.text_input("Option 1", selected_question["options"][0])
        option_2 = st.text_input("Option 2", selected_question["options"][1])
        option_3 = st.text_input("Option 3", selected_question["options"][2])
        option_4 = st.text_input("Option 4", selected_question["options"][3])

        # Correct answer selection
        correct_answer = st.selectbox(
            "Select Correct Answer", [option_1, option_2, option_3, option_4]
        )

        if st.button("Update Question"):
            # Update the question data
            question_data = {
                "question": new_question,
                "options": [option_1, option_2, option_3, option_4],
                "correct_answer": correct_answer,
                "is_code": is_code,
            }
            
            # Add language if it's a code question
            if is_code:
                question_data["language"] = language

            # Save to database (Firestore or another storage system)
            quiz_doc.set({f"Question {question_index + 1}": question_data}, merge=True)

            # Update session state
            selected_question.update(question_data)

            st.success("Question updated successfully!")
    else:
        st.warning("Incorrect password. You cannot update the questions.")
    

# Set the background image

col1,col2,col3 = st.columns(3, gap='small', vertical_alignment='center')
with col1:
    st.image("./images/learnlablogo-removebg-preview.png", width = 350)
with col2:
    st.image("./images/hub logo.png", width = 250)
with col3:
    st.image("./images/logo.png", width = 150)
    


admin_page()
