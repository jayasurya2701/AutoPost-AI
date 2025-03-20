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

# 🎯 AI Chatbot Topics
chatbot_topics = {
    "Motivation": ["Career growth", "Perseverance", "Success mindset", "Overcoming self-doubt"],
    "Mental Health": ["Stress management", "Work-life balance", "Handling anxiety"],
    "Networking": ["Building connections", "Engaging with professionals", "Personal branding"],
    "Self Improvement": ["Learning new skills", "Time management", "Confidence building"],
    "Rejections": ["Overcoming failures", "Job search setbacks", "Resilience"],
    "Workplace Success": ["Excelling at work", "Standing out in workplace", "Asking for a raise"],
    "Leadership & Growth": ["Becoming a leader", "Decision-making skills", "Inspiring others"],
    "Entrepreneurship": ["Starting a business", "Side hustles", "Scaling a startup"],
    "Productivity": ["How to work smarter", "Best productivity hacks", "Morning routines"],
    "Happiness & Fulfillment": ["Finding happiness at work", "Staying positive", "The power of gratitude"],
}

# 🏆 Profession categories & topics
professions = {
    "Technical": {
        "IT": {
            "Software Developer": ["Coding", "Debugging", "Software Architecture"],
            "Full Stack Developer": ["Frontend", "Backend", "APIs"],
            "Cybersecurity Specialist": ["Security", "Hacking", "Encryption"],
            "Blockchain Developer": ["Blockchain", "Smart Contracts", "DeFi"],
            "UI/UX Designer": ["User Experience", "Design", "Prototyping"],
            "Open-Source Contributor": ["GitHub", "Collaboration", "Projects"]
        },
        "AI": {
            "AI Engineer": ["MachineLearning", "DeepLearning", "GenerativeAI","AI Agents","Agentic AI","LLM"],
            "NLP Engineer": ["NLP", "Text Analysis", "Chatbots"],
            "Computer Vision Engineer": ["Image Processing", "Object Detection", "Face Recognition"],
            "AI Research Scientist": ["AIResearch", "Ethics", "Innovation"],
            "Robotics Engineer": ["Automation", "AI Ethics", "Computer Vision"]
        },
        "Cloud": {
            "Cloud Engineer": ["AWS", "Azure", "GCP", "Kubernetes"],
            "Cloud Security Engineer": ["DevSecOps", "CloudSecurity", "Virtualization"],
            "Cloud Solutions Architect": ["Infrastructure", "Serverless", "Networking"],
            "DevOps Engineer": ["Automation", "CI/CD", "Infrastructure"],
        },
        "Cybersecurity": {
            "Cybersecurity Analyst": ["Threats", "Pentesting", "Encryption"],
            "Ethical Hacker": ["Hacking", "Phishing", "ZeroTrust"],
            "Security Engineer": ["Compliance", "Ransomware", "Cybersecurity"]
        },
        "Data Science": {
            "Data Scientist": ["Analytics", "BigData", "AIModels"],
            "Data Analyst": ["Visualization", "Forecasting", "Statistics"],
            "Business Intelligence Analyst": ["BI", "Dashboards", "Data Mining"]
        }
    },
    "Healthcare": {
        "Doctors": {
            "Surgeon": ["Surgery", "Medical Innovations", "Patient Care"],
            "Cardiologist": ["Heart Health", "Treatments", "Research"],
            "Pediatrician": ["Children’s Health", "Vaccination", "Diagnosis"]
        },
        "Medical Support": {
            "Registered Nurse": ["Therapy", "Nursing", "MentalHealth"],
            "Pharmacist": ["Pharmacy", "Medication", "Prevention"],
            "Physical Therapist": ["Rehabilitation", "PublicHealth", "Wellness"]
        }
    },
    "Engineering": {
        "Core Engineering": {
            "Mechanical Engineer": ["Manufacturing", "CAD", "Design"],
            "Electrical Engineer": ["Prototyping", "Sustainability", "Innovation"],
            "Civil Engineer": ["Construction", "Testing", "Infrastructure"]
        }
    },
    "Business": {
        "Entrepreneurship": {
            "Startup Founder": ["Startups", "Fundraising", "Scaling"],
            "Small Business Owner": ["Networking", "Leadership", "Branding"]
        },
        "Marketing": {
            "Digital Marketing Specialist": ["SEO", "Branding", "Advertising"],
            "Social Media Marketer": ["SocialMedia", "Campaigns", "Growth"]
        },
        "Finance": {
            "Financial Analyst": ["Investing", "Banking", "Wealth"],
            "Risk Manager": ["Taxation", "Trading", "Portfolio"]
        },
        "Sales": {
            "Sales Manager": ["Negotiation", "Closing", "LeadGeneration"],
            "Account Manager": ["B2B", "B2C", "CRM"]
        }
    },
    "Legal": {
        "Lawyers": {
            "Corporate Lawyer": ["Contracts", "Litigation", "Compliance"],
            "Intellectual Property Lawyer": ["IP", "Regulations", "Ethics"]
        },
        "Legal Support": {
            "Paralegal": ["Research", "CaseLaw", "Policy"],
            "Compliance Officer": ["Advocacy", "Justice", "Arbitration"]
        }
    },
    "Education": {
        "Academia": {
            "Professor": ["Research", "Lectures", "Pedagogy"],
            "Education Consultant": ["Innovation", "HigherEd", "Publications"]
        },
        "School": {
            "School Teacher": ["Teaching", "Curriculum", "Exams"],
            "EdTech Specialist": ["EdTech", "Learning", "SpecialEducation"]
        }
    },
    "Consulting": {
        "Business Consulting": {
            "Management Consultant": ["Strategy", "Optimization", "Growth"],
            "Digital Transformation Consultant": ["Leadership", "Analytics", "Transformation"]
        }
    },
    "Government & Public Services": {
        "Civil Services": {
            "IAS Officer": ["Governance", "Policy", "PublicService"],
            "Diplomat": ["Administration", "Leadership", "Diplomacy"]
        },
        "Law Enforcement": {
            "Police Officer": ["Crime", "Surveillance", "Forensics"],
            "Intelligence Analyst": ["Ethics", "NationalSecurity", "ThreatAssessment"]
        }
    },
    "Media & Creative": {
        "Media": {
            "Journalist": ["Journalism", "Reporting", "Storytelling"],
            "Public Relations Specialist": ["PR", "Content", "Editing"]
        },
        "Creative Arts": {
            "Graphic Designer": ["Design", "Illustration", "Aesthetics"],
            "Filmmaker": ["Photography", "Animation", "Music"]
        }
    },
    "Freelancing": {
        "Tech Freelancers": {
            "Freelance Software Developer": ["RemoteWork", "Contracts", "Clients"],
            "Freelance UI/UX Designer": ["Branding", "Portfolios", "DesignTrends"]
        },
        "Marketing Freelancers": {
            "Freelance Digital Marketer": ["Engagement", "GrowthHacking", "Conversion"]
        }
    },
    "Students & Freshers": {
        "Student": {
            "Undergraduate Student": ["Learning", "Internships", "Projects"],
            "Graduate Student": ["Research", "Networking", "Exams"]
        },
        "Fresher": {
            "Entry-Level Software Developer": ["Jobs", "Resume", "Interview"],
            "Junior Data Scientist": ["Training", "Certifications", "EntryLevel"]
        }
    }
}

