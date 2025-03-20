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
            "Full Stack Developer": ["Frontend", "Backend", "APIs"],
            "Mobile App Developer": ["iOS", "Android", "Flutter"],
            "Game Developer": ["Unity", "Unreal Engine", "Game AI"],
            "Embedded Systems Engineer": ["IoT", "Firmware", "Microcontrollers"],
            "Blockchain Developer": ["Smart Contracts", "DeFi", "Cryptography"],
            "Cybersecurity Specialist": ["PenTesting", "Encryption", "Zero Trust"],
            "Cloud Engineer": ["AWS", "Azure", "GCP", "Kubernetes"],
            "DevOps Engineer": ["CI/CD", "Infrastructure as Code", "Automation"],
            "UI/UX Designer": ["User Experience", "Design Thinking", "Prototyping"],
            "Open-Source Contributor": ["GitHub", "Collaboration", "Community"]
        },
        "Artificial Intelligence & Machine Learning": {
            "AI Engineer": ["Generative AI", "LLMs", "Deep Learning"],
            "Prompt Engineer": ["AI Prompting", "Fine-Tuning", "LLM Customization"],
            "NLP Engineer": ["Text Analysis", "Chatbots", "Conversational AI"],
            "Computer Vision Engineer": ["Image Processing", "Object Detection"],
            "AI Research Scientist": ["Model Training", "Ethics", "ML Innovations"],
            "Robotics Engineer": ["Automation", "AI Ethics", "Perception Systems"],
            "AI Ethics Consultant": ["Fairness", "Bias Detection", "AI Policy"]
        },
        "Cloud & DevOps": {
            "Cloud Solutions Architect": ["AWS", "Azure", "Hybrid Cloud"],
            "Cloud Security Engineer": ["DevSecOps", "Compliance", "Zero Trust"],
            "Site Reliability Engineer (SRE)": ["Observability", "Fault Tolerance"],
            "Kubernetes Engineer": ["Microservices", "Scaling", "Containerization"]
        },
        "Cybersecurity": {
            "Ethical Hacker": ["Hacking", "Phishing", "Red Teaming"],
            "Security Engineer": ["SIEM", "Threat Intelligence", "Network Security"],
            "Incident Response Analyst": ["Threat Mitigation", "Security Audits"],
            "Cryptography Expert": ["Encryption", "Blockchain Security"]
        },
        "Data Science & Analytics": {
            "Data Scientist": ["AI Models", "Big Data", "Predictive Analytics"],
            "Data Engineer": ["ETL Pipelines", "Data Warehousing", "Cloud Storage"],
            "Business Intelligence Analyst": ["BI Tools", "Data Visualization"],
            "ML Engineer": ["MLOps", "Model Deployment", "Feature Engineering"],
            "Bioinformatics Scientist": ["Genomics", "Computational Biology"]
        }
    },
    "Healthcare & Medicine": {
        "Doctors & Physicians": {
            "General Practitioner": ["Diagnosis", "Patient Care", "Primary Health"],
            "Surgeon": ["Surgical Innovations", "Medical Robotics"],
            "Cardiologist": ["Heart Health", "Clinical Trials"],
            "Neurologist": ["Brain Research", "Mental Health"],
            "Oncologist": ["Cancer Research", "Precision Medicine"]
        },
        "Healthcare Technology": {
            "Medical AI Researcher": ["AI in Healthcare", "Medical Imaging AI"],
            "Telemedicine Specialist": ["Remote Consultations", "eHealth"],
            "Biomedical Engineer": ["Medical Devices", "Prosthetics"],
            "Pharmacovigilance Expert": ["Drug Safety", "Clinical Trials"]
        },
        "Mental Health & Wellness": {
            "Psychologist": ["Therapy", "Mental Health Awareness"],
            "Psychiatrist": ["Neuropharmacology", "Cognitive Science"]
        }
    },
    "Engineering & Technology": {
        "Mechanical Engineering": {
            "Automotive Engineer": ["EV Technology", "Autonomous Vehicles"],
            "Aerospace Engineer": ["Rocket Propulsion", "Space Tech"],
            "Manufacturing Engineer": ["Lean Manufacturing", "3D Printing"]
        },
        "Electrical & Electronics": {
            "Renewable Energy Engineer": ["Solar Tech", "Battery Storage"],
            "Chip Design Engineer": ["Semiconductors", "FPGA"],
            "Power Systems Engineer": ["Smart Grids", "Energy Efficiency"]
        },
        "Civil & Structural Engineering": {
            "Structural Engineer": ["Earthquake Resistant Design", "Bridges"],
            "Smart Cities Engineer": ["Urban Planning", "GreenTech"]
        }
    },
    "Business & Finance": {
        "Entrepreneurship & Startups": {
            "Tech Startup Founder": ["Product Market Fit", "Angel Investment"],
            "SaaS Founder": ["Subscription Models", "Scaling"],
            "FinTech Innovator": ["Digital Banking", "DeFi"],
            "EdTech Entrepreneur": ["AI Tutors", "Online Learning"],
            "GreenTech Founder": ["Sustainability", "Carbon Neutrality"]
        },
        "Marketing & Sales": {
            "Growth Hacker": ["Viral Marketing", "User Retention"],
            "SEO Specialist": ["Google Ranking", "Keyword Optimization"],
            "Social Media Manager": ["Brand Engagement", "Content Strategy"],
            "Sales Executive": ["Negotiation", "Lead Generation"]
        },
        "Finance & Investment": {
            "Financial Analyst": ["Stock Market", "Wealth Management"],
            "Risk Manager": ["Portfolio Management", "Financial Compliance"],
            "Cryptocurrency Analyst": ["Bitcoin Trends", "NFT Market"]
        }
    },
    "Legal & Government": {
        "Law & Compliance": {
            "Corporate Lawyer": ["Mergers & Acquisitions", "IP Law"],
            "Human Rights Lawyer": ["Ethical Justice", "Advocacy"],
            "Legal Tech Consultant": ["AI in Law", "Blockchain Contracts"]
        },
        "Government & Public Policy": {
            "IAS Officer": ["Policy Implementation", "Governance"],
            "Diplomat": ["Foreign Relations", "International Trade"],
            "Urban Planner": ["Smart Cities", "Public Transportation"]
        }
    },
    "Media, Design & Arts": {
    "Media & Journalism": {
        "Investigative Journalist": ["Political Reporting", "Fact Checking", "Breaking News"],
        "Podcaster": ["Audio Content", "Storytelling", "Engagement Strategies"],
        "Public Relations Expert": ["Brand Management", "Crisis Handling", "Media Outreach"]
    },
    "Content Creation & Digital Media": {
        "YouTuber": ["Video Content", "Subscriber Growth", "Monetization"],
        "Social Media Influencer": ["Instagram Growth", "Reels/TikTok Strategies", "Brand Collabs"],
        "Content Creator": ["Content Strategy", "Engagement Metrics", "Niche Selection"],
        "Live Streamer (Twitch, YouTube, Kick)": ["Gaming", "Live Interaction", "Sponsorships"]
    },
    "Video Editing & Production": {
        "Video Editor": ["Adobe Premiere Pro", "Final Cut Pro", "Post-Production"],
        "Motion Graphics Artist": ["After Effects", "3D Animation", "Visual Effects"],
        "Cinematographer": ["Camera Techniques", "Lighting", "Color Grading"],
        "Film Director": ["Scriptwriting", "Storyboarding", "Directing Actors"]
    },
    "Graphic Design & Animation": {
        "Graphic Designer": ["Typography", "Illustration", "Branding"],
        "3D Animator": ["Blender", "Maya", "CGI & VFX"],
        "UI/UX Designer": ["Wireframes", "Prototyping", "User Interaction"]
    },
    "Gaming Industry & Esports": {
        "Game Designer": ["Level Design", "Narrative Development", "Game Mechanics"],
        "Esports Manager": ["Competitive Gaming", "Sponsorships", "Team Management"],
        "Gaming Content Creator": ["Let’s Plays", "Game Streaming", "Twitch Growth"]
    }
},
    "Freelancing & Remote Work": {
        "Freelance Tech": {
            "Freelance Developer": ["Remote Work", "Client Management"],
            "Freelance UX Designer": ["Wireframes", "Prototyping"],
            "Freelance Cybersecurity Consultant": ["Pen Testing", "Data Privacy"]
        },
        "Freelance Creative": {
            "Freelance Writer": ["SEO Blogs", "Ghostwriting"],
            "Freelance Photographer": ["Photo Editing", "Composition"],
            "Freelance Filmmaker": ["Short Films", "Content Monetization"]
        }
    }
}


