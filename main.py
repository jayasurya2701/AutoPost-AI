import streamlit as st
import os
from few_shot import FewShotPosts
from post_generator import generate_post
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Sidebar for API Key input (hidden)
st.sidebar.header("🔐 Enter LLM API Key")
user_api_key = st.sidebar.text_input("API Key", type="password")

if user_api_key:
    os.environ["GROQ_API_KEY"] = user_api_key
    st.sidebar.success("✅ API Key Set Successfully!")
else:
    st.sidebar.warning("⚠️ Please enter your API key to generate posts.")

# 🏆 Profession categories & topics
professions = {
    "Technical": {
        "IT & Software Development": {
            "Software Developer": ["Coding", "Debugging", "Software Architecture","General Thoughts"],
            "Full Stack Developer": ["Frontend", "Backend", "APIs","General Thoughts"],
            "Mobile App Developer": ["iOS", "Android", "Flutter","General Thoughts"],
            "Game Developer": ["Unity", "Unreal Engine", "Game AI","General Thoughts"],
            "Embedded Systems Engineer": ["IoT", "Firmware", "Microcontrollers","General Thoughts"],
            "Blockchain Developer": ["Smart Contracts", "DeFi", "Cryptography","General Thoughts"],
            "Cybersecurity Specialist": ["PenTesting", "Encryption", "Zero Trust","General Thoughts"],
            "Cloud Engineer": ["AWS", "Azure", "GCP", "Kubernetes","General Thoughts"],
            "DevOps Engineer": ["CI/CD", "Infrastructure as Code", "Automation","General Thoughts"],
            "UI/UX Designer": ["User Experience", "Design Thinking", "Prototyping","General Thoughts"],
            "Open-Source Contributor": ["GitHub", "Collaboration", "Community","General Thoughts"]
        },
        "Artificial Intelligence & Machine Learning": {
            "AI Engineer": ["Generative AI", "LLMs", "Deep Learning","General Thoughts"],
            "Prompt Engineer": ["AI Prompting", "Fine-Tuning", "LLM Customization","General Thoughts"],
            "NLP Engineer": ["Text Analysis", "Chatbots", "Conversational AI","General Thoughts"],
            "Computer Vision Engineer": ["Image Processing", "Object Detection","General Thoughts"],
            "AI Research Scientist": ["Model Training", "Ethics", "ML Innovations","General Thoughts"],
            "Robotics Engineer": ["Automation", "AI Ethics", "Perception Systems","General Thoughts"],
            "AI Ethics Consultant": ["Fairness", "Bias Detection", "AI Policy","General Thoughts"]
        },
        "Cloud & DevOps": {
            "Cloud Solutions Architect": ["AWS", "Azure", "Hybrid Cloud","General Thoughts"],
            "Cloud Security Engineer": ["DevSecOps", "Compliance", "Zero Trust","General Thoughts"],
            "Site Reliability Engineer (SRE)": ["Observability", "Fault Tolerance","General Thoughts"],
            "Kubernetes Engineer": ["Microservices", "Scaling", "Containerization","General Thoughts"]
        },
        "Cybersecurity": {
            "Ethical Hacker": ["Hacking", "Phishing", "Red Teaming","General Thoughts"],
            "Security Engineer": ["SIEM", "Threat Intelligence", "Network Security","General Thoughts"],
            "Incident Response Analyst": ["Threat Mitigation", "Security Audits","General Thoughts"],
            "Cryptography Expert": ["Encryption", "Blockchain Security","General Thoughts"]
        },
        "Data Science & Analytics": {
            "Data Scientist": ["AI Models", "Big Data", "Predictive Analytics","General Thoughts"],
            "Data Engineer": ["ETL Pipelines", "Data Warehousing", "Cloud Storage","General Thoughts"],
            "Business Intelligence Analyst": ["BI Tools", "Data Visualization","General Thoughts"],
            "ML Engineer": ["MLOps", "Model Deployment", "Feature Engineering","General Thoughts"],
            "Bioinformatics Scientist": ["Genomics", "Computational Biology","General Thoughts"]
        }
    },
    "Healthcare & Medicine": {
        "Doctors & Physicians": {
            "General Practitioner": ["Diagnosis", "Patient Care", "Primary Health","General Thoughts"],
            "Surgeon": ["Surgical Innovations", "Medical Robotics","General Thoughts"],
            "Cardiologist": ["Heart Health", "Clinical Trials","General Thoughts"],
            "Neurologist": ["Brain Research", "Mental Health","General Thoughts"],
            "Oncologist": ["Cancer Research", "Precision Medicine","General Thoughts"]
        },
        "Healthcare Technology": {
            "Medical AI Researcher": ["AI in Healthcare", "Medical Imaging AI","General Thoughts"],
            "Telemedicine Specialist": ["Remote Consultations", "eHealth","General Thoughts"],
            "Biomedical Engineer": ["Medical Devices", "Prosthetics","General Thoughts"],
            "Pharmacovigilance Expert": ["Drug Safety", "Clinical Trials","General Thoughts"]
        },
        "Mental Health & Wellness": {
            "Psychologist": ["Therapy", "Mental Health Awareness","General Thoughts"],
            "Psychiatrist": ["Neuropharmacology", "Cognitive Science","General Thoughts"]
        }
    },
    "Engineering & Technology": {
        "Mechanical Engineering": {
            "Automotive Engineer": ["EV Technology", "Autonomous Vehicles","General Thoughts"],
            "Aerospace Engineer": ["Rocket Propulsion", "Space Tech","General Thoughts"],
            "Manufacturing Engineer": ["Lean Manufacturing", "3D Printing","General Thoughts"]
        },
        "Electrical & Electronics": {
            "Renewable Energy Engineer": ["Solar Tech", "Battery Storage","General Thoughts"],
            "Chip Design Engineer": ["Semiconductors", "FPGA","General Thoughts"],
            "Power Systems Engineer": ["Smart Grids", "Energy Efficiency","General Thoughts"]
        },
        "Civil & Structural Engineering": {
            "Structural Engineer": ["Earthquake Resistant Design", "Bridges","General Thoughts"],
            "Smart Cities Engineer": ["Urban Planning", "GreenTech","General Thoughts"]
        }
    },
    "Business & Finance": {
        "Entrepreneurship & Startups": {
            "Tech Startup Founder": ["Product Market Fit", "Angel Investment","General Thoughts"],
            "SaaS Founder": ["Subscription Models", "Scaling","General Thoughts"],
            "FinTech Innovator": ["Digital Banking", "DeFi","General Thoughts"],
            "EdTech Entrepreneur": ["AI Tutors", "Online Learning","General Thoughts"],
            "GreenTech Founder": ["Sustainability", "Carbon Neutrality","General Thoughts"]
        },
        "Marketing & Sales": {
            "Growth Hacker": ["Viral Marketing", "User Retention","General Thoughts"],
            "SEO Specialist": ["Google Ranking", "Keyword Optimization","General Thoughts"],
            "Social Media Manager": ["Brand Engagement", "Content Strategy","General Thoughts"],
            "Sales Executive": ["Negotiation", "Lead Generation","General Thoughts"]
        },
        "Finance & Investment": {
            "Financial Analyst": ["Stock Market", "Wealth Management","General Thoughts"],
            "Risk Manager": ["Portfolio Management", "Financial Compliance","General Thoughts"],
            "Cryptocurrency Analyst": ["Bitcoin Trends", "NFT Market","General Thoughts"]
        }
    },
    "Legal & Government": {
        "Law & Compliance": {
            "Corporate Lawyer": ["Mergers & Acquisitions", "IP Law","General Thoughts"],
            "Human Rights Lawyer": ["Ethical Justice", "Advocacy","General Thoughts"],
            "Legal Tech Consultant": ["AI in Law", "Blockchain Contracts","General Thoughts"]
        },
        "Government & Public Policy": {
            "IAS Officer": ["Policy Implementation", "Governance","General Thoughts"],
            "Diplomat": ["Foreign Relations", "International Trade","General Thoughts"],
            "Urban Planner": ["Smart Cities", "Public Transportation","General Thoughts"]
        }
    },
    "Media, Design & Arts": {
    "Media & Journalism": {
        "Investigative Journalist": ["Political Reporting", "Fact Checking", "Breaking News","General Thoughts"],
        "Podcaster": ["Audio Content", "Storytelling", "Engagement Strategies","General Thoughts"],
        "Public Relations Expert": ["Brand Management", "Crisis Handling", "Media Outreach","General Thoughts"]
    },
    "Content Creation & Digital Media": {
        "YouTuber": ["Video Content", "Subscriber Growth", "Monetization","General Thoughts"],
        "Social Media Influencer": ["Instagram Growth", "Reels/TikTok Strategies", "Brand Collabs","General Thoughts"],
        "Content Creator": ["Content Strategy", "Engagement Metrics", "Niche Selection","General Thoughts"],
        "Live Streamer (Twitch, YouTube, Kick)": ["Gaming", "Live Interaction", "Sponsorships","General Thoughts"]
    },
    "Video Editing & Production": {
        "Video Editor": ["Adobe Premiere Pro", "Final Cut Pro", "Post-Production","General Thoughts"],
        "Motion Graphics Artist": ["After Effects", "3D Animation", "Visual Effects","General Thoughts"],
        "Cinematographer": ["Camera Techniques", "Lighting", "Color Grading","General Thoughts"],
        "Film Director": ["Scriptwriting", "Storyboarding", "Directing Actors","General Thoughts"]
    },
    "Graphic Design & Animation": {
        "Graphic Designer": ["Typography", "Illustration", "Branding","General Thoughts"],
        "3D Animator": ["Blender", "Maya", "CGI & VFX","General Thoughts"],
        "UI/UX Designer": ["Wireframes", "Prototyping", "User Interaction","General Thoughts"]
    },
    "Gaming Industry & Esports": {
        "Game Designer": ["Level Design", "Narrative Development", "Game Mechanics","General Thoughts"],
        "Esports Manager": ["Competitive Gaming", "Sponsorships", "Team Management","General Thoughts"],
        "Gaming Content Creator": ["Let’s Plays", "Game Streaming", "Twitch Growth","General Thoughts"]
    }
},
    "Freelancing & Remote Work": {
        "Freelance Tech": {
            "Freelance Developer": ["Remote Work", "Client Management","General Thoughts"],
            "Freelance UX Designer": ["Wireframes", "Prototyping","General Thoughts"],
            "Freelance Cybersecurity Consultant": ["Pen Testing", "Data Privacy","General Thoughts"]
        },
        "Freelance Creative": {
            "Freelance Writer": ["SEO Blogs", "Ghostwriting","General Thoughts"],
            "Freelance Photographer": ["Photo Editing", "Composition","General Thoughts"],
            "Freelance Filmmaker": ["Short Films", "Content Monetization","General Thoughts"]
        }
    },
    
    "Personal Growth": {
        "Motivation": ["Inspiration", "Self Improvement", "Growth Mindset"],
        "Mental Health": ["Job Search Anxiety", "Stress Management", "Work-Life Balance"],
        "Networking": ["Building Connections", "Professional Networking", "Socializing"],
        "Rejections": ["Job Rejections", "Application Rejections", "Interview Failures"],
        "Leadership": ["Decision Making", "Team Management", "Public Speaking"],
        "Productivity": ["Time Management", "Focus Strategies", "Deep Work"],
        "Personal Branding": ["LinkedIn Growth", "Content Creation", "Online Influence"],
        "Critical Thinking": ["Problem Solving", "Logical Reasoning", "Debate"],
        "Confidence Building": ["Overcoming Fear", "Self-Expression", "Public Speaking"],
        "Emotional Intelligence": ["Handling Criticism", "Resilience", "Self-Awareness"],
        "Mindset Mastery": ["Stoicism", "Growth Mindset", "Mental Toughness"]
    }
}

