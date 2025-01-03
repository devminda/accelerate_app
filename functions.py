import os
import base64
import streamlit as st

def set_background_image(image_path):
    # Load image and convert it to base64
    with open(image_path, "rb") as image_file:
        img_base64 = base64.b64encode(image_file.read()).decode()
    
    # Inject CSS for background image
    background_css = f"""
    <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{img_base64}");
            background-size: cover;
            background-position: center center;
            background-repeat: no-repeat;
            height: 100vh;
        }}
    </style>
    """
    st.markdown(background_css, unsafe_allow_html=True)



# Function to reset responses in Firestore
def reset_responses(responses_collection):
    docs = responses_collection.stream()
    for doc in docs:
        doc.reference.delete()

# Function to fetch responses from Firestore
def fetch_responses(responses_collection):
    docs = responses_collection.stream()
    return [doc.to_dict()["response"] for doc in docs]

# Function to fetch the current question from Firestore
def fetch_current_question(question_doc):
    question_data = question_doc.get()
    if question_data.exists:
        return question_data.to_dict().get("question", "No question set.")
    return "No question set."

# Function to fetch the quiz question and answers
def fetch_quiz_data(quiz_doc):
    quiz_data = quiz_doc.get()
    if quiz_data.exists:
        quiz = quiz_data.to_dict()
        return quiz.get("question", "What is your favorite color?"), quiz.get("answers", ["Red", "Blue", "Green", "Yellow"])
    return "What is your favorite color?", ["Red", "Blue", "Green", "Yellow"]

# Fetch the current question and responses
def update_data(response_collection, question_doc):
    st.session_state["responses"] = fetch_responses(response_collection)  # Fetch new responses
    st.session_state["current_question"] = fetch_current_question(question_doc)  # Fetch current question
    # st.session_state["quiz_question"], st.session_state["quiz_answers"] = fetch_quiz_data()  # Fetch quiz question and answers

# Preprocess response function
def preprocess_response(response):
    response = response.replace("not sure", "not_sure")
    return response
