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
    Generates a LinkedIn post based on user inputs.

    - **post_length**: Short, Medium, or Long
    - **language**: English or Tanglish
    - **topic**: The subject of the post
    - **profession**: User's selected profession
    - **post_reason**: The purpose of the post (e.g., "Completed a Course", "Landed a New Job")
    - **custom_keywords**: Additional keywords to fine-tune the post

    Returns:
        A unique LinkedIn post as a string.
    """

    # ✅ Prevent Empty Inputs
    if not topic:
        return "⚠️ Error: Topic is missing!"
    if not profession:
        return "⚠️ Error: Profession is missing!"
    if not post_reason:
        return "⚠️ Error: Please specify the purpose of your post."

    length_str = get_length_str(post_length)

    # **Dynamically Varying Prompts Based on Purpose**
    prompt_variations = {
        "Completed a Course": [
            f"""
            🎓 **Generate a professional, insightful LinkedIn post celebrating course completion.**
            
            📚 **Course Accomplished**: {topic}
            💼 **Profession**: {profession}
            📏 **Post Length**: {length_str}
            🔍 **Key Learnings & Takeaways**: {custom_keywords if custom_keywords else "None"}

            🎯 **Guidelines**:
            - Highlight **key takeaways** from the course.
            - Express excitement for **what's next** (future learning/career application).
            - If **Tanglish**, mix Tamil & English fluently.
            """,
            
            f"""
            🎉 **I just completed a course!** 🚀

            ✅ **Course**: {topic}  
            💼 **My Profession**: {profession}  
            📏 **Post Length**: {length_str}  
            🔑 **Extra Insights**: {custom_keywords if custom_keywords else "None"}

            🔥 **Key Learnings**:
            - What did I find most exciting?
            - How will this course impact my career?
            - What’s my next step?

            Let's celebrate achievements & keep learning together! 🚀
            """
        ],
        "Landed a New Job": [
            f"""
            🚀 **Big Career Update!**
            
            🎉 I’m thrilled to announce that I’ve just landed a new job as a **{profession}**! 

            Over the past months, I have worked hard on {topic}, and now I finally have the chance to apply my skills in a professional setting. 

            Looking forward to this exciting new journey! 🚀
            """,

            f"""
            💼 **New Beginnings!**  

            I’m excited to start my new role as a **{profession}**! My journey in {topic} has been an incredible learning experience, and I can’t wait to contribute my skills.  

            **What’s next?**  
            - 🚀 Growing as a {profession}  
            - 🎯 Building expertise in {topic}  
            - 🤝 Connecting with amazing professionals

            If you’re in {topic}, let’s connect and grow together! #Networking
            """
        ]
    }

    # ✅ Choose a random prompt variation
    prompt = random.choice(prompt_variations.get(post_reason, [
        f"""
        🎯 **Create a LinkedIn post that is professional, inspiring, and engaging.**
        
        🏆 **Post Context**: {post_reason}
        💼 **Profession**: {profession}
        🔹 **Topic**: {topic}
        📏 **Length**: {length_str}
        🔑 **Custom Keywords**: {custom_keywords if custom_keywords else "None"}
        
        📝 **Guidelines**:
        - The tone should match the excitement of the user's milestone.
        - Avoid generic phrases. The post should be **authentic, engaging, and unique**.
        - If **Tanglish**, mix Tamil and English naturally (English script).
        """
    ]))

    try:
        # ✅ Retrieve relevant example posts
        examples = few_shot.get_filtered_posts(post_length, language, topic)
        if examples:
            prompt += "\n\n📌 **Example Writing Styles:**"
            for i, post in enumerate(examples):
                prompt += f"\n\n**Example {i+1}:**\n{post['text']}"
                if i == 1:  # Limit to two examples
                    break

        # ✅ Generate post using LLM
        response = llm.generate(prompt)

        # ✅ Handle empty or invalid response
        if not response or not isinstance(response, str):
            return generate_fallback_post(topic, profession, post_reason, post_length, language)

        # ✅ Apply Tanglish Spelling Correction (if needed)
        if language == "Tanglish":
            response = correct_tanglish_spelling(response)

        return response

    except Exception:
        # ✅ Fallback post in case of any LLM failure
        return generate_fallback_post(topic, profession, post_reason, post_length, language)


def generate_fallback_post(topic, profession, post_reason, post_length, language):
    """
    Generates a fallback post when LLM fails.
    
    - Uses a structured manual format to ensure users still get a useful post.
    - Tanglish posts are generated manually to ensure natural language flow.
    """

    length_str = get_length_str(post_length)

    english_fallback_templates = [
        f"""
        🎉 Big news! I just {post_reason.lower()} in **{topic}** as a **{profession}**. 

        This journey has been challenging yet rewarding. The insights I gained from {topic} are invaluable, and I'm eager to apply them in real-world projects. 

        Looking forward to learning more and connecting with like-minded professionals. Let’s grow together! 🚀 #CareerGrowth""",

        f"""
        🔥 Exciting milestone! As a **{profession}**, I’ve recently {post_reason.lower()} in **{topic}**. 

        This experience has deepened my knowledge, and I can’t wait to contribute more to this field. 

        If you're also passionate about {topic}, let's connect and exchange ideas! 💡 #Networking""",

        f"""
        🚀 Feeling proud! I’ve just {post_reason.lower()} in **{topic}**, marking a major step in my journey as a **{profession}**. 

        Every day is a learning opportunity, and I’m excited about what’s next. 

        Who else is exploring {topic}? Let’s discuss! 🌱 #Learning"""
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
