import streamlit as st
import os
from google.cloud import speech
import pyaudio
import wave
import io
import threading
import queue
import time
from google.oauth2 import service_account

class GoogleCloudVoiceAssistant:
    def __init__(self):
        self.client = speech.SpeechClient()
        self.config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code="en-US",
        )
        self.streaming_config = speech.StreamingRecognitionConfig(
            config=self.config, interim_results=True
        )
        self.audio_queue = queue.Queue()

    def listen(self):
        st.write("Listening... (Click 'Stop' when finished speaking)")
        stop_listening = st.button("Stop")

        audio_interface = pyaudio.PyAudio()
        audio_stream = audio_interface.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=1024,
        )

        while not stop_listening:
            data = audio_stream.read(1024)
            self.audio_queue.put(data)

        audio_stream.stop_stream()
        audio_stream.close()
        audio_interface.terminate()

        return self.transcribe()

    def transcribe(self):
        def request_generator():
            while True:
                chunk = self.audio_queue.get()
                if chunk is None:
                    break
                yield speech.StreamingRecognizeRequest(audio_content=chunk)

        requests = request_generator()
        responses = self.client.streaming_recognize(self.streaming_config, requests)

        for response in responses:
            for result in response.results:
                if result.is_final:
                    return result.alternatives[0].transcript

        return ""

    def process_command(self, command):
        if "lesson" in command:
            return "Opening the latest lesson for you."
        elif "quiz" in command:
            return "Starting a new quiz now."
        elif "explain" in command:
            return "I'd be happy to explain. What topic would you like to know more about?"
        else:
            return "I'm sorry, I didn't understand that command."

def run_voice_assistant():
    st.header("🎙️ Google Cloud Voice-Activated Learning Assistant")
    
    if 'voice_assistant' not in st.session_state:
        st.session_state.voice_assistant = GoogleCloudVoiceAssistant()
    
    if st.button("Start Listening"):
        command = st.session_state.voice_assistant.listen()
        if command:
            st.write(f"You said: {command}")
            response = st.session_state.voice_assistant.process_command(command)
            st.write(f"Assistant: {response}")
            #text-to-speech
