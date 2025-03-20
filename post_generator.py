import random
from llm_helper import llm
from preprocess import correct_tanglish_spelling

def get_length_str(length):
    """Maps the selected post length to a descriptive format."""
    length_map = {
        "Short": "1 to 5 lines",
        "Medium": "6 to 10 lines",
        "Long": "11 to 15 lines"
    }
    return length_map.get(length, "6 to 10 lines")  # Default to Medium

def generate_post(post_length, language, topic, profession, post_reason, custom_keywords=""):
    """
    Generates a LinkedIn post that **perfectly matches the user’s inputs**.

    - **post_length**: Short, Medium, or Long
    - **language**: English or Tanglish
    - **topic**: The subject of the post
    - **profession**: User's selected profession
    - **post_reason**: The purpose of the post (e.g., "Won a Hackathon", "Landed a New Job")
    - **custom_keywords**: Additional keywords to fine-tune the post

    Returns:
        A **unique, expectation-matching LinkedIn post**.
    """

    # ✅ **Prevent Empty Inputs**
    if not topic:
        return "⚠️ Error: Topic is missing!"
    if not profession:
        return "⚠️ Error: Profession is missing!"
    if not post_reason:
        return "⚠️ Error: Please specify the purpose of your post."

    length_str = get_length_str(post_length)

    # ✅ **Dynamically Constructed Prompt (No Templates, Just AI Thinking)**
    prompt = f"""
    You are an expert LinkedIn post writer. Generate a **100% unique, highly relevant LinkedIn post** based on these details:

    🏆 **Purpose of Post**: {post_reason}
    💼 **Profession**: {profession}
    🔹 **Topic**: {topic}
    📏 **Length**: {length_str}
    🔑 **Extra Keywords**: {custom_keywords if custom_keywords else "None"}
    
    **Post Expectations**:
    - Ensure the post is **highly relevant to the purpose of the post**.
    - Structure the content properly. If the purpose is **"Completed a Course"**, mention the learning experience, key takeaways, and excitement for the future.
    - **DO NOT generate generic text**. Every word should be meaningful and aligned to the purpose.
    - If **Tanglish**, mix Tamil and English naturally (written in English script).
    - Use an **engaging style** that will encourage LinkedIn engagement.
    
    Generate only the LinkedIn post content, no preambles.
    """

    try:
        # ✅ **Generate post using Groq Cloud's Llama 3 model**
        response = llm.generate(prompt, model="llama3-8b-8192")

        # ✅ **Handle any AI failures or empty responses**
        if not response or not isinstance(response, str):
            return "⚠️ AI was unable to generate a valid post. Please try again."

        # ✅ **Apply Tanglish Spelling Correction (if needed)**
        if language == "Tanglish":
            response = correct_tanglish_spelling(response)

        return response

    except Exception as e:
        return f"⚠️ Error generating post: {str(e)}"
