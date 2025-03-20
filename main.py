import streamlit as st
import os
from few_shot import FewShotPosts
from post_generator import generate_post
from dotenv import load_dotenv

# Profession categories and subcategories
professions = {
    "Technical": {
        "IT": [
            "Software Developer", "Full Stack Developer", "Backend Developer", "Frontend Developer",
            "Mobile App Developer", "Game Developer", "Embedded Systems Developer", "Software Architect",
            "Blockchain Developer"
        ],
        "AI": [
            "AI Engineer", "Machine Learning Engineer", "Deep Learning Engineer", "NLP Engineer",
            "Computer Vision Engineer", "AI Research Scientist", "AI Ethics Specialist", 
            "Robotics Engineer", "Autonomous Systems Engineer"
        ],
        "Cloud": [
            "Cloud Engineer", "AWS Cloud Engineer", "Azure Cloud Engineer", "GCP Cloud Engineer",
            "DevOps Engineer", "Cloud Security Engineer", "Cloud Solutions Architect",
            "Kubernetes Engineer"
        ],
        "Cybersecurity": [
            "Cybersecurity Analyst", "Ethical Hacker", "Penetration Tester", "Security Engineer",
            "Incident Response Analyst", "Cloud Security Specialist"
        ],
        "Data Science": [
            "Data Scientist", "Data Analyst", "Machine Learning Engineer", "AI Research Scientist",
            "Big Data Engineer", "Business Intelligence Analyst", "Data Engineer", 
            "Data Visualization Specialist"
        ]
    },
    "Healthcare": {
        "Doctors": [
            "General Physician", "Surgeon", "Cardiologist", "Pediatrician", "Dermatologist", 
            "Neurologist", "Oncologist", "Radiologist", "Psychiatrist", "Orthopedic Surgeon"
        ],
        "Medical Support": [
            "Registered Nurse", "Medical Assistant", "Pharmacist", "Physical Therapist",
            "Occupational Therapist", "Speech Therapist", "Dentist"
        ]
    },
    "Engineering": {
        "Core Engineering": [
            "Mechanical Engineer", "Electrical Engineer", "Civil Engineer", "Aerospace Engineer",
            "Automotive Engineer", "Biomedical Engineer", "Chemical Engineer", "Structural Engineer"
        ]
    },
    "Business": {
        "Entrepreneurship": [
            "Startup Founder", "Small Business Owner", "Tech Entrepreneur", "Social Entrepreneur",
            "E-commerce Business Owner", "Venture Capitalist", "Angel Investor"
        ],
        "Marketing": [
            "Digital Marketing Specialist", "SEO Specialist", "Brand Manager", "Social Media Marketer",
            "Content Strategist", "Growth Hacker", "Affiliate Marketer", "Marketing Automation Specialist"
        ],
        "Finance": [
            "Financial Analyst", "Investment Banker", "Risk Manager", "Wealth Manager",
            "Tax Consultant", "Actuary", "Hedge Fund Manager", "Venture Capital Analyst"
        ],
        "Sales": [
            "Sales Representative", "Account Manager", "Sales Manager", "Business Development Executive",
            "Retail Sales Associate", "Inside Sales Representative", "Sales Consultant"
        ]
    },
    "Legal": {
        "Lawyers": [
            "Corporate Lawyer", "Criminal Lawyer", "Intellectual Property Lawyer", "Litigation Lawyer",
            "Family Lawyer", "Tax Lawyer", "Environmental Lawyer", "Immigration Lawyer"
        ],
        "Legal Support": [
            "Paralegal", "Corporate Counsel", "Compliance Officer", "Contract Lawyer", 
            "Intellectual Property Consultant", "Environmental Law Specialist"
        ]
    },
    "Education": {
        "Academia": [
            "Professor", "Assistant Professor", "Associate Professor", "Adjunct Professor", 
            "Research Professor", "Visiting Professor", "Department Chair", "Lecturer"
        ],
        "School": [
            "School Teacher", "University Lecturer", "Education Consultant", "Curriculum Developer",
            "School Administrator", "Education Technology Specialist"
        ]
    },
    "Consulting": {
        "Business Consulting": [
            "Management Consultant", "IT Consultant", "Financial Consultant", "HR Consultant",
            "Strategy Consultant", "Legal Consultant", "Healthcare Consultant"
        ]
    },
    "Government & Public Services": {
        "Civil Services": [
            "IAS Officer", "District Collector", "Cabinet Secretary", "Joint Secretary", 
            "Deputy Commissioner", "Under Secretary", "Chief Secretary", "SDM (Sub-Divisional Magistrate)"
        ],
        "Law Enforcement": [
            "Police Officer", "Intelligence Analyst", "Public Policy Analyst", "Firefighter",
            "Foreign Service Officer", "Diplomat"
        ]
    },
    "Media & Creative": {
        "Media": [
            "Journalist", "News Reporter", "Editor", "Content Writer", "Technical Writer",
            "Scriptwriter", "Copywriter", "Public Relations Specialist"
        ],
        "Creative Arts": [
            "Graphic Designer", "Art Director", "Photographer", "Illustrator", "Video Producer",
            "Animator", "3D Modeler", "Fashion Designer"
        ]
    },
    "Freelancing": {
        "Tech Freelancers": [
            "Freelance Software Developer", "Freelance UI/UX Designer", "Freelance Blockchain Developer",
            "Freelance Data Scientist"
        ],
        "Creative Freelancers": [
            "Freelance Writer", "Freelance Graphic Designer", "Freelance Video Editor",
            "Freelance Photographer", "Freelance Translator"
        ],
        "Marketing Freelancers": [
            "Freelance Digital Marketer", "Freelance SEO Specialist", "Freelance Content Strategist"
        ]
    },
    "Students & Freshers": {
        "Student": [
            "Undergraduate Student", "Graduate Student", "PhD Student", "Research Assistant", "Intern"
        ],
        "Fresher": [
            "Entry-Level Software Developer", "Junior Data Scientist", "Trainee Engineer", 
            "Graduate Analyst", "Junior Marketing Associate", "Trainee Consultant"
        ]
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
        selected_tag = st.selectbox("🔹 Select a Topic:", options=tags)
    
    with col2:
        selected_category = st.selectbox("📂 Select Category:", options=professions.keys())
        selected_subcategory = st.selectbox("📁 Select Subcategory:", options=professions[selected_category].keys())
        selected_profession = st.selectbox("💼 Select Your Profession:", options=professions[selected_category][selected_subcategory])
    
    with col3:
        selected_language = st.selectbox("📝 Select Language:", options=language_options)
    
    selected_length = st.radio("📏 Select Post Length:", options=length_options, horizontal=True)
    
    custom_keywords = st.text_input("🔑 Add Specific Keywords (Optional)", help="Enter keywords to fine-tune the generated post.")
    
    if st.button("⚡ Generate Post"):
        post = generate_post(selected_length, selected_language, selected_tag, selected_profession, custom_keywords)
        st.write(post)

if __name__ == "__main__":
    main()
