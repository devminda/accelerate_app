import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore
import toml

# Load Firebase credentials from Streamlit secrets
firebase_credentials = st.secrets["firebase_credentials"]
toml_data = toml.load(firebase_credentials)

# Convert the secret string to a dictionary
# cred_dict = json.loads(firebase_credentials)

import base64

# Firebase setup
if not firebase_admin._apps:
    cred = credentials.Certificate(toml_data)
    firebase_admin.initialize_app(cred)

db = firestore.client()
question_doc = db.collection("app_data").document("current_question")
responses_collection = db.collection("responses")

# Initialize session state
if "responses" not in st.session_state:
    st.session_state["responses"] = []

if "current_question" not in st.session_state:
    st.session_state["current_question"] = "Loading question..."

# Function to fetch responses from Firestore
def fetch_responses():
    docs = responses_collection.stream()
    return [doc.to_dict()["response"] for doc in docs]

# Function to fetch the current question from Firestore
def fetch_current_question():
    question_data = question_doc.get()
    if question_data.exists:
        return question_data.to_dict().get("question", "No question set.")
    return "No question set."

# Function to reset responses in Firestore
def reset_responses():
    docs = responses_collection.stream()
    for doc in docs:
        doc.reference.delete()

# Fetch the current question and responses
def update_data():
    st.session_state["responses"] = fetch_responses()  # Fetch new responses
    st.session_state["current_question"] = fetch_current_question()  # Fetch current question

# Replace specific phrases with a single token (e.g., "not sure" becomes "not_sure")
def preprocess_response(response):
    # Replace "not sure" with a single token
    response = response.replace("not sure", "not_sure")
    return response

# Admin Controls
st.sidebar.title("Admin Controls")
admin_password = "admin123"  # Hardcoded password for the admin

# Password input for admin mode
entered_password = st.sidebar.text_input("Enter Admin Password", type="password")

if entered_password == admin_password:
    st.sidebar.success("Password Correct! You can now set a new question.")
    new_question = st.sidebar.text_input("Set a New Question")
    if st.sidebar.button("Update Question"):
        question_doc.set({"question": new_question})
        reset_responses()  # Clear old responses when updating the question
        st.session_state["responses"] = []  # Clear session state responses
        st.success("Question updated successfully! Word cloud reset.")
else:
    st.sidebar.warning("Incorrect password. You cannot update the question.")

# Background image URL (change to an actual URL or a file path)
with open(r'C:\Users\Devminda\OneDrive\Documents\Projects\Global shapers\Projects\Finance project\app\pexels-jessbaileydesign-743986.jpg', "rb") as image_file:
    background_image_url = base64.b64encode(image_file.read()).decode()

# CSS to set the background image
background_image_css = f"""
    <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{background_image_url}");
            background-size: cover;
            background-position: center center;
            background-repeat: no-repeat;
            height: 100vh;
        }}
    </style>
"""

# Inject the CSS into the Streamlit app
st.markdown(background_image_css, unsafe_allow_html=True)

# set_png_as_page_bg(r'C:\Users\Devminda\OneDrive\Documents\Projects\Global shapers\Projects\Finance project\app\pexels-jessbaileydesign-743986.jpg')

# Display the current question
st.title("Interactive Word Cloud App")
st.header("Current Question")
update_data()  # Fetch the latest data for the question and responses
question = st.session_state["current_question"]
st.markdown(f'<h1 style="font-size: 40px; text-align: center; color: #f1c40f;">{question}</h1>', unsafe_allow_html=True)

# User Input Section
st.subheader("Submit Your Answer")
user_input = st.text_input("Your Answer")
if st.button("Submit"):
    if user_input.strip():
        # Preprocess the response to replace "not sure" with "not_sure"
        preprocessed_input = preprocess_response(user_input.strip())
        responses_collection.add({"response": preprocessed_input})
        st.success("Your answer has been added!")
    else:
        st.warning("Please enter a valid answer.")

# Generate Word Cloud
if st.session_state["responses"]:
    st.subheader("Dynamic Word Cloud")
    
    # Combine all responses into one text
    text = " ".join(st.session_state["responses"])
    
    # Generate the word cloud
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)
    
    # Display the word cloud
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)

# Display all responses
if st.session_state["responses"]:
    st.subheader("All User Responses")
    st.write(pd.DataFrame(st.session_state["responses"], columns=["Responses"]))
