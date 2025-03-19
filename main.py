import streamlit as st
import os
from few_shot import FewShotPosts
from post_generator import generate_post
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Options for length and language
length_options = ["Short", "Medium", "Long"]
language_options = ["English", "Tanglish"]

# Sidebar for API Key input (hidden)
st.sidebar.header("🔐 Enter LLM API Key")
user_api_key = st.sidebar.text_input("API Key", type="password")

# Store API key in session state (secure access)
if user_api_key:
    os.environ["GROQ_API_KEY"] = user_api_key
    st.sidebar.success("✅ API Key Set Successfully!")
else:
    st.sidebar.warning("⚠️ Please enter your API key to generate posts.")

# Main app layout
def main():
    st.subheader("🚀 AutoPost-AI : AI-Powered-LinkedIn-Post-Generator")

    # Create three columns for dropdowns
    col1, col2, col3 = st.columns(3)

    fs = FewShotPosts()
    tags = fs.get_tags()

    with col1:
        selected_tag = st.selectbox("📌 Topic", options=tags)

    with col2:
        selected_length = st.selectbox("📏 Length", options=length_options)

    with col3:
        selected_language = st.selectbox("🗣 Language", options=language_options)

    # Generate Button
    if st.button("✨ Generate Post"):
        if not user_api_key:
            st.error("❌ API Key is required to generate posts.")
        else:
            post = generate_post(selected_length, selected_language, selected_tag)
            st.write(post)

# Run the app
if __name__ == "__main__":
    main()
