import streamlit as st
import os
from few_shot import FewShotPosts
from post_generator import generate_post
from dotenv import load_dotenv

# Profession categories, subcategories, and discussion topics
professions = {
    "Technical": {
        "IT": {
            "Software Developer": ["Coding", "Debugging", "Software Architecture"],
            "Full Stack Developer": ["Frontend", "Backend", "APIs"],
            "DevOps Engineer": ["Automation", "CI/CD", "Infrastructure"],
            "Cybersecurity Specialist": ["Security", "Hacking", "Encryption"],
            "Blockchain Developer": ["Blockchain", "Smart Contracts", "DeFi"],
            "Cloud Engineer": ["AWS", "Azure", "GCP", "Kubernetes"],
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
            "Cloud Solutions Architect": ["Infrastructure", "Serverless", "Networking"]
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

length_options = ["Short", "Medium", "Long"]
language_options = ["English", "Tanglish"]

def main():
    st.subheader("🚀 LinkedIn Post Generator")
    fs = FewShotPosts()
    tags = fs.get_tags()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        selected_category = st.selectbox("📂 Select Category:", options=professions.keys())
    
    with col2:
        selected_subcategory = st.selectbox("📁 Select Subcategory:", options=professions[selected_category].keys())
        selected_profession = st.selectbox("💼 Select Your Profession:", options=professions[selected_category][selected_subcategory].keys())
    
    with col3:
        selected_topic = st.selectbox("🎯 Select a Discussion Topic:", options=professions[selected_category][selected_subcategory][selected_profession])
        selected_language = st.selectbox("📝 Select Language:", options=language_options)
    
    selected_length = st.radio("📏 Select Post Length:", options=length_options, horizontal=True)
    custom_keywords = st.text_input("🔑 Add Specific Keywords (Optional)", help="Enter keywords to fine-tune the generated post.")
    
    if st.button("⚡ Generate Post"):
        post = generate_post(selected_length, selected_language, selected_topic, selected_profession, custom_keywords)
        st.write(post)

if __name__ == "__main__":
    main()
