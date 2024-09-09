import streamlit as st
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

class AdaptiveLearning:
    def __init__(self):
        self.scaler = StandardScaler()
        self.model = KMeans(n_clusters=3)
        
    def update_user_model(self, user_data):
        
        features = np.array([[
            user_data['quiz_scores'],
            user_data['time_spent'],
            user_data['interaction_type']
        ]])
        scaled_features = self.scaler.fit_transform(features)
        self.model.fit(scaled_features)
        
    def get_learning_style(self, user_data):
        features = np.array([[
            user_data['quiz_scores'],
            user_data['time_spent'],
            user_data['interaction_type']
        ]])
        scaled_features = self.scaler.transform(features)
        return self.model.predict(scaled_features)[0]
    
    def recommend_content(self, learning_style):
        
        content_types = {
            0: "Visual content with interactive elements",
            1: "Text-based in-depth explanations",
            2: "Audio lectures with quizzes"
        }
        return content_types.get(learning_style, "Mixed content")

def run_adaptive_learning():
    st.header("🧠 Adaptive Learning")
    
    if 'adaptive_model' not in st.session_state:
        st.session_state.adaptive_model = AdaptiveLearning()
    
    
    quiz_score = st.slider("Recent Quiz Score", 0, 100, 50)
    time_spent = st.slider("Time Spent Learning (minutes)", 0, 120, 60)
    interaction_type = st.selectbox("Preferred Interaction Type", ["Visual", "Textual", "Auditory"])
    
    if st.button("Update Learning Profile"):
        user_data = {
            'quiz_scores': quiz_score,
            'time_spent': time_spent,
            'interaction_type': ["Visual", "Textual", "Auditory"].index(interaction_type)
        }
        st.session_state.adaptive_model.update_user_model(user_data)
        learning_style = st.session_state.adaptive_model.get_learning_style(user_data)
        recommendation = st.session_state.adaptive_model.recommend_content(learning_style)
        
        st.success(f"Your learning profile has been updated!")
        st.info(f"Recommended content type: {recommendation}")