# 🎯 **Why This Post is Generated** (Context)
post_reasons = [
    # ✅ Career Achievements & Milestones
    "Completed a Course",
    "Achieved an Internship",
    "Landed a New Job",
    "Got a Promotion",
    "Transitioned to a New Industry",
    "Started a Side Hustle",
    "Won a Hackathon",
    "Reached a Career Milestone",
    "Started My Own Business",
    "Secured a Major Deal or Client",
    "Reached a New Certification Level",
    "Spoke at an Industry Event",
    "Graduated from College or University",
    "Completed a Professional Certification",
    "Started a New Leadership Role",
    "Announcing My Resignation & Next Steps",
    "Completed a Significant Project",
    
    # ✅ Industry Insights & Thought Leadership
    "Sharing Industry Insights",
    "Sharing Research & Innovations",
    "Providing a Market Trend Analysis",
    "Commenting on Emerging Technologies",
    "Breaking Down a Complex Topic for Beginners",
    "Debunking a Common Myth in My Industry",
    "Sharing a Recent Study or Whitepaper",
    "Explaining Lessons from a Past Experience",
    
    # ✅ Personal Growth & Reflection
    "Personal Reflection & Growth",
    "Sharing a Lesson from My Career",
    "Overcoming a Major Challenge",
    "How I Recovered from Failure",
    "Lessons from a Recent Setback",
    "What I Would Tell My Younger Self",
    "Discussing Work-Life Balance",
    "My Journey in Personal Branding",
    "What I Learned from Changing Industries",
    
    # ✅ Team & Community Engagement
    "Celebrating a Team Achievement",
    "Giving Back to the Community",
    "Announcing a Volunteering Experience",
    "Recognizing a Mentor or Role Model",
    "Expressing Gratitude to My Network",
    "Launching a Mentorship Initiative",
    "Supporting a Social Cause or Movement",
    "Highlighting an Inspiring Colleague",
    "Showcasing a Collaborative Effort",
    
    # ✅ Events, Speaking & Public Recognition
    "Speaking at an Industry Conference",
    "Participating in a Panel Discussion",
    "Attending a Major Networking Event",
    "Recognizing an Award or Honor",
    "Getting Featured in Media or Articles",
    "Publishing My First (or Latest) Article",
    "Hosting a Webinar or Workshop",
    "Launching a New Podcast or YouTube Series",
    "Guest Appearing on a Podcast",
    
    # ✅ Company & Organizational Updates
    "Announcing My Company’s Growth",
    "Sharing My Company’s New Product Launch",
    "Introducing a New Initiative at Work",
    "Highlighting My Organization’s Culture",
    "Encouraging People to Join My Company",
    "Welcoming New Team Members",
    "Announcing a Company Achievement",
    
    # ✅ Job Search & Career Development
    "Sharing My Job Search Experience",
    "Seeking Career Advice from My Network",
    "Announcing an Open Job Position",
    "Asking for Referrals or Recommendations",
    "My Experience with Job Interviews",
    "Discussing Salary Negotiations",
    
    # ✅ Freelancing & Entrepreneurship
    "Announcing My Freelance Journey",
    "Launching a New Service or Offering",
    "Explaining How I Got My First Client",
    "Lessons from Building My Own Business",
    "How I Handle Client Relationships",
    
    # ✅ Productivity & Work Strategies
    "Sharing My Daily Productivity Routine",
    "Discussing Time Management Hacks",
    "How I Improved My Work-Life Balance",
    "Breaking Down My Workflow & Tools",
    
    # ✅ Challenges, Failures & Real Talk
    "What No One Talks About in My Industry",
    "Lessons from My Biggest Career Mistake",
    "How I Bounced Back from a Layoff",
    "When Things Didn't Go as Planned",
    
    # ✅ Celebrating Others & Engaging the Network
    "Congratulating Someone in My Network",
    "Asking My Network a Thought-Provoking Question",
    "Highlighting an Underrated Industry Trend",
    "Thanking Someone for Their Help",
]

