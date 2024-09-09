import streamlit as st
from datetime import datetime, timedelta

class GamificationSystem:
    def __init__(self):
        self.levels = {
            1: 0,
            2: 100,
            3: 300,
            5: 600,
            10: 1000
        }
        self.badges = {
            "Quick Learner": "Complete 5 lessons in a day",
            "Night Owl": "Study for 2 hours after 10 PM",
            "Perfectionist": "Get 100% on 3 quizzes in a row",
            "Polyglot": "Use TTS in 5 different languages",
            "Document Master": "Chat with 20 different documents"
        }
    
    def calculate_level(self, xp):
        for level, threshold in sorted(self.levels.items(), reverse=True):
            if xp >= threshold:
                return level
        return 1
    
    def award_badge(self, user_stats):
        earned_badges = []
        if user_stats['lessons_completed_today'] >= 5:
            earned_badges.append("Quick Learner")
        if user_stats['night_study_hours'] >= 2:
            earned_badges.append("Night Owl")
        
        return earned_badges

def run_gamification():
    st.header("🏆 Your Learning Journey")
    
    if 'gamification_system' not in st.session_state:
        st.session_state.gamification_system = GamificationSystem()
    
    if 'user_xp' not in st.session_state:
        st.session_state.user_xp = 0
    
    
    if st.button("Complete a lesson (+10 XP)"):
        st.session_state.user_xp += 10
    
    level = st.session_state.gamification_system.calculate_level(st.session_state.user_xp)
    
    st.subheader(f"Current Level: {level}")
    st.progress(st.session_state.user_xp / 1000)  
    st.write(f"Total XP: {st.session_state.user_xp}")
    
    
    st.subheader("Your Badges")
    for badge, description in st.session_state.gamification_system.badges.items():
        st.write(f"- {badge}: {description}")

