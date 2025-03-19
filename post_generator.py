from llm_helper import llm
from few_shot import FewShotPosts

# Import Tanglish spelling correction function
from preprocess import correct_tanglish_spelling  

few_shot = FewShotPosts()


def get_length_str(length):
    if length == "Short":
        return "1 to 5 lines"
    if length == "Medium":
        return "6 to 10 lines"
    if length == "Long":
        return "11 to 15 lines"


def generate_post(length, language, tag):
    from preprocess import correct_tanglish_spelling  # Lazy import

    prompt = get_prompt(length, language, tag)
    response = llm.invoke(prompt)

    if language.lower() == "tanglish":
        return correct_tanglish_spelling(response.content)

    return response.content



def get_prompt(length, language, tag):
    length_str = get_length_str(length)

    # Base Prompt
    prompt = f"""
    Generate a LinkedIn post using the below information. No preamble.

    1) Topic: {tag}
    2) Length: {length_str}
    3) Language: {language}
    If Language is Tanglish, then it is a mix of Tamil and English. 
    The script for the generated post should always be in English.
    """

    # Fetch few-shot examples based on previous LinkedIn posts
    examples = few_shot.get_filtered_posts(length, language, tag)

    if len(examples) > 0:
        prompt += "\n\n4) Use the writing style as per the following examples."

    for i, post in enumerate(examples):
        post_text = post["text"]
        prompt += f"\n\nExample {i+1}: \n\n{post_text}"

        if i == 1:  # Use max two samples
            break

    # Improve Tanglish output by enforcing clear spelling rules
    if language.lower() == "tanglish":
        prompt += """
        
        5) Follow this Tanglish writing style strictly:

        ✅ Use simple, clear English words mixed with Tamil phrases.
        ✅ Always spell Tamil words in the most **phonetic and readable way**.
        ✅ **Avoid complex Tamil words** that don't transliterate well.
        ✅ **Use natural conversational flow**, like how native speakers text.
        ✅ **Maintain correct spelling and pronunciation**.

        Example 1:
        "Job search vera level stress da! 😩  
        Call varuma nu wait panna, mail varuma nu check panna, last la ‘We regret to inform you’ nu oru mail.  
        Aana keep going! One rejection doesn’t define your future. Un effort kandippa result kudukum! 🔥  
        Oru naal, neeyum ‘We’re happy to offer you the position’ nu read pannuvey. 💪"

        Example 2:
        "Networking panna kashtama iruku nu oru feeling. 😩  
        Aana bro, romba simple.  
        1. DM panna oru 'Hi' sollu.  
        2. Interest iruka field la leaders oda post la engage pannu.  
        3. Calls, webinars la participate pannu.  
        Oru naal unga name therinja, opportunities varum. 🚀"

        Now, generate a new LinkedIn post in the **same Tanglish style**, keeping spelling and pronunciation correct.
        """

    return prompt


if __name__ == "__main__":
    print(generate_post("Medium", "Tanglish", "Job Search"))
