import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE-API-KEY"))

model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def generate_learning_content(user_input, user_profile):
    prompt = f"""
    Based on the user's profile: {user_profile}, generate a comprehensive learning path for the topic: {user_input}.
    Please include:
    1. A detailed lesson plan that explains the concept fully, with examples and illustrations.
    2. A set of 5 quiz questions based on the lesson, each with multiple-choice options and fully explained answers.
    """
    response = chat.send_message(prompt)
    return response.text

def run():
    st.header("Personalized Learning Companion")

    if 'user_profile' not in st.session_state:
        st.session_state['user_profile'] = {}

    name = st.text_input("What's your name?", key="name_input")
    if name:
        st.session_state['user_profile']['name'] = name

    learning_goal = st.text_input("What do you want to learn today?", key="goal_input")
    submit = st.button("Generate Learning Path")

    if submit and learning_goal:
        user_profile = st.session_state['user_profile']
        learning_content = generate_learning_content(learning_goal, user_profile)
        
        if learning_content:
            st.write("Here's your personalized learning content:")
            st.write(learning_content)
        else:
            st.error("Sorry, we couldn't generate a proper response. Please try again.")

        
        st.session_state['user_profile']['learning_goal'] = learning_goal
        st.session_state['user_profile']['learning_content'] = learning_content