# 🎯 **UI Layout: Clean & Organized**
col1, col2 = st.columns([2, 1])

### **🚀 LinkedIn Post Generator - Left Column**
with col1:
    st.markdown("### 🚀 **LinkedIn Post Generator**")
    st.markdown("*Craft engaging posts tailored to your profession!*")

    fs = FewShotPosts()

    # Maintain user state
    if "selected_category" not in st.session_state:
        st.session_state["selected_category"] = list(professions.keys())[0]

    if "selected_subcategory" not in st.session_state:
        st.session_state["selected_subcategory"] = list(professions[st.session_state["selected_category"]].keys())[0]

    if "selected_profession" not in st.session_state:
        st.session_state["selected_profession"] = list(professions[st.session_state["selected_category"]][st.session_state["selected_subcategory"]].keys())[0]

    # 🔹 **User-Friendly Horizontal Layout**
    colA, colB, colC = st.columns(3)

    with colA:
        selected_category = st.selectbox(
            "📂 **Select Category**", 
            options=professions.keys(),
            index=list(professions.keys()).index(st.session_state["selected_category"])
        )
        st.session_state["selected_category"] = selected_category

    with colB:
        subcategories = list(professions[selected_category].keys())
        selected_subcategory = st.selectbox(
            "📁 **Select Subcategory**", 
            options=subcategories,
            index=subcategories.index(st.session_state["selected_subcategory"]) if st.session_state["selected_subcategory"] in subcategories else 0
        )
        st.session_state["selected_subcategory"] = selected_subcategory

    with colC:
        professions_list = list(professions[selected_category][selected_subcategory].keys())
        selected_profession = st.selectbox(
            "💼 **Select Your Profession**", 
            options=professions_list,
            index=professions_list.index(st.session_state["selected_profession"]) if st.session_state["selected_profession"] in professions_list else 0
        )
        st.session_state["selected_profession"] = selected_profession

    # **Topic & Language Selection**
    colD, colE = st.columns(2)
    
    with colD:
        topics = professions[selected_category][selected_subcategory][selected_profession]
        selected_topic = st.selectbox("🎯 **Discussion Topic**", options=topics)
    
    with colE:
        selected_language = st.selectbox("📝 **Select Language**", options=["English", "Tanglish"])

    # **Post Length & Keywords**
    colF, colG = st.columns([1, 3])
    
    with colF:
        selected_length = st.radio("📏 **Post Length**", options=["Short", "Medium", "Long"], horizontal=True)
    
    with colG:
        custom_keywords = st.text_input("🔑 **Custom Keywords (Optional)**", help="Enter keywords for fine-tuning.")

    # **Generate Post**
    if st.button("⚡ **Generate Post**", key="generate_post_button"):
        post = generate_post(selected_length, selected_language, selected_topic, selected_profession, custom_keywords)
        st.success("🎉 **Post Generated!**")
        st.markdown(f"📝 **Your Post:**\n\n{post}")

### **🤖 InspireBot - AI Career Chatbot (Right Column)**
with col2:
    st.markdown("### 🤖 **InspireBot - AI Career Coach**")
    
    selected_chatbot_topic = st.selectbox("🧠 **Choose a Topic**", options=chatbot_topics.keys())
    
    if st.button("✨ **Get Career Insights**"):
        insights = f"🔹 {selected_chatbot_topic}: {', '.join(chatbot_topics[selected_chatbot_topic][:3])}..."
        st.info(insights)
    
    user_query = st.text_input("💬 **Ask InspireBot (Career & Growth)**")
    
    if st.button("🚀 **Get AI Advice**"):
        chatbot_response = f"💡 **Career Tip:** {chatbot_topics[selected_chatbot_topic][0]}"
        st.success(chatbot_response)

if __name__ == "__main__":
    main()
