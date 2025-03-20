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
    Generates a **highly personalized LinkedIn post** based on user inputs.

    - **post_length**: Short, Medium, or Long
    - **language**: English or Tanglish
    - **topic**: The subject of the post
    - **profession**: User's selected profession
    - **post_reason**: The purpose of the post (e.g., "My Experience with Job Interviews", "Landed a New Job")
    - **custom_keywords**: Additional keywords to fine-tune the post

    Returns:
        A **unique, contextually relevant LinkedIn post**.
    """

    # ✅ **Prevent Empty Inputs**
    if not topic:
        return "⚠️ Error: Topic is missing!"
    if not profession:
        return "⚠️ Error: Profession is missing!"
    if not post_reason:
        return "⚠️ Error: Please specify the purpose of your post."

    length_str = get_length_str(post_length)

    # ✅ **Dynamically Generate Prompt Based on Purpose**
    prompt = f"""
    🎯 **Create a LinkedIn post that feels engaging, natural, and contextually relevant.**
    
    🏆 **Post Purpose**: {post_reason}
    💼 **Profession**: {profession}
    🔹 **Topic**: {topic}
    📏 **Length**: {length_str}
    🔑 **Extra Details**: {custom_keywords if custom_keywords else "None"}

    🎯 **What the post should achieve**:
    - The content should **match the user’s intention fully** (no generic responses).
    - Avoid clichés—make it **unique, real, and valuable**.
    - If **Tanglish**, mix Tamil and English naturally (English script).

    💡 **Make sure the post fits the tone of the purpose.**
    - If the purpose is **'Job Interview Experience'**, share learnings, challenges, and key takeaways.
    - If the purpose is **'Landed a New Job'**, share the excitement, gratitude, and future vision.
    - If the purpose is **'Completed a Course'**, share the learning experience and future applications.
    """

    try:
        # ✅ **Generate post using LLM**
        response = llm.generate(prompt)

        # ✅ **Handle empty or invalid response**
        if not response or not isinstance(response, str):
            return generate_fallback_post(topic, profession, post_reason, post_length, language)

        # ✅ **Apply Tanglish Spelling Correction (if needed)**
        if language == "Tanglish":
            response = correct_tanglish_spelling(response)

        return response

    except Exception:
        return generate_fallback_post(topic, profession, post_reason, post_length, language)


def generate_fallback_post(topic, profession, post_reason, post_length, language):
    """
    Generates a **fallback post** when LLM fails.
    
    - Uses a **structured but flexible approach** to ensure a **valuable** post.
    - Tanglish posts are **written naturally** instead of direct translations.
    """

    length_str = get_length_str(post_length)

    # ✅ **Intelligent fallback generation based on purpose**
    if post_reason == "My Experience with Job Interviews":
        english_fallbacks = [
            f"""
            🎤 Job interviews are more than just a test of skills—they are a test of mindset.

            As a **{profession}**, I’ve had my share of **challenging interviews** in {topic}. Some went well, some didn’t, but each one **taught me something valuable**.

            Key takeaway? **Confidence and preparation matter as much as technical skills.**
            If you're preparing for interviews, my biggest advice: **Be yourself and keep learning!** 🚀 #JobInterviews
            """,

            f"""
            🎯 Interviews can be unpredictable, but every experience makes you stronger.

            In my journey as a **{profession}**, I’ve faced **tough technical rounds, unexpected questions, and even rejections**. But each one shaped me.

            The best lesson? **A rejection today might lead to a better opportunity tomorrow.**  
            Keep learning, keep growing! 💡 #CareerLessons
            """
        ]

        tanglish_fallbacks = [
            f"""
            🎤 Interview vera level experience dhaan! 😅  

            **{topic}** la konjam confident ah irunthalum, interview la kelvi kekum pothu vera level tension varum! 🤯  
            
            **Experience enna soludhu na?** Confidence iruntha pothum! **Preparation + Nambikkai = Success!** 💡  
            Naangalum kashtapattu kathukitom, neengalum nalla perform pannunga! 🔥 #JobInterview
            """,

            f"""
            🔥 **Interview vera level learning experience dhaan!**  

            **Naan {topic} pathi kathukittu nalla prepare pannirunthalum**, interview la unexpected questions kekum pothu thirupi yosikanum.  

            **Lesson?** Rejection nu oru periya vishayam illa, **oru door close aana, innoru better chance ready irukum!** 🚀  
            Neenga ethana interviews attend pannirukeenga? Share pannunga! 💡 #CareerGrowth
            """
        ]

    elif post_reason == "Landed a New Job":
        english_fallbacks = [
            f"""
            🎉 Exciting update! I’m thrilled to announce that I’ve joined **{profession}** role in {topic}!  

            The journey wasn’t easy—lots of **learning, rejections, and self-doubt** along the way. But every challenge shaped me into who I am today.  

            To everyone still searching, **stay patient, keep learning, and trust the process**. 🚀 #NewJob #CareerGrowth
            """
        ]

        tanglish_fallbacks = [
            f"""
            🔥 Vera level news! **Naan ippo {profession} role ku join panniten in {topic}!** 😍  

            **Challenges irunthuchu**, but **hard work + patience** success kuduthuchu!  
            Ithuvum oru new start dhaan! 🚀 **Naangalum improve aaganum, neengalum improve aaganum!**  

            **Neenga enna challenges face panninga? Let’s discuss!** #NewJob
            """
        ]

    else:
        english_fallbacks = [
            f"""
            🚀 Big step forward! Just achieved a major milestone in {topic} as a **{profession}**.  

            Every journey comes with struggles, but growth happens when we embrace challenges.  
            Excited for what’s next! Let’s connect and grow together. 💡 #Networking
            """
        ]

        tanglish_fallbacks = [
            f"""
            🔥 Periya step forward! **Naan {topic} la oru milestone achieve panniten** as a **{profession}**.  

            **Life la ellame oru learning dhaan!** Innum nalla improve aaganum nu nenekiren! 🚀  
            **Neenga enna nenekreenga? Let's discuss!** 💡 #CareerGrowth
            """
        ]

    return random.choice(tanglish_fallbacks) if language == "Tanglish" else random.choice(english_fallbacks)
