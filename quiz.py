import streamlit as st
from firebase_functions import quiz_doc

def quiz_page():

    st.title("Multi-Question Quiz")
    
    user_answers = {}
    quiz_data = quiz_doc.get()
    if quiz_data.exists:
        quiz = quiz_data.to_dict()
        if len(quiz) > 0:
            for key, val in quiz.items():
                st.session_state["quiz_data"][key] = val

    for i, quiz in st.session_state["quiz_data"].items():
        st.subheader(f"{i}")
        
        # Check if the question is a code snippet
        if quiz.get("is_code", False):
            st.code(quiz["question"], language=quiz.get("language", "python"))
        else:
            st.write(quiz["question"])
        
        user_answers[i] = st.radio(f"Your Answer for {i}", quiz["options"], key=f"{i}")

    if st.button("Submit Answers"):
        st.subheader("Results")
        for i, quiz in st.session_state["quiz_data"].items():
            if user_answers[i] == quiz["correct_answer"]:
                st.success(f"{i}: Correct! 🎉")
            else:
                st.error(f"{i}: Wrong! The correct answer is {quiz['correct_answer']}.")

quiz_page()