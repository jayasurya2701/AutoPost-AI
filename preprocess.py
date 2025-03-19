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

    with open(raw_file_path, encoding='utf-8') as file:
        posts = json.load(file)
        enriched_posts = []
        
        for post in posts:
            metadata = extract_metadata(post['text'])
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


def get_unified_tags(posts_with_metadata):
    """Unifies tags across all posts using an LLM."""

    unique_tags = set()

    # Extract all unique tags from posts
    for post in posts_with_metadata:
        unique_tags.update(post["tags"])  

    unique_tags_list = ",".join(unique_tags)

    template = '''  
    I will give you a list of tags. You need to unify them with the following rules:  
    1. Merge similar tags into a single category.  
       Example:  
          - "Fresh Graduates", "Recent Graduates" → "Freshers"  
          - "Job Hunting", "Job Search", "Applying for Jobs" → "Job Search"  
          - "Motivation", "Inspiration", "Career Motivation" → "Motivation"  
          - "Mental Health", "Job Search Anxiety", "Stress Management" → "Mental Health"  
          - "Networking", "Building Connections", "Professional Networking" → "Networking"  
          - "Self Improvement", "Personal Growth", "Career Growth" → "Self Improvement"  
          - "Rejections", "Job Rejections", "Application Rejections" → "Rejections"  
    2. Each tag should follow title case convention. Example: "Motivation", "Job Search"  
    3. Output should be a JSON object (no preamble) mapping original tags to unified tags.  
       Example:  
       {{"Fresh Graduates": "Freshers", "Job Hunting": "Job Search", "Motivation": "Motivation"}}  

    Here is the list of tags:  
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
    """Corrects common Tanglish spelling and pronunciation errors in generated text."""
    
    corrections = {
    # Common Tamil words with proper transliteration
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
    
    # Sentence flow improvements
    "nanri solluven": "nandri sollven",
    "periya impact": "periya effect",
    "romba tough": "romba kashtama",
    "mudiyala": "mudiyala",
    "seriya": "seriyaa",
    "mosamaana": "mosama",
    "nambunga": "nambunga daa",
    
    # Job-related phrases
    "resume nalla irukkanum": "resume nallaa irukanom",
    "apply pannuvinga": "apply pannunga",
    "call varuma": "call varuma?",
    "mail varuma": "mail varuma?",
    "kandippa work aagum": "kandippa velai vaanganom",
    "interview poganum": "interview ku poganum",
    "job search vera level stress": "job search periya stress",
    
    # Motivation and encouragement phrases
    "nambikkai irrukanum": "nambikkai irukanom",
    "try pannu da": "try pannunga daa",
    "pathu seeiya": "parthu sei",
    "thirupi try pannu": "thirumba try pannu",
    "oru naal win pannuvey": "oru naal jeipa ",
    
    # Conversational & Casual Corrections
    "bro, stress aayiduchu": "bro, stress aaiduchu",
    "sama kashtama": "romba kashtama",
    "nallavanga kita pesunga": "nallavanga kita pesunga bro",
    "veliya poitu varen": "veliya poitu varen",
    "podhum da": "podhum daa",
    "semma matter": "periya matter",
    "enna da nadakudhu": "enna daa nadakudhu",
    "evlo time agiduchu": "evlo neram aagiduchu",
    "irukura situation semma tough": "inga situation romba kashtama irruku",
    "summa time waste pannathe": "summa time waste pannadha bro",
    "kandippa try pannu da": "kandippa try pannunga daa",
    "yethuku stress eduthukka": "edhuku stress aaganom bro",
    "na solliten la": "naan solliten la",
    "aprum enna plan": "aprm enna plan bro",
    "semma confusion ah iruku": "romba confusion ah iruku",
    "kashtam but manage pannu": "kashtamaana situation but manage pannunga",
    "koodave irunga bro": "koodave irunga bro",
    "engaluku appdi lam onnum thevai illa": "engaluku appadi lam onnum thevai illa",
    "intha week kandippa busy ah irukum": "intha week kandippa busy aa irukum",
    "unnoda decision semma correct": "ungaloda decision nalla iruku bro",
    "nalla time pass aayidum": "nalla time pass aagum",
    "edhuku ivlo tension edukkura": "ethuku ivlo tension eduthukura",
    "evlo try pannalum use illa": "evlo try pannalum result illa",
    "parava illa da": "parava illa daa",
    "kandippa win panniduvom": "kandippa win pannuvom daa",
    "onnum periya matter illa bro": "onnum periya problem illa bro",
    "seri seri poi thoongu": "seri seri, poi thoonga",
    "chumma light ah eduthu": "chumma light ah eduthuko",
    "adhu unga future ku nalladhilla": "adhu unga future ku nalladhu illa bro",
    "sama happy aayiten": "romba sandhosama iruku",
    "over think pannathe": "overthink pannadha bro",
    "life la oru time try pannu": "life la one time try pannunga",
    "edhu nadanthaalum nalladhu than": "ethu nadandhaalum adhu nalladhuku dhan",
    "mokka topic ah pesathinga da": "mokka topic pesadhinga daa",
    "thirumba pesalam bro": "thirumba pesa lam bro",
    "neenga super bro": "neenga vera level bro",
    "indha mathiri kashtam ellam temporary": "intha maari kashtam temporary dhan bro",
    "paathu sollu da": "paathu sollu daa",
    "santhosha news bro": "super news bro",
    "edho oru feel iruku bro": "edho oru different feel ah iruku bro",
    "intha decision confirm ah best": "intha decision confirm ah nalla decision bro",
    "modhal la kashtama dhan irukum": "modhala kashtama dhan irukum",
    "positive mindset vachuko": "positive mindset vachikonga",
    "apadi nu think pannadha": "epdi nu think pannadha bro",
    "panra work la full focus pannu": "panra work la full focus pannunga",
    "seriya plan panni start pannu": "seriyaa plan panni start pannunga",
    "oru naal periya aagiduven": "oru naal periya aal ah aagiduvinga",
    "intha vishayam deep ah think pannu": "intha vishayam deep ah yosichu paaru",
    "evlo try pannalum set aagala": "evlo try pannalum set aagala bro",
    "apram ennada panrathu": "aprm enna bro panna pora",
    "thirumba start pannalama": "thirumba start pannalama bro",
    "ennamo correct ah theriyala": "ennamo correct ah theriyala bro",
    "correct ah decide pannu da": "correct ah decide pannunga daa",
    "kandippa next level povom": "kandippa next level povom bro",
    "romba naala free time illa": "romba naala free time illa bro",
    "edhuku ivlo feel pannura": "ethuku ivlo feel pannura bro",
    "current situation ku adjust pannu": "current situation ku adjust pannunga",
    "nenacha maari illa bro": "nenacha maari illa bro",
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
    "nallaa irundha pothum bro": "nallaa irundha pothum bro",
    "relax ah iru bro": "relax ah iru bro",
    "porumaiya iru bro": "porumaiya iru bro",
    "work speed aagiduchu": "work speed aagiduchu bro",
    "ellam set aagidum da": "ellam set aagidum daa"
    
    # Positive Affirmations & Productivity
    "nalla chance kedaikum": "nallaa chance kedaikum",
    "oru naal periya aagiduven": "oru naal periya aala aagiduvinga",
    "self-improvement mukkiyam": "self-improvement romba mukkiyam",
    "daily learn pannu": "daily learn pannu",
    
    # Networking & Communication
    "connect aagunga": "connect pannunga",
    "reply varuma": "reply varuma?",
    "DM pannu": "DM pannunga",
    "network build pannu": "network build pannunga",
    "speech improve pannu": "speech develop pannunga",
    
    # Common Encouragements
    "unakku kedaikum": "ungaluku kedaikum",
    "keep trying": "kadaisi varai poradu",
    "nalla pannunga": "nalla pannunga",
    "kastam vanthaa thaan growth": "kastam vanthaa thaan growth",
    "vayasu aayiduchu bro": "vayasu aaiduchu bro"",
}

    
    for wrong, correct in corrections.items():
        text = text.replace(wrong, correct)
    
    return text


if __name__ == "__main__":
    process_posts("data/raw.json", "data/processed_posts.json")
