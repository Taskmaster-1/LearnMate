import streamlit as st
from google.cloud import texttospeech

def run_multilingual_tts():
    st.title("Multilingual Text-to-Speech")
    
    text = st.text_area("Enter text:")
    language_code = st.selectbox("Select Language", ["en-US", "es-ES", "fr-FR"])
    
    if st.button("Generate Speech"):
        with st.spinner("Generating speech..."):
            client = texttospeech.TextToSpeechClient()
            synthesis_input = texttospeech.SynthesisInput(text=text)
            voice = texttospeech.VoiceSelectionParams(language_code=language_code)
            audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
            response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

            with open("output.mp3", "wb") as out:
                out.write(response.audio_content)
            st.audio("output.mp3", format="audio/mp3")
            st.download_button("Download Speech", data="output.mp3", file_name="speech.mp3")