# Post Length & Language Options
length_options = ["Short", "Medium", "Long"]
language_options = ["English", "Tanglish"]

# **Main Function**
def main():
    """Renders the Streamlit UI for generating LinkedIn posts."""
    st.subheader("🚀 LinkedIn Post Generator")
    fs = FewShotPosts()

    # ✅ Ensure session state is initialized
    if "selected_category" not in st.session_state:
        st.session_state["selected_category"] = list(professions.keys())[0]

    if "selected_subcategory" not in st.session_state:
        st.session_state["selected_subcategory"] = ""

    if "selected_profession" not in st.session_state:
        st.session_state["selected_profession"] = ""

    if "selected_reason" not in st.session_state:
        st.session_state["selected_reason"] = post_reasons[0]

    # **Horizontal Layout**
    col1, col2, col3 = st.columns(3)

    with col1:
        selected_category = st.selectbox("📂 Select Category:", options=list(professions.keys()), 
                                         index=list(professions.keys()).index(st.session_state["selected_category"]))
        st.session_state["selected_category"] = selected_category  # Update session state

    # **Handling "Personal Growth" category separately**
    if selected_category == "Personal Growth":
        topics = list(professions[selected_category].keys())
        selected_topic = st.selectbox("🎯 Select a Discussion Topic:", options=topics)
        selected_language = st.selectbox("📝 Select Language:", options=language_options)
        selected_reason = st.selectbox("🤔 Why is this post generated?", options=post_reasons)

        col4, col5 = st.columns([1, 3])
        with col4:
            selected_length = st.radio("📏 Select Post Length:", options=length_options, horizontal=True)
        with col5:
            custom_keywords = st.text_input("🔑 Add Specific Keywords (Optional)", "")

        # ✅ **Generate Post**
        if st.button("⚡ Generate Post"):
            post = generate_post(selected_length, selected_language, selected_topic, "Personal Growth", custom_keywords, selected_reason)
            st.write(post)

        return  # **Exit here** since subcategory/profession isn't needed for "Personal Growth"

    # **For other categories (Technical, Business, etc.)**
    with col2:
        subcategories = list(professions[selected_category].keys())
        selected_subcategory = st.selectbox("📁 Select Subcategory:", options=subcategories, 
                                            index=subcategories.index(st.session_state["selected_subcategory"]) if st.session_state["selected_subcategory"] in subcategories else 0)
        st.session_state["selected_subcategory"] = selected_subcategory

    with col3:
        professions_list = list(professions[selected_category][selected_subcategory].keys()) if selected_subcategory in professions[selected_category] else []
        selected_profession = st.selectbox("💼 Select Your Profession:", options=professions_list,
                                           index=professions_list.index(st.session_state["selected_profession"]) if st.session_state["selected_profession"] in professions_list else 0)
        st.session_state["selected_profession"] = selected_profession

    # **Align Topic & Language Selection**
    col4, col5 = st.columns(2)

    with col4:
        topics = professions[selected_category][selected_subcategory].get(selected_profession, ["General Thoughts"])
        selected_topic = st.selectbox("🎯 Select a Discussion Topic:", options=topics)

    with col5:
        selected_language = st.selectbox("📝 Select Language:", options=language_options)

    # **Why This Post is Generated**
    selected_reason = st.selectbox("🤔 Why is this post generated?", options=post_reasons)

    # **Post Length & Keywords**
    col6, col7 = st.columns([1, 3])

    with col6:
        selected_length = st.radio("📏 Select Post Length:", options=length_options, horizontal=True)

    with col7:
        custom_keywords = st.text_input("🔑 Add Specific Keywords (Optional)", "")

    # ✅ **Generate Post**
    if st.button("⚡ Generate Post"):
        post = generate_post(selected_length, selected_language, selected_topic, selected_profession, custom_keywords, selected_reason)
        st.write(post)

if __name__ == "__main__":
    main()
