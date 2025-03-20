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
    - **post_reason**: Context for why this post is being generated
    - **custom_keywords**: Additional keywords to fine-tune the post

    Returns:
        A generated LinkedIn post as a string.
    """

    # ✅ Prevent Empty Inputs
    if not topic:
        return "⚠️ Error: Topic is missing!"
    if not profession:
        return "⚠️ Error: Profession is missing!"
    if not post_reason:
        return "⚠️ Error: Please specify the purpose of your post."

    length_str = get_length_str(post_length)

    prompt = f"""
    🎯 **Generate a professional, engaging LinkedIn post.**
    
    🏆 **Post Context**: {post_reason}
    💼 **Profession**: {profession}
    🔹 **Topic**: {topic}
    📏 **Length**: {length_str}
    🔑 **Custom Keywords**: {custom_keywords if custom_keywords else "None"}

    📝 **Guidelines**:
    - Keep the post **engaging, professional, and insightful**.
    - If **Tanglish**, mix Tamil and English while ensuring readability in **English script**.
    - The post should be **authentic and valuable** to the audience.
    """

    try:
        # ✅ Retrieve relevant example posts
        examples = few_shot.get_filtered_posts(post_length, language, topic)
        if examples:
            prompt += "\n\n📌 **Example Writing Style**:\n"
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
    
    - Uses a structured manual format to ensure user still gets a useful post.
    - Tanglish posts are generated manually to ensure natural language flow.
    """

    length_str = get_length_str(post_length)

    if language == "English":
        fallback_template = f"""
        🚀 Exciting Update! 🚀

        As a **{profession}**, I’ve been exploring **{topic}** lately, and it's been an incredible journey!
        
        Whether it's **{post_reason}**, or simply a passion for continuous learning, this has been a rewarding experience.
        
        The field of {topic} is evolving rapidly, and I’m eager to keep up with new trends.
        
        What’s your take on {topic}? Let’s discuss! 💡 #CareerGrowth #Networking
        """

    else:  # Tanglish version
        fallback_template = f"""
        🚀 Vera Level Update! 🚀

        **{profession}** ah irunthu **{topic}** pathi kathukitu iruken, semma interesting journey da!  
        
        **{post_reason}** nu solli kathukitu poitu iruken, romba nalla experience!  
        
        **{topic}** ippo vera level ah maari iruku, update aganum nu try panren!  
        
        **Ungaloda opinion enna? Let's discuss!** 💡 #GrowthMindset #Networking
        """

    return fallback_template


def get_prompt(length, language, topic, profession, custom_keywords):
    """
    Constructs a detailed prompt for generating a LinkedIn post.

    - **length**: Short, Medium, or Long
    - **language**: English or Tanglish
    - **topic**: Topic of the post
    - **profession**: User's profession
    - **custom_keywords**: Additional keywords for post refinement

    Returns:
        A formatted prompt string.
    """

    length_str = get_length_str(length)

    prompt = f"""
    🎯 **Generate a LinkedIn post based on the following details**:

    🔹 **Topic**: {topic}
    📏 **Length**: {length_str}
    🌍 **Language**: {language}
    💼 **Profession**: {profession}
    🔑 **Custom Keywords**: {custom_keywords if custom_keywords else "None"}

    📝 **Guidelines**:
    - Ensure the post is **engaging, professional, and insightful**.
    - If **Tanglish**, mix Tamil and English while ensuring readability in **English script**.
    - The post should be **thought-provoking and relatable**.
    """

    # Retrieve relevant example posts
    examples = few_shot.get_filtered_posts(length, language, topic)
    if examples:
        prompt += "\n\n📌 **Example Writing Style**:\n"
        for i, post in enumerate(examples):
            prompt += f"\n\n**Example {i+1}:**\n{post['text']}"
            if i == 1:  # Limit to two examples
                break

    return prompt
