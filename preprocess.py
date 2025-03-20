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
            post_with_metadata = {**post, **metadata}  # Correct syntax for dictionary merging
            
            # Apply Tanglish correction if the post is identified as Tanglish
            if post_with_metadata["language"].lower() == "tanglish":
                post_with_metadata["text"] = correct_tanglish_spelling(post_with_metadata["text"])

            # Enhance post with profession-based content
            profession = post_with_metadata.get("profession", "General")
            post_with_metadata["text"] = enhance_post_with_profession(post_with_metadata["text"], profession)

            enriched_posts.append(post_with_metadata)

    # Get unified tags mapping
    unified_tags = get_unified_tags(enriched_posts)

    # Replace tags in posts using unified mapping
    for post in enriched_posts:
        current_tags = post["tags"]
        new_tags = {unified_tags.get(tag, tag) for tag in current_tags}  
        post["tags"] = list(new_tags)

    # Save processed posts
    with open(processed_file_path, mode="w", encoding="utf-8") as outfile:
        json.dump(enriched_posts, outfile, indent=4)


def extract_metadata(post):
    """Extracts metadata (line count, language, profession, and tags) from a LinkedIn post using LLM."""
    
    template = '''
    You are given a LinkedIn post. Extract:
    1. Number of lines.
    2. Language (English or Tanglish).
    3. Relevant profession (if applicable) from: Student, IAS Officer, Lawyer, Cloud Engineer, AI Engineer, Fresher, Data Scientist, Entrepreneur, Doctor, Marketer, etc.
    4. Extract 2-3 relevant tags.

    Output in JSON format with fields: line_count, language, profession, tags.
    
    Here is the actual post:
    {post}
    '''

    pt = PromptTemplate.from_template(template)
    chain = pt | llm

    response = retry_invoke(chain, {"post": post})  

    try:
        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content)
    except OutputParserException:
        raise OutputParserException("Context too big. Unable to parse post metadata.")

    return res


def enhance_post_with_profession(text, profession):
    """Enhances LinkedIn post content with domain-specific insights."""

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

    for post in posts_with_metadata:
        unique_tags.update(post["tags"])  

    unique_tags_list = ", ".join(sorted(unique_tags))  

    template = '''  
    Unify the following LinkedIn tags based on similar meanings. Merge redundant ones into broader categories:
    {tags}  
    Output in JSON format mapping original tags to unified tags.
    '''  

    pt = PromptTemplate.from_template(template)
    chain = pt | llm

    response = retry_invoke(chain, {"tags": unique_tags_list})

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
            time.sleep(2 ** attempt + random.uniform(0, 1))  

    raise Exception("Max retries reached")


