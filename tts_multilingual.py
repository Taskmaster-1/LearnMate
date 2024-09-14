import streamlit as st
from google.cloud import texttospeech
from google.cloud import translate_v2 as translate
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Google Cloud clients
tts_client = texttospeech.TextToSpeechClient()
translate_client = translate.Client()

# Language code mappings
language_codes = {
    "English (US)": "en-US",
    "Spanish (Spain)": "es-ES",
    "French (France)": "fr-FR",
    "German (Germany)": "de-DE",
    "Hindi (India)": "hi-IN"
}

def translate_text(text, target_language):
    result = translate_client.translate(text, target_language=target_language)
    return result['translatedText']

def convert_text_to_speech_google_cloud(text, language_code):
    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = tts_client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return response.audio_content

def run_multilingual_tts():
    st.title("Multilingual Text-to-Speech with Translation")
    
    # Input text
    text = st.text_area("Enter text:", value="Hello, how are you?")
    
    # Language selection
    selected_language = st.selectbox(
        "Select Language for Translation and Speech",
        list(language_codes.keys())
    )
    
    # Detect the target language code for translation and TTS
    target_language_code = language_codes[selected_language]

    if st.button("Generate Speech"):
        if text.strip() == "":
            st.error("Please enter some text to generate speech.")
            return

        with st.spinner("Translating and generating speech..."):
            try:
                # Translate the input text to the selected language
                translated_text = translate_text(text, target_language=target_language_code[:2])  # Use only language part for translation
                
                # Convert the translated text to speech
                audio_content = convert_text_to_speech_google_cloud(translated_text, target_language_code)

                # Save the audio to a file
                with open("output.mp3", "wb") as out:
                    out.write(audio_content)
                
                # Play and download the audio file
                st.audio("output.mp3", format="audio/mp3")
                with open("output.mp3", "rb") as f:
                    st.download_button("Download Speech", data=f, file_name="speech.mp3")
            
            except Exception as e:
                st.error(f"An error occurred: {e}")

# Run the app
#run_multilingual_tts()
