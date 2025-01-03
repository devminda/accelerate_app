
import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import toml


# Load Firebase credentials from Streamlit secrets
toml_file_path = ".streamlit/secrets.toml"
toml_data = toml.load(toml_file_path)
firebase_credentials = toml_data['firebase_credentials']

# Firebase setup
if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_credentials)
    firebase_admin.initialize_app(cred)

db = firestore.client()
question_doc = db.collection("app_data").document("current_question")
quiz_doc = db.collection("app_data").document("quiz_data")
responses_collection = db.collection("responses")

