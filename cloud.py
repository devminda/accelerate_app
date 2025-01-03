import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt

from functions import set_background_image, update_data, preprocess_response
from firebase_functions import responses_collection, question_doc




def word_cloud_page():
    st.subheader("Word Cloud Page")
    update_data(responses_collection, question_doc)  # Fetch the latest responses and question
    question = st.session_state["current_question"]
    st.markdown(f'<h1 style="font-size: 40px; text-align: center; color: #f1c40f;">{question}</h1>', unsafe_allow_html=True)

    # User Input Section
    user_input = st.text_input("Your Answer")
    if st.button("Submit"):
        if user_input.strip():
            preprocessed_input = preprocess_response(user_input.strip())
            responses_collection.add({"response": preprocessed_input})
            st.success("Your answer has been added!")
            update_data(responses_collection, question_doc)  # Update responses
        else:
            st.warning("Please enter a valid answer.")

    # Generate Word Cloud
    if st.session_state["responses"]:
        st.subheader("Dynamic Word Cloud")
        text = " ".join(st.session_state["responses"])
        wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)
        fig, ax = plt.subplots()
        ax.imshow(wordcloud, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig)

word_cloud_page()