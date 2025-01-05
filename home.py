
import streamlit as st


# Function to render the home page
def home_page():
    
    # Add a welcome message
    st.title(":blue[Welcome to **LearnLab** - Powered by  **Accelerate SL**!]")
    st.markdown(
        """
        This tool is designed to make your learning experience more interactive.

        ### Explore the Features:
        - **Poll**: Dive into the polls to explore user preferences visually.
        - **Quiz**: Test your knowledge with fun and challenging questions.
        - **Word Cloud**: Visualize user responses in an engaging word cloud.
        - **Admin Panel**: Manage content, settings, and more from the admin section.

        Use the navigation menu on the sidebar to move between pages.
        """
    )

    # Add navigation buttons to go to specific pages
    col1, col2, col3,= st.columns(3)
    # _,col4,_ = st.columns(3)

    with col3:
        if st.button("Go to Word Cloud", icon=":material/cloud:"):
            st.switch_page('cloud.py')

    with col2:
        if st.button(" Go to Quiz ", icon=":material/how_to_vote:"):
            st.switch_page("quiz.py")

    with col1:
        if st.button("Go to Poll", icon=":material/quiz:"):
            st.switch_page("poll.py")
    
col1,col2,col3 = st.columns(3, gap='small', vertical_alignment='center')
with col1:
    st.image("./images/learnlablogo-removebg-preview.png", width = 350)
with col2:
    st.image("./images/hub logo.png", width = 250)
with col3:
    st.image("./images/logo.png", width = 150)

# Show the page
home_page()