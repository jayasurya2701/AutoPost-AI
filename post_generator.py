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

        # ✅ **Ensure response is a valid string**
        if not response or not isinstance(response, str):
            return generate_fallback_post(topic, profession, post_reason, post_length, language)

        # ✅ **Apply Tanglish Spelling Correction (if needed)**
        if language == "Tanglish":
            response = correct_tanglish_spelling(response)

        return response.strip()  # Ensure clean output

    except Exception as e:
        return f"⚠️ Error generating post: {str(e)}"

def generate_fallback_post(topic, profession, post_reason, post_length, language):
    """
    Generates a fallback post when LLM fails.
    
    - Uses a structured manual format to ensure users still get a useful post.
    - Tanglish posts are generated manually to ensure natural language flow.
    """

    length_str = get_length_str(post_length)

    english_fallback_templates = [
        f"""
        🎉 Just achieved a major milestone! **{post_reason}** in {topic} as a {profession}.  
        It was a challenging yet rewarding experience, and I’m excited for what’s ahead!  
        Learning never stops—let’s connect and grow together. 🚀 #CareerGrowth""",

        f"""
        🚀 Big moment! I’ve recently **{post_reason.lower()}** in {topic} as a {profession}.  
        This journey has taught me valuable lessons, and I can’t wait to explore further.  
        Who else is passionate about {topic}? Let’s discuss! 💡 #Networking""",

        f"""
        🔥 Super excited! Just **{post_reason.lower()}** in {topic}.  
        Every day is a new learning opportunity, and I’m grateful for this step forward in my career as a {profession}.  
        Looking forward to connecting with more professionals in this space! #GrowthMindset"""
    ]

    tanglish_fallback_templates = [
        f"""
        🎉 Vera level update! **Naan {topic} la oru periya step eduthiruken** as a **{profession}**!  
        **{post_reason}** panna romba kashtam, aana super experience ah irundhuchu. Innum nariya kathukanum nu feel pannuren.  
        **Ungaloda experience enna?** Let’s connect! 🚀 #Networking""",

        f"""
        🔥 Semma proud moment! **Naan {topic} pathi deep ah kathukiten** as a **{profession}**.  
        **{post_reason}** panna vera level feel! Innum nalla improve aaganum nu wait pannitu iruken.  
        **Neenga enna nenekreenga? Let's discuss!** 💡 #CareerGrowth""",

        f"""
        🚀 Enna oru journey! **{topic} la periya growth achieve panniten** as a **{profession}**.  
        **{post_reason}** nu solla super happy ah iruken. Innum nariya updates share pannuren!  
        **Let’s connect and grow together!** 🌱 #Networking"""
    ]

    return random.choice(tanglish_fallback_templates) if language == "Tanglish" else random.choice(english_fallback_templates)
