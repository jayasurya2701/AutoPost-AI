import streamlit as st
import os
from few_shot import FewShotPosts
from post_generator import generate_post
from dotenv import load_dotenv

# Profession categories, subcategories, and discussion topics
professions = {
    "Technical": {
        "IT": {
            "Software Developer": ["Coding", "Debugging", "Software Architecture"],
            "Full Stack Developer": ["Frontend", "Backend", "APIs"],
            "Mobile App Developer": ["Android", "iOS", "Cross-Platform"]
        },
        "AI": {
            "AI Engineer": ["MachineLearning", "DeepLearning", "NLP"],
            "Robotics Engineer": ["Automation", "AI Ethics", "Computer Vision"]
        }
    },
    "Healthcare": {
        "Doctors": {
            "Surgeon": ["Surgery", "Medical Innovations", "Patient Care"],
            "Cardiologist": ["Heart Health", "Treatments", "Research"]
        }
    }
}

length_options = ["Short", "Medium", "Long"]
language_options = ["English", "Tanglish"]

def main():
    st.subheader("🚀 LinkedIn Post Generator")
    fs = FewShotPosts()
    tags = fs.get_tags()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        selected_tag = st.selectbox("🔹 Select a General Topic:", options=tags)
    
    with col2:
        selected_category = st.selectbox("📂 Select Category:", options=professions.keys())
        selected_subcategory = st.selectbox("📁 Select Subcategory:", options=professions[selected_category].keys())
        selected_profession = st.selectbox("💼 Select Your Profession:", options=professions[selected_category][selected_subcategory].keys())
    
    with col3:
        selected_topic = st.selectbox("🎯 Select a Discussion Topic:", options=professions[selected_category][selected_subcategory][selected_profession])
        selected_language = st.selectbox("📝 Select Language:", options=language_options)
    
    selected_length = st.radio("📏 Select Post Length:", options=length_options, horizontal=True)
    custom_keywords = st.text_input("🔑 Add Specific Keywords (Optional)", help="Enter keywords to fine-tune the generated post.")
    
    if st.button("⚡ Generate Post"):
        post = generate_post(selected_length, selected_language, selected_topic, selected_profession, custom_keywords)
        st.write(post)

if __name__ == "__main__":
    main()
