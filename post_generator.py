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
    Generates a LinkedIn post that **perfectly** matches the user’s inputs.

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

    # ✅ **Fully Dynamic Prompt (No Templates, Just AI Magic)**
    prompt = f"""
    Generate a **100% unique, highly relevant LinkedIn post** based on the following:
    
    🏆 **Purpose of Post**: {post_reason}
    💼 **Profession**: {profession}
    🔹 **Topic**: {topic}
    📏 **Length**: {length_str}
    🔑 **Extra Keywords**: {custom_keywords if custom_keywords else "None"}

    **Content Expectations**:
    - **DO NOT** generate a generic post. The content must be **highly relevant** to {post_reason}.
    - **DO NOT** make assumptions outside the given details.
    - The structure should logically follow the purpose (e.g., if it's about "Winning a Hackathon", talk about the journey, teamwork, challenges, and key lessons).
    - The content should **feel real, natural, and written by a human**.
    - If **Tanglish**, mix Tamil and English naturally in **English script**.
    """

    try:
        # ✅ **Generate post using AI**
        response = llm.generate(prompt)

        # ✅ **Handle any AI failures or empty responses**
        if not response or not isinstance(response, str):
            return "⚠️ AI was unable to generate a valid post. Please try again."

        # ✅ **Apply Tanglish Spelling Correction (if needed)**
        if language == "Tanglish":
            response = correct_tanglish_spelling(response)

        return response

    except Exception as e:
        return f"⚠️ Error generating post: {str(e)}"