def correct_tanglish_spelling(text):
    """Corrects Tanglish spelling and ensures phonetic readability."""

    corrections = {
        # Common Tamil words with correct transliteration
        "ungalukku": "ungaluku",
        "pannuvaanga": "pannuvanga",
        "support pannuvaanga": "support pannuvanga",
        "irukku": "iruku",
        "kastama": "kashtama",
        "thevai": "thevai",
        "nalla": "nalla",
        "venum": "venum",
        "resume nalla irukkanum": "resume nallaa irukanom",
        "job search vera level stress": "job search periya stress",
        "try pannu da": "try pannunga daa",
        "bro, stress aayiduchu": "bro, stress aagudhu",
        "sama kashtama": "romba kashtama",
        "parava illa da": "parava illa daa",
        "santhosha news bro": "super news bro",
        "correct ah decide pannu da": "correct ah decide pannunga daa",
        "kandippa next level povom": "kandippa next level povom bro",
        "romba naala free time illa": "romba naala free time illa bro",
        "veliya poitu varen": "veliya poitu varen",
        "podhum da": "podhum daa",
        "kashtam but manage pannu": "kashtamaana situation dhan but manage pannunga",
        "intha decision confirm ah best": "intha decision confirm ah nalla decision bro",
        "modhal la kashtama dhan irukum": "modhala kashtama dhan irukum",
        "positive mindset vachuko": "positive mindset vachikonga",
        "thirumba start pannalama": "thirumba start pannalama bro",
        "correct ah decide pannu da": "correct ah decide pannunga daa",
        "chumma light ah eduthu": "chumma light ah eduthuko",
        
        # Job-related corrections
        "apply pannuvinga": "apply pannunga",
        "call varuma": "call varuma?",
        "mail varuma": "mail varuma?",
        "kandippa work aagum": "kandippa velai vaanganom",
        "interview poganum": "interview ku poganum",
        "job search romba tough": "job search periya challenge",
        "work pressure semma high": "work pressure romba high",
        "company la set aagiduven": "company la adjust aagiduven",
        
        # Motivation and encouragement phrases
        "nambikkai irrukanum": "nambikkai irukanom",
        "pathu seeiya": "parthu pannu",
        "thirupi try pannu": "thirumba try pannu",
        "oru naal win pannuvey": "oru naal jeipa",
        "oru naal periya aagiduven": "oru naal periya aal aagiduvom",
        "kastam vanthaa thaan growth": "kashtam vantha than growth",
        "mokka pesatha bro": "mokka podadha bro",
        "stress eduthukkama work pannu": "stress eduthukkama work pannunga",
        
        # Conversational & Casual corrections
        "bro evlo stress aayiduchu": "bro romba stress aaiduchu",
        "sama kashtama iruku da": "romba kashtama iruku daa",
        "parava illa bro": "parava illa daa",
        "ennada nadakudhu": "enna daa nadakudhu",
        "evlo time aagiduchu": "evlo neram aagiduchu",
        "nallavanga kita pesunga": "nallavanga kita pesunga bro",
        "edhuku ivlo tension edukkura": "ethuku ivlo tension aagura",
        "evlo try pannalum set aagala": "evlo try pannalum set aagala bro",
        "aprum enna panrathu": "aprm enna bro panna pora",
        "semma matter da": "mukkiyamana vishyam da",
        "na solliten la": "naan solliten la",
        "apdi nu think pannadha": "epdi nu think pannadha bro",
        "panra work la full focus pannu": "panra work la full focus pannunga",
        "seri seri poi thoongu": "seri seri, poi thoongu",
        "thirumba start pannalama": "thirumba start pannalama bro",
        "ennamo correct ah theriyala": "ennamo correct ah therila bro",
        "kandippa next level povom": "kandippa next level povom bro",
        "romba naala free time illa": "romba naala free time illa bro",
        "current situation ku adjust pannu": "current situation ku adjust pannunga",
        "padikka try pannu": "padikka try pannunga",
        "intha time la stress eduthukkama iru": "intha time la stress eduthukama iru bro",
        "situation la nallaa handle pannu": "intha situation la nallaa handle pannunga",
        "pudhu plan start pannu": "pudhu plan start pannunga",
        "sama jolly ah iruku bro": "romba jolly ah iruku bro",
        "day by day improve aagunga": "daily improve aagunga",
        "chumma doubt tha bro": "chumma doubt dhan bro",
        "simple ah think pannu": "simple ah yosichu paaru",
        "thirumba yosika vendam": "thirumba yosikadha bro",
        "full tension da": "full tension daa",
        "nallaa irundha pothum bro": "nalla irundha pothum bro",
        "relax ah iru bro": "relax ah iru bro",
        "porumaiya iru bro": "porumaiya iru bro",
        "work speed aagiduchu": "work speed aagiduchu bro",
        "ellam set aagidum da": "ellam set aagidum daa",
        
        # Positive Affirmations & Productivity
        "nalla chance kedaikum": "nallaa chance kedaikum",
        "self-improvement mukkiyam": "self-improvement romba mukkiyam",
        "daily learn pannu": "daily learn pannu",
        
        # Networking & Communication
        "connect aagunga": "connect pannunga",
        "reply varuma": "reply varuma?",
        "DM pannu": "DM pannunga",
        "network build pannu": "network build pannunga",
        "speech improve pannu": "speech develop pannunga"
    }
    
    for wrong, correct in corrections.items():
        text = text.replace(wrong, correct)

    return text


if __name__ == "__main__":
    process_posts("data/raw.json", "data/processed_posts.json")
