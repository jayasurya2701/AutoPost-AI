import json
import os
import time
import random
from llm_helper import llm
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException


def process_posts(raw_file_path, processed_file_path=None):
    """Processes LinkedIn posts by extracting metadata, unifying tags, and correcting Tanglish spelling."""
    
    # Check if raw file exists
    if not os.path.exists(raw_file_path):
        raise FileNotFoundError(f"File not found: {raw_file_path}")

    with open(raw_file_path, encoding="utf-8") as file:
        posts = json.load(file)
        enriched_posts = []
        
        for post in posts:
            metadata = extract_metadata(post["text"])
            post_with_metadata = post | metadata
            
            # Apply Tanglish correction if the post is identified as Tanglish
            if post_with_metadata["language"].lower() == "tanglish":
                post_with_metadata["text"] = correct_tanglish_spelling(post_with_metadata["text"])

            enriched_posts.append(post_with_metadata)

    # Get unified tags mapping
    unified_tags = get_unified_tags(enriched_posts)

    # Replace tags in posts using unified mapping
    for post in enriched_posts:
        current_tags = post["tags"]
        new_tags = {unified_tags.get(tag, tag) for tag in current_tags}  # Use .get(tag, tag) to avoid KeyError
        post["tags"] = list(new_tags)

    # Save processed posts
    with open(processed_file_path, mode="w", encoding="utf-8") as outfile:
        json.dump(enriched_posts, outfile, indent=4)


def extract_metadata(post):
    """Extracts metadata (line count, language, and tags) from a LinkedIn post using LLM."""
    
    template = '''
    You are given a LinkedIn post. You need to extract number of lines, language of the post, and tags.
    1. Return a valid JSON. No preamble. 
    2. JSON object should have exactly three keys: line_count, language, and tags. 
    3. tags is an array of text tags. Extract a maximum of two tags.
    4. Language should be English or Tanglish (Tanglish means Tamil + English).
    5. Relevant profession (if applicable) from: Student, IAS Officer, Lawyer, Cloud Engineer, AI Engineer, Fresher, Data Scientist, Entrepreneur, Doctor, Marketer, etc.
    
    Here is the actual post:
    {post}
    '''

    pt = PromptTemplate.from_template(template)
    chain = pt | llm

    response = retry_invoke(chain, {"post": post})  # Use retry logic

    try:
        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content)
    except OutputParserException:
        raise OutputParserException("Context too big. Unable to parse post metadata.")

    return res

def enhance_post_with_profession(text, profession):
    """Enhances post content with domain-specific insights."""

    profession_keywords = {
        "Student": ["career growth", "learning mindset", "internships"],
        "AI Engineer": ["machine learning", "deep learning", "LLMs"],
        "Cloud Engineer": ["AWS", "scalability", "Kubernetes"],
        "Entrepreneur": ["startup success", "funding", "growth hacking"],
        "Doctor": ["medical AI", "patient care", "health tech"],
        "Lawyer": ["legal insights", "case studies", "justice system"],
        "Fresher": ["resume tips", "job search", "first job advice"]
    }

    if profession in profession_keywords:
        text += f"\n\n💡 Key Insights for {profession}: " + ", ".join(profession_keywords[profession])

    return text

def get_unified_tags(posts_with_metadata):
    """Unifies tags across all posts using an LLM."""

    unique_tags = set()

    # Extract all unique tags from posts
    for post in posts_with_metadata:
        unique_tags.update(post["tags"])  

    unique_tags_list = ",".join(unique_tags)

    template = '''  
    You are given a list of tags. Your task is to unify them into broader categories using the following rules:  

    🔹 **Rules for Tag Unification:**  
    1️⃣ Merge similar tags into a single standardized category.  
       - Example:  
          - "Fresh Graduates", "Recent Graduates" → **"Freshers"**  
          - "Job Hunting", "Job Search", "Applying for Jobs" → **"Job Search"**  
          - "Motivation", "Inspiration", "Career Motivation" → **"Motivation"**  
          - "Mental Health", "Job Search Anxiety", "Stress Management" → **"Mental Health"**  
          - "Networking", "Building Connections", "Professional Networking" → **"Networking"**  
          - "Self Improvement", "Personal Growth", "Career Growth" → **"Self Improvement"**  
          - "Rejections", "Job Rejections", "Application Rejections" → **"Rejections"**  
    2️⃣ Each tag should follow **Title Case formatting** (e.g., "Job Search" instead of "job search").  
    3️⃣ Return a **valid JSON object** mapping original tags to unified tags.  
       Example Output Format:  
       ```json
       {{"Fresh Graduates": "Freshers", "Job Hunting": "Job Search", "Motivation": "Motivation"}}
       ```

    **List of Tags:**  
    {tags}
    '''  

    pt = PromptTemplate.from_template(template)
    chain = pt | llm

    response = retry_invoke(chain, {"tags": str(unique_tags_list)})  # Use retry logic

    try:
        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content)
    except OutputParserException:
        raise OutputParserException("Context too big. Unable to parse unified tags.")

    return res


def retry_invoke(chain, input_data, max_retries=3):
    """Retries the LLM call with exponential backoff to handle rate limits."""
    
    for attempt in range(max_retries):
        try:
            response = chain.invoke(input=input_data)
            return response
        except Exception as e:
            print(f"Attempt {attempt+1} failed: {e}")
            time.sleep(2 ** attempt + random.uniform(0, 1))  # Exponential backoff

    raise Exception("Max retries reached")


def correct_tanglish_spelling(text):
    """Corrects common Tanglish spelling and pronunciation errors."""
    
    corrections = {
        "ungalukku": "ungaluku",
        "pannuvaanga": "pannuvinga",
        "support pannuvaanga": "support pannuvanga",
        "irukku": "iruku",
        "kastama": "kashtama",
        "urupada": "urupada",
        "periya": "periya",
        "enna": "enna",
        "thevai": "thevai",
        "nalla": "nallaa",
        "venum": "venum",
        "resume nalla irukkanum": "resume nallaa irukanom",
        "apply pannuvinga": "apply pannunga",
        "call varuma": "call varuma?",
        "job search vera level stress": "job search periya stress",
        "nambikkai irrukanum": "nambikkai irukanom",
        "try pannu da": "try pannunga daa",
        "thirupi try pannu": "thirumba try pannu",
        "oru naal win pannuvey": "oru naal jeipa",
        "bro, stress aayiduchu": "bro, stress aaiduchu",
        "sama kashtama": "romba kashtama",
        "parava illa da": "parava illa daa",
        "santhosha news bro": "super news bro",
        "correct ah decide pannu da": "correct ah decide pannunga daa",
        "kandippa next level povom": "kandippa next level povom bro",
        "romba naala free time illa": "romba naala free time illa bro",
    }

    for wrong, correct in corrections.items():
        text = text.replace(wrong, correct)
    
    return text


if __name__ == "__main__":
    process_posts("data/raw.json", "data/processed_posts.json")
