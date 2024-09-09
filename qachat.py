import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GOOGLE-API-KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-pro")

def get_gemini_response(context):
    chat = model.start_chat(history=[])
    response = chat.send_message(context, stream=True)
    return response

def run_Chat():
    st.header("Q&A Application")

    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []
    if 'conversation_context' not in st.session_state:
        st.session_state['conversation_context'] = ""

    input_text = st.text_input("Ask your question:", key="input")
    submit = st.button("Submit")

    chat_placeholder = st.container()

    if submit and input_text:
        st.session_state['conversation_context'] += f"User: {input_text}\n"
        context = st.session_state['conversation_context'] + "Bot:"

        response = get_gemini_response(context)
        bot_response = ""

        for chunk in response:
            if hasattr(chunk, 'text'):
                bot_response += chunk.text
            else:
                st.warning("The bot could not generate a response. Please rephrase.")

        if bot_response:
            st.session_state['chat_history'].append(("You", input_text))
            st.session_state['chat_history'].append(("Bot", bot_response))
            st.session_state['conversation_context'] += f"Bot: {bot_response}\n"

    with chat_placeholder:
        for role, text in st.session_state['chat_history']:
            if role == "You":
                st.markdown(f"<div style='text-align: right; background-color: #A3FFA1; padding: 10px; border-radius: 10px; margin: 5px;'>{text}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='text-align: left; background-color: #EFEFEF; padding: 10px; border-radius: 10px; margin: 5px;'>{text}</div>", unsafe_allow_html=True)
        
        st.markdown("<div id='scroll_anchor'></div>", unsafe_allow_html=True)
        st.markdown("<script>window.scrollTo(0, document.body.scrollHeight);</script>", unsafe_allow_html=True)
