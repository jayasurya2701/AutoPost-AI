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
        A generated LinkedIn post as a string or an error message.
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

        # ✅ Handle empty response
        if not response:
            return "⚠️ Error: No response received from LLM!"

        # ✅ Apply Tanglish Spelling Correction (if needed)
        if language == "Tanglish":
            response = correct_tanglish_spelling(response)

        return response

    except Exception as e:
        return f"⚠️ Error generating post: {str(e)}"


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
