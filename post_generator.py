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


def generate_post(post_length, language, topic, profession, custom_keywords="", post_reason=""):
    """
    Generates a LinkedIn post based on user inputs.
    
    - **post_length**: Short, Medium, or Long
    - **language**: English or Tanglish
    - **topic**: The subject of the post
    - **profession**: User's selected profession
    - **custom_keywords**: Additional keywords to fine-tune the post
    - **post_reason**: Context for why this post is being generated

    Returns:
        A generated LinkedIn post as a string.
    """

    length_str = get_length_str(post_length)

    prompt = f"""
    📌 **Generate a professional and engaging LinkedIn post.**  
    🎯 **Post Context**: {post_reason}  
    💼 **Profession**: {profession}  
    🔹 **Topic**: {topic}  
    📏 **Length**: {length_str}  
    🔑 **Custom Keywords**: {custom_keywords if custom_keywords else "None"}  

    📢 **Guidelines**:
    - Ensure the tone is **engaging, professional, and relatable**.
    - If language is **Tanglish**, mix Tamil and English but keep readability in **English script**.
    - The post should be **authentic**, valuable, and suitable for LinkedIn.
    """

    # Generate post using LLM (assuming `llm.generate` exists)
    response = llm.generate(prompt)

    # Correct spelling for Tanglish (if applicable)
    if language == "Tanglish":
        response = correct_tanglish_spelling(response)

    return response


def get_prompt(length, language, tag, profession, keywords):
    """
    Constructs a detailed prompt for generating a LinkedIn post.
    
    - **length**: Short, Medium, or Long
    - **language**: English or Tanglish
    - **tag**: Topic of the post
    - **profession**: User's profession
    - **keywords**: Custom keywords for post refinement

    Returns:
        A formatted prompt string.
    """

    length_str = get_length_str(length)

    prompt = f"""
    📌 **Generate a LinkedIn post based on the following details**:

    1️⃣ **Topic**: {tag}
    2️⃣ **Length**: {length_str}
    3️⃣ **Language**: {language}
    4️⃣ **Profession**: {profession}
    5️⃣ **Custom Keywords**: {keywords if keywords else "None"}

    📢 **Guidelines**:
    - Keep the post **engaging, professional, and insightful**.
    - If **Tanglish**, mix Tamil and English while maintaining readability in **English script**.
    - The post should be **thought-provoking and relatable**.
    
    ---
    """

    # Retrieve relevant example posts
    examples = few_shot.get_filtered_posts(length, language, tag)

    if examples:
        prompt += "📌 **Example Writing Style**:\n"
    
    for i, post in enumerate(examples):
        post_text = post["text"]
        prompt += f"\n\n**Example {i+1}:**\n{post_text}"

        if i == 1:  # Limit to two examples
            break

    return prompt
