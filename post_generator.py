import random
from llm_helper import llm
from few_shot import FewShotPosts
from preprocess import correct_tanglish_spelling

few_shot = FewShotPosts()

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
    Generates a fully **dynamic LinkedIn post** based on user inputs.

    - **post_length**: Short, Medium, or Long
    - **language**: English or Tanglish
    - **topic**: The subject of the post
    - **profession**: User's selected profession
    - **post_reason**: The purpose of the post (e.g., "Won a Hackathon", "Landed a New Job")
    - **custom_keywords**: Additional keywords to fine-tune the post

    Returns:
        A **context-aware, unique LinkedIn post**.
    """

    # ✅ **Prevent Empty Inputs**
    if not topic:
        return "⚠️ Error: Topic is missing!"
    if not profession:
        return "⚠️ Error: Profession is missing!"
    if not post_reason:
        return "⚠️ Error: Please specify the purpose of your post."

    length_str = get_length_str(post_length)

    # ✅ **Dynamically Generated Prompt (Fully AI-Driven)**
    prompt = f"""
    🎯 **Generate a highly engaging, 100% contextually accurate LinkedIn post.**
    
    🏆 **Post Purpose**: {post_reason}
    💼 **Profession**: {profession}
    🔹 **Topic**: {topic}
    📏 **Length**: {length_str}
    🔑 **Extra Details**: {custom_keywords if custom_keywords else "None"}

    **Guidelines for the AI**:
    - Make the post **100% unique and fully relevant to the user's reason for posting**.
    - The structure should **logically follow the purpose** (e.g., if the user "Won a Hackathon", the post should highlight their experience, teamwork, and learnings).
    - The content should **not be generic**—make it **deeply personal, specific, and engaging**.
    - If **Tanglish**, mix Tamil and English naturally in English script.

    **Post Expectations**:
    - If the purpose is **"Won a Hackathon"**, highlight the **challenges faced, teamwork, innovations, and key takeaways**.
    - If the purpose is **"Completed a Course"**, focus on **learnings, applications, and how it will impact the future**.
    - If the purpose is **"Got a Promotion"**, emphasize **career growth, recognition, and motivation for others**.
    - If the purpose is **"Landed a New Job"**, describe **the journey, struggles, and gratitude**.

    🚀 **Make sure each generated post is completely fresh and does not repeat previous responses.**
    """

    try:
        # ✅ **Generate post using LLM**
        response = llm.generate(prompt)

        # ✅ **Handle empty or invalid response**
        if not response or not isinstance(response, str):
            return "⚠️ Error: The AI was unable to generate a response. Please try again."

        # ✅ **Apply Tanglish Spelling Correction (if needed)**
        if language == "Tanglish":
            response = correct_tanglish_spelling(response)

        return response

    except Exception as e:
        return f"⚠️ Error generating post: {str(e)}"
