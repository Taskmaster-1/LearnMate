import streamlit as st
from qachat import run_Chat
from ivextract import run_invoice_extractor
from chat import run_Document
from tts_multilingual import run_multilingual_tts
from learning_companion import run
from adaptive import run_adaptive_learning
from Gamification import run_gamification
from voice_assistant import run_voice_assistant
import base64

def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
        background-image: url("data:image/png;base64,%s");
        background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

def local_css(file_name):
    with open(file_name, "r") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def main():
    st.set_page_config(page_title="LearnMate", layout="wide", initial_sidebar_state="expanded")
    local_css("style.css")
    set_background('background.webp')

    # Initialize session state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Home"

    # Sidebar
    with st.sidebar:
        st.image("learnMate.png", width=200)
        st.title("LearnMate")
        menu_options = {
            "Home": "🏠",
            "Q&A Chat": "💬",
            "Invoice Extractor": "📄",
            "Document Chat": "📚",
            "Multilingual TTS": "🗣️",
            "Learning Companion": "🧠",
            "Adaptive Learning": "📊",
            "Gamification": "🏆",
            "Voice Assistant": "🎙️"
        }
        
        for option, icon in menu_options.items():
            if st.button(f"{icon} {option}", key=f"btn_{option}", use_container_width=True):
                st.session_state.current_page = option

    # Main content area
    if st.session_state.current_page == "Home":
        show_intro()
    elif st.session_state.current_page == "Q&A Chat":
        run_Chat()
    elif st.session_state.current_page == "Invoice Extractor":
        run_invoice_extractor()
    elif st.session_state.current_page == "Document Chat":
        run_Document()
    elif st.session_state.current_page == "Multilingual TTS":
        run_multilingual_tts()
    elif st.session_state.current_page == "Learning Companion":
        run()
    elif st.session_state.current_page == "Adaptive Learning":
        run_adaptive_learning()
    elif st.session_state.current_page == "Gamification":
        run_gamification()
    elif st.session_state.current_page == "Voice Assistant":
        run_voice_assistant()

def show_intro():
    st.title("Welcome to LearnMate! 🚀")
    st.write("Your AI-powered interactive learning assistant.")
    
    st.markdown("""
    <div class="grid-container">
        <div class="grid-item">
            <h3>💬 Q&A Chat</h3>
            <p>Get instant answers to your questions using our AI-powered chatbot.</p>
        </div>
        <div class="grid-item">
            <h3>📄 Invoice Extractor</h3>
            <p>Easily extract and analyze information from invoice documents.</p>
        </div>
        <div class="grid-item">
            <h3>📚 Document Chat</h3>
            <p>Chat with your documents and extract valuable insights.</p>
        </div>
        <div class="grid-item">
            <h3>🗣️ Multilingual TTS</h3>
            <p>Convert text to speech in multiple languages for enhanced learning.</p>
        </div>
        <div class="grid-item">
            <h3>🧠 Learning Companion</h3>
            <p>Get personalized learning paths and interactive quizzes.</p>
        </div>
        <div class="grid-item">
            <h3>📊 Adaptive Learning</h3>
            <p>Experience a learning journey tailored to your unique style and pace.</p>
        </div>
        <div class="grid-item">
            <h3>🏆 Gamification</h3>
            <p>Level up your learning with points, badges, and rewards.</p>
        </div>
        <div class="grid-item">
            <h3>🎙️ Voice Assistant</h3>
            <p>Interact with LearnMate using voice commands for hands-free learning.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()