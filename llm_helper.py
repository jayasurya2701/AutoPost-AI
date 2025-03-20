from langchain_groq import ChatGroq
import os
import streamlit as st
from dotenv import load_dotenv

# Load environment variables (if running locally)
load_dotenv()

# Sidebar input for API key (hidden for security)
st.sidebar.header("🔐 Enter Your Groq API Key")
user_api_key = st.sidebar.text_input("API Key", type="password")

# Store API key in session state
if user_api_key:
    st.session_state["GROQ_API_KEY"] = user_api_key
    st.sidebar.success("✅ API Key Set Successfully!")
else:
    st.sidebar.warning("⚠️ Please enter your API key to proceed.")

# Fetch API key (priority: user input → environment variable)
api_key = st.session_state.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")

# Ensure API key is present before making API calls
if not api_key:
    st.error("❌ API Key is missing! Please enter it in the sidebar.")
    st.stop()

# Initialize LLM with error handling
try:
    llm = ChatGroq(groq_api_key=api_key, model_name="llama3-8b-8192")
except Exception as e:
    st.error(f"❌ Failed to connect to Groq API: {e}")
    st.stop()

# Function to generate response
def generate_response(prompt):
    try:
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        return f"❌ Error: {e}"

# Testing functionality
if __name__ == "__main__":
    test_prompt = "What is the capital of India?"
    output = generate_response(test_prompt)
    print(output)
