import random
from llm_helper import generate_response
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
    Generates a LinkedIn post that is highly relevant and unique.

    - **post_length**: Short, Medium, or Long
    - **language**: English or Tanglish
    - **topic**: The subject of the post
    - **profession**: User's selected profession
    - **post_reason**: The purpose of the post (e.g., "Completed a Course", "Landed a New Job")
    - **custom_keywords**: Additional keywords to fine-tune the post

    Returns:
        A unique LinkedIn post string.
    """

    # ✅ **Ensure all inputs are present**
    if not topic:
        return "⚠️ Error: Topic is missing!"
    if not profession:
        return "⚠️ Error: Profession is missing!"
    if not post_reason:
        return "⚠️ Error: Please specify the purpose of your post."

    length_str = get_length_str(post_length)

    # ✅ **Dynamically Constructed Prompt Based on User Input**
    prompt = f"""
    You are a professional LinkedIn post writer. Generate a **highly relevant, structured, and engaging LinkedIn post** based on these details:

    🏆 **Purpose of Post**: {post_reason}
    💼 **Profession**: {profession}
    🔹 **Topic**: {topic}
    📏 **Length**: {length_str}
    🔑 **Additional Keywords**: {custom_keywords if custom_keywords else "None"}
    
    **Post Expectations**:
    - Ensure the post is **directly related to the purpose of the post**.
    - Structure the content properly. Example:
      - If the purpose is **"Completed a Course"**, discuss the learning experience, key takeaways, and future goals.
      - If the purpose is **"Won a Hackathon"**, describe the project, teamwork, and what was learned.
    - **No generic content** – it should feel personal, meaningful, and context-aware.
    - If **Tanglish**, mix Tamil and English naturally (written in English script).
    - Use an **engaging, professional, and storytelling tone**.
    
    Generate only the LinkedIn post content, no preambles.
    """

    try:
        # ✅ **Generate post using LLM**
        response = generate_response(prompt)

        # ✅ **Handle any API failures or empty responses**
        if not response or not isinstance(response, str) or response.strip() == "":
            return "⚠️ Error: LLM response was empty. Please try again."

        # ✅ **Apply Tanglish Spelling Correction (if needed)**
        if language == "Tanglish":
            response = correct_tanglish_spelling(response)

        return response.strip()

    except Exception as e:
        return f"⚠️ Error generating post: {str(e)}"
