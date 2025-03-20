from llm_helper import llm
from few_shot import FewShotPosts
from preprocess import correct_tanglish_spelling

few_shot = FewShotPosts()

def get_length_str(length):
    if length == "Short":
        return "1 to 5 lines"
    if length == "Medium":
        return "6 to 10 lines"
    if length == "Long":
        return "11 to 15 lines"

def generate_post(length, language, tag, profession, keywords):
    prompt = get_prompt(length, language, tag, profession, keywords)
    response = llm.invoke(prompt)

    # Apply correction if the output is in Tanglish
    if language.lower() == "tanglish":
        return correct_tanglish_spelling(response.content)

    return response.content

def get_prompt(length, language, tag, profession, keywords):
    length_str = get_length_str(length)

    prompt = f"""
    Generate a LinkedIn post based on the following details:

    1️⃣ **Topic**: {tag}
    2️⃣ **Length**: {length_str}
    3️⃣ **Language**: {language}
    4️⃣ **Profession**: {profession}
    5️⃣ **Keywords**: {keywords if keywords else "None"}

    🎯 If Language is Tanglish, write in a mix of Tamil and English but ensure readability in **English script**.
    💡 The post should be **engaging, professional, and relatable**.
    🔥 Use a **casual yet impactful tone**.

    ---
    """

    examples = few_shot.get_filtered_posts(length, language, tag)

    if len(examples) > 0:
        prompt += "📌 **Example Writing Style**:"

    for i, post in enumerate(examples):
        post_text = post["text"]
        prompt += f"\n\n**Example {i+1}:**\n{post_text}"

        if i == 1:  # Use max two samples
            break

    return prompt
