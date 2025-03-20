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
    Generates a highly personalized LinkedIn post based on user inputs.

    - **post_length**: Short, Medium, or Long
    - **language**: English or Tanglish
    - **topic**: The subject of the post
    - **profession**: User's selected profession
    - **post_reason**: The purpose of the post (e.g., "Got a Promotion", "Completed a Course")
    - **custom_keywords**: Additional keywords to fine-tune the post

    Returns:
        A **unique, personalized LinkedIn post** as a string.
    """

    # ✅ Prevent Empty Inputs
    if not topic:
        return "⚠️ Error: Topic is missing!"
    if not profession:
        return "⚠️ Error: Profession is missing!"
    if not post_reason:
        return "⚠️ Error: Please specify the purpose of your post."

    length_str = get_length_str(post_length)

    # ✅ **Craft a dynamic prompt based on user selection**
    prompt = f"""
    ✨ **Create a LinkedIn post that is unique, engaging, and deeply personal.**
    
    🏆 **User Milestone**: {post_reason}
    💼 **Profession**: {profession}
    🔹 **Topic**: {topic}
    📏 **Length**: {length_str}
    🔑 **Extra Details**: {custom_keywords if custom_keywords else "None"}

    🎯 **What the post should convey**:
    - The user should sound **authentic, confident, and proud**.
    - It should feel **natural, engaging, and emotionally relatable**.
    - No overused phrases—make it **fresh, human-like, and inspiring**.
    - If **Tanglish**, use a smooth mix of Tamil+English in English script.
    """

    # ✅ **Generate post using LLM**
    try:
        response = llm.generate(prompt)

        # ✅ Handle empty or invalid response
        if not response or not isinstance(response, str):
            return generate_fallback_post(topic, profession, post_reason, post_length, language)

        # ✅ Apply Tanglish Spelling Correction (if needed)
        if language == "Tanglish":
            response = correct_tanglish_spelling(response)

        return response

    except Exception:
        return generate_fallback_post(topic, profession, post_reason, post_length, language)


def generate_fallback_post(topic, profession, post_reason, post_length, language):
    """
    Generates a **fallback post** when LLM fails.
    
    - Uses a **context-aware format** to ensure a **useful and meaningful** post.
    - Tanglish posts **sound natural** and not robotic.
    """

    length_str = get_length_str(post_length)

    # ✅ **Dynamic fallback content generation (No fixed templates)**
    if post_reason == "Got a Promotion":
        english_fallbacks = [
            f"""
            🚀 Exciting news! I’m incredibly grateful to have been **promoted as a {profession}** in the field of {topic}!

            This journey has been filled with challenges, learning, and growth. Looking forward to taking on **new responsibilities and contributing even more**.

            Huge thanks to my mentors, colleagues, and everyone who supported me! On to the next chapter! 🚀 #CareerGrowth #Promotion
            """,

            f"""
            🌟 A new milestone unlocked! 

            Thrilled to share that I’ve been **promoted as a {profession}**, marking a significant step in my journey in {topic}.

            Hard work, persistence, and passion always pay off! Excited to keep learning and contributing. 🚀 #Success #NewRole
            """
        ]

        tanglish_fallbacks = [
            f"""
            🔥 Vera level update! **Naan inime {profession} role ku promote aayiten!** 🚀

            **{topic}** la romba kashtapattu work panniten, ipo oru periya milestone reach panniten.  
            **Hard work, patience, and learning** – ithanoda key!  

            Neenga ellarum en support pannitinga, nandri! ❤️ #CareerGrowth
            """,

            f"""
            🎉 Semma happy moment!  

            **En promotion** vandhachu! 😍 **{profession}** role ku elevate aayiten in {topic}.  

            Challenges irundhalum, **kadaisi varaikum nambikkai irundhuchu** – ipo ithu result!  
            Let’s all grow together! 🚀 #Success #Promotion
            """
        ]

    elif post_reason == "Completed a Course":
        english_fallbacks = [
            f"""
            🎓 Just completed a deep-dive into **{topic}**! 

            As a **{profession}**, continuous learning is essential, and this course gave me incredible insights.  
            Looking forward to **applying these skills** in real-world projects. 🚀  

            **Have you taken any interesting courses lately? Let’s discuss!** 👇 #Learning #Upskilling
            """,

            f"""
            📚 Learning never stops!  

            Thrilled to share that I’ve successfully **completed a course on {topic}**.  
            Every new skill learned is a step forward. Excited to implement these insights in my role as a **{profession}**! 🚀  

            **What’s the best course you’ve ever taken? Drop your recommendations!** 👇 #CareerGrowth
            """
        ]

        tanglish_fallbacks = [
            f"""
            📚 Vera level course complete panniten!  

            **{topic}** pathi **deep ah study pannitu** ipo confidence ah iruken.  
            **Learning never stops da!** Ithoda next step apply pannitu, innum periya level ku poganum! 🚀  

            **Neenga ethavathu course complete panna experience share pannunga!** #Growth #Learning
            """,

            f"""
            🎉 Course complete agiduchu!  

            **{topic}** la periya learning eduthen.  
            **{profession}** ah irukura oruthanuku knowledge growth romba mukkiyam.  
            Naan next level la povathuku ready! 🔥  

            **Neenga enna course recommend pannuringa? Comment pannunga!** #Upskilling
            """
        ]

    else:
        english_fallbacks = [
            f"""
            🚀 Big milestone achieved! Just took a step forward in my career as a **{profession}** in {topic}.  
            Every journey has its challenges, but growth comes from pushing through.  

            Excited for what’s next! Let’s connect and share insights. 💡 #CareerGrowth #Networking
            """
        ]

        tanglish_fallbacks = [
            f"""
            🔥 Periya milestone! **Naan {topic} la oru periya step eduthiruken** as a {profession}.  
            **Life la ellame oru learning dhaan!** Innum nalla improve aaganum nu nenekiren! 🚀  
            **Neenga enna nenekreenga? Let's discuss!** 💡 #CareerGrowth
            """
        ]

    return random.choice(tanglish_fallbacks) if language == "Tanglish" else random.choice(english_fallbacks)