length_options = ["Short", "Medium", "Long"]
language_options = ["English", "Tanglish"]

def main():
    st.subheader("🚀 LinkedIn Post Generator")
    fs = FewShotPosts()

    # Maintain state for selections
    if "selected_category" not in st.session_state:
        st.session_state["selected_category"] = list(professions.keys())[0]

    if "selected_subcategory" not in st.session_state:
        st.session_state["selected_subcategory"] = list(professions[st.session_state["selected_category"]].keys())[0]

    if "selected_profession" not in st.session_state:
        st.session_state["selected_profession"] = list(professions[st.session_state["selected_category"]][st.session_state["selected_subcategory"]].keys())[0]

    # 🔹 **Horizontal Layout for User-Friendly Experience**
    col1, col2, col3 = st.columns(3)
    
    with col1:
        selected_category = st.selectbox(
            "📂 Select Category:", 
            options=professions.keys(),
            index=list(professions.keys()).index(st.session_state["selected_category"])
        )
        st.session_state["selected_category"] = selected_category  # Update state

    with col2:
        subcategories = list(professions[selected_category].keys())
        selected_subcategory = st.selectbox(
            "📁 Select Subcategory:", 
            options=subcategories,
            index=subcategories.index(st.session_state["selected_subcategory"]) if st.session_state["selected_subcategory"] in subcategories else 0
        )
        st.session_state["selected_subcategory"] = selected_subcategory  # Update state

    with col3:
        professions_list = list(professions[selected_category][selected_subcategory].keys())
        selected_profession = st.selectbox(
            "💼 Select Your Profession:", 
            options=professions_list,
            index=professions_list.index(st.session_state["selected_profession"]) if st.session_state["selected_profession"] in professions_list else 0
        )
        st.session_state["selected_profession"] = selected_profession  # Update state

    # **Align topic & language selections in one row for clarity**
    col4, col5 = st.columns(2)
    
    with col4:
        topics = professions[selected_category][selected_subcategory][selected_profession]
        selected_topic = st.selectbox("🎯 Select a Discussion Topic:", options=topics)
    
    with col5:
        selected_language = st.selectbox("📝 Select Language:", options=language_options)

    # **Length & Keywords - Aligned Horizontally**
    col6, col7 = st.columns([1, 3])
    
    with col6:
        selected_length = st.radio("📏 Select Post Length:", options=length_options, horizontal=True)
    
    with col7:
        custom_keywords = st.text_input("🔑 Add Specific Keywords (Optional)", help="Enter keywords to fine-tune the generated post.")

    # **Generate Post Button**
    if st.button("⚡ Generate Post"):
        post = generate_post(selected_length, selected_language, selected_topic, selected_profession, custom_keywords)
        st.write(post)

if __name__ == "__main__":
    main()
