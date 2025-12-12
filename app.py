import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import re
import json
import io
import base64
from datetime import datetime
from typing import Dict, List, Tuple
import random
import feedparser
import PyPDF2
import pdfplumber
from io import BytesIO
import time
import urllib.parse

# Configure page
st.set_page_config(
    page_title="CareerSense.AI - Resume to Career",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with proper styling
st.markdown("""
<style>
    /* Main styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    
    /* Skill badges */
    .skill-badge {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 4px 12px;
        margin: 2px 4px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
    }
    
    /* Job cards */
    .job-card {
        background: white;
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border-top: 5px solid #667eea;
        transition: transform 0.3s ease;
    }
    
    .job-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    /* Course cards */
    .course-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border-left: 5px solid #4CAF50;
        transition: transform 0.3s ease;
    }
    
    .course-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.12);
    }
    
    /* Platform badges */
    .platform-badge {
        background: linear-gradient(135deg, #6c757d, #495057);
        color: white;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    
    .platform-badge-coursera {
        background: linear-gradient(135deg, #0056D2, #003D82);
        color: white;
    }
    .platform-badge-edx {
        background: linear-gradient(135deg, #00A2B1, #007B8A);
        color: white;
    }
    .platform-badge-udemy {
        background: linear-gradient(135deg, #EC5252, #992337);
        color: white;
    }
    .platform-badge-fcc {
        background: linear-gradient(135deg, #0A0A23, #000000);
        color: white;
    }
    .platform-badge-khan {
        background: linear-gradient(135deg, #14BF96, #0D8C6D);
        color: white;
    }
    .platform-badge-linkedin {
        background: linear-gradient(135deg, #0077B5, #005582);
        color: white;
    }
    .platform-badge-youtube {
        background: linear-gradient(135deg, #FF0000, #CC0000);
        color: white;
    }
    .platform-badge-mit {
        background: linear-gradient(135deg, #8A8D8F, #5A5D5F);
        color: white;
    }
    .platform-badge-google {
        background: linear-gradient(135deg, #4285F4, #34A853);
        color: white;
    }
    .platform-badge-microsoft {
        background: linear-gradient(135deg, #00A4EF, #7FBA00);
        color: white;
    }
    .platform-badge-codecademy {
        background: linear-gradient(135deg, #1F4056, #0D1F2B);
        color: white;
    }
    .platform-badge-pluralsight {
        background: linear-gradient(135deg, #F15B2A, #C43C0E);
        color: white;
    }
    .platform-badge-futurelearn {
        background: linear-gradient(135deg, #DE0D6D, #A00A52);
        color: white;
    }
    .platform-badge-skillshare {
        background: linear-gradient(135deg, #2AB9A5, #1D8A7A);
        color: white;
    }
    .platform-badge-udacity {
        background: linear-gradient(135deg, #02B3E4, #0185B3);
        color: white;
    }
    .platform-badge-alison {
        background: linear-gradient(135deg, #FFE312, #000000);
        color: black;
    }
    .platform-badge-harvard {
        background: linear-gradient(135deg, #A41034, #7A0C27);
        color: white;
    }
    .platform-badge-stanford {
        background: linear-gradient(135deg, #8C1515, #650F0F);
        color: white;
    }
    .platform-badge-cisco {
        background: linear-gradient(135deg, #1BA0D7, #1478A3);
        color: white;
    }
    .platform-badge-ibm {
        background: linear-gradient(135deg, #054ADA, #0337A6);
        color: white;
    }
    .platform-badge-aws {
        background: linear-gradient(135deg, #FF9900, #CC7A00);
        color: black;
    }
    .platform-badge-oracle {
        background: linear-gradient(135deg, #F80000, #C00000);
        color: white;
    }
    .platform-badge-salesforce {
        background: linear-gradient(135deg, #00A1E0, #007EAD);
        color: white;
    }
    .platform-badge-redhat {
        background: linear-gradient(135deg, #EE0000, #BB0000);
        color: white;
    }
    .platform-badge-fastai {
        background: linear-gradient(135deg, #6F42C1, #59339E);
        color: white;
    }
    
    /* Level badges */
    .level-badge-beginner {
        background: linear-gradient(135deg, #28a745, #1e7e34);
        color: white;
        padding: 2px 8px;
        border-radius: 10px;
        font-size: 0.7rem;
        font-weight: 600;
    }
    
    .level-badge-intermediate {
        background: linear-gradient(135deg, #ffc107, #e0a800);
        color: black;
        padding: 2px 8px;
        border-radius: 10px;
        font-size: 0.7rem;
        font-weight: 600;
    }
    
    .level-badge-advanced {
        background: linear-gradient(135deg, #dc3545, #c82333);
        color: white;
        padding: 2px 8px;
        border-radius: 10px;
        font-size: 0.7rem;
        font-weight: 600;
    }
    
    /* Salary badges */
    .salary-badge {
        background: linear-gradient(135deg, #20c997, #17a2b8);
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    /* Match badges */
    .match-badge-high {
        background: linear-gradient(135deg, #28a745, #20c997);
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 1rem;
        text-align: center;
    }
    
    .match-badge-medium {
        background: linear-gradient(135deg, #ffc107, #fd7e14);
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 1rem;
        text-align: center;
    }
    
    .match-badge-low {
        background: linear-gradient(135deg, #dc3545, #e83e8c);
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 1rem;
        text-align: center;
    }
    
    /* Buttons */
    .job-link-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 8px 20px;
        border-radius: 25px;
        text-decoration: none;
        font-weight: 600;
        font-size: 0.9rem;
        display: inline-block;
        transition: all 0.3s ease;
        border: none;
        cursor: pointer;
    }
    
    .job-link-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        color: white;
        text-decoration: none;
    }
    
    .course-link-button {
        background: linear-gradient(135deg, #4CAF50, #45a049);
        color: white;
        padding: 8px 20px;
        border-radius: 25px;
        text-decoration: none;
        font-weight: 600;
        font-size: 0.9rem;
        display: inline-block;
        transition: all 0.3s ease;
        border: none;
        cursor: pointer;
    }
    
    .course-link-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(76, 175, 80, 0.4);
        color: white;
        text-decoration: none;
    }
    
    /* Learning path styles */
    .learning-path-container {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 20px 0;
        border-left: 5px solid #667eea;
    }
    
    .path-step {
        background: white;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        border-left: 4px solid #4CAF50;
    }
    
    .path-step-number {
        background: #4CAF50;
        color: white;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        margin-right: 10px;
    }
    
    .learning-path-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border-top: 5px solid #667eea;
        transition: transform 0.3s ease;
    }
    
    .learning-path-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #5a6fd8 0%, #6a3f8f 100%);
    }
    
    /* Card animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.5s ease-out;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'resume_data' not in st.session_state:
    st.session_state.resume_data = None
if 'recommendations' not in st.session_state:
    st.session_state.recommendations = None

class ResumeParser:
    """Parse resumes from PDF and extract skills, experience, and education"""
    
    def __init__(self):
        self.common_skills = [
            # Programming Languages
            'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'php', 'ruby', 'go', 'rust',
            'swift', 'kotlin', 'scala', 'r', 'matlab', 'sql', 'nosql',
            
            # Web Technologies
            'html', 'css', 'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask',
            'spring', 'laravel', 'ruby on rails', 'asp.net', 'jquery', 'bootstrap',
            
            # Data Science & AI
            'machine learning', 'deep learning', 'artificial intelligence', 'ai', 
            'data science', 'data analysis', 'data visualization', 'statistics',
            'natural language processing', 'nlp', 'computer vision', 'big data',
            'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'pandas', 'numpy',
            
            # Cloud & DevOps
            'aws', 'amazon web services', 'azure', 'google cloud', 'gcp', 'docker',
            'kubernetes', 'jenkins', 'git', 'github', 'gitlab', 'ci/cd', 'terraform',
            'ansible', 'linux', 'unix', 'bash', 'shell scripting',
            
            # Databases
            'mysql', 'postgresql', 'mongodb', 'redis', 'oracle', 'sql server', 'sqlite',
            'cassandra', 'elasticsearch', 'dynamodb',
            
            # Tools & Platforms
            'tableau', 'power bi', 'excel', 'jupyter', 'spark', 'hadoop', 'kafka',
            'airflow', 'snowflake', 'databricks', 'jira', 'confluence', 'slack',
            
            # Soft Skills
            'leadership', 'communication', 'teamwork', 'problem solving', 'project management',
            'agile', 'scrum', 'kanban', 'time management', 'critical thinking', 'creativity',
            'adaptability', 'collaboration', 'presentation', 'negotiation'
        ]
    
    def extract_text_from_pdf(self, pdf_file) -> str:
        """Extract text from PDF file"""
        text = ""
        
        try:
            with pdfplumber.open(BytesIO(pdf_file.read())) as pdf:
                for i, page in enumerate(pdf.pages):
                    if i < 5:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
                        time.sleep(0.01)
        except Exception as e:
            st.warning(f"pdfplumber failed: {str(e)[:100]}... Trying PyPDF2")
            try:
                pdf_file.seek(0)
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                for i, page in enumerate(pdf_reader.pages):
                    if i < 5:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
            except Exception as e2:
                st.error(f"PyPDF2 failed: {str(e2)[:100]}...")
        
        return text
    
    def extract_skills(self, text: str) -> List[str]:
        """Extract skills from text"""
        if not text:
            return []
        
        text_lower = text.lower()
        found_skills = set()
        
        for skill in self.common_skills:
            if skill in text_lower:
                found_skills.add(skill.title())
        
        return list(found_skills)[:20]
    
    def extract_experience(self, text: str) -> int:
        """Extract years of experience from text"""
        if not text:
            return 0
        
        patterns = [
            r'(\d+)\s*(?:years?|yrs?)\s*(?:of)?\s*experience',
            r'experience\s*(?:of)?\s*(\d+)\s*(?:years?|yrs?)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text.lower())
            if matches:
                try:
                    return int(matches[0])
                except:
                    pass
        
        return 2
    
    def extract_education(self, text: str) -> List[str]:
        """Extract education information"""
        if not text:
            return []
        
        education_keywords = ['bachelor', 'master', 'phd', 'university', 'college', 'degree']
        
        sentences = re.split(r'[.!?]', text)
        education = []
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            if any(edu in sentence_lower for edu in education_keywords):
                clean_sentence = re.sub(r'\s+', ' ', sentence).strip()
                if len(clean_sentence) > 10:
                    education.append(clean_sentence[:100])
        
        return education[:3]

    def parse_resume(self, file) -> Dict:
        """Parse resume and return structured data"""
        text = self.extract_text_from_pdf(file)
        
        if not text or len(text.strip()) < 50:
            return {
                'skills': ['Python', 'SQL', 'Communication'],
                'experience': 2,
                'education': ['Bachelor\'s Degree'],
                'raw_text': text or 'No text extracted'
            }
        
        return {
            'skills': self.extract_skills(text),
            'experience': self.extract_experience(text),
            'education': self.extract_education(text),
            'raw_text': text[:500] + '...' if len(text) > 500 else text
        }

class FreeJobAPI:
    """Free job APIs"""
    
    def __init__(self):
        self.platform_urls = {
            'Indeed': 'https://www.indeed.com/jobs?q=',
            'LinkedIn': 'https://www.linkedin.com/jobs/search/?keywords=',
            'Glassdoor': 'https://www.glassdoor.com/Job/jobs.htm?sc.keyword=',
            'RemoteOK': 'https://remoteok.com/remote-',
            'WeWorkRemotely': 'https://weworkremotely.com/categories/remote-',
            'AngelList': 'https://angel.co/jobs?keyword=',
            'Google Jobs': 'https://www.google.com/search?q=',
            'Stack Overflow': 'https://stackoverflow.com/jobs?q=',
            'GitHub Jobs': 'https://jobs.github.com/positions?description=',
            'Monster': 'https://www.monster.com/jobs/search?q=',
            'CareerBuilder': 'https://www.careerbuilder.com/jobs?keywords=',
            'SimplyHired': 'https://www.simplyhired.com/search?q=',
            'ZipRecruiter': 'https://www.ziprecruiter.com/jobs-search?search='
            
        }
    
    def get_job_openings(self, role: str, location: str = "remote", count: int = 10) -> List[Dict]:
        """Get job openings with real search URLs"""
        job_platforms = list(self.platform_urls.keys())[:8]
        
        jobs = []
        for i in range(min(count, 12)):
            platform = job_platforms[i % len(job_platforms)]
            encoded_role = urllib.parse.quote(role + " " + location)
            
            job = {
                'title': f'{role}',
                'company': self._get_random_company(),
                'location': location.title(),
                'salary': self._get_random_salary(role),
                'posted': f'{random.randint(1, 7)} days ago',
                'description': f'Seeking a {role} with relevant experience. Apply now for this exciting opportunity!',
                'skills': self._get_skills_for_role(role),
                'url': f"{self.platform_urls.get(platform, 'https://www.indeed.com/jobs?q=')}{encoded_role}",
                'platform': platform,
                'experience': f'{random.randint(1, 5)}+ years',
                'type': random.choice(['Full-time', 'Contract', 'Part-time', 'Remote']),
                'posted_date': datetime.now().strftime('%Y-%m-%d')
            }
            jobs.append(job)
        
        return jobs[:count]
    
    def _get_random_company(self):
        companies = [
            'TechCorp Solutions', 'Digital Innovations Inc', 'Cloud Systems LLC',
            'Data Analytics Pro', 'AI Research Labs', 'Web Development Hub',
            'Mobile First Tech', 'Enterprise Solutions Inc', 'Startup XYZ',
            'Global Tech Partners', 'Future Systems Ltd', 'Smart Solutions Co'
        ]
        return random.choice(companies)
    
    def _get_random_salary(self, role):
        salary_ranges = {
            'Data Scientist': ('$120,000', '$160,000'),
            'Software Engineer': ('$100,000', '$140,000'),
            'Data Analyst': ('$80,000', '$110,000'),
            'DevOps Engineer': ('$110,000', '$150,000'),
            'Machine Learning Engineer': ('$130,000', '$180,000'),
            'Frontend Developer': ('$90,000', '$130,000'),
            'Backend Developer': ('$100,000', '$140,000'),
            'Full Stack Developer': ('$95,000', '$135,000'),
            'Cloud Architect': ('$140,000', '$200,000'),
            'Product Manager': ('$120,000', '$170,000')
        }
        
        default = ('$80,000', '$120,000')
        min_sal, max_sal = salary_ranges.get(role, default)
        return f'{min_sal} - {max_sal}'
    
    def _get_skills_for_role(self, role):
        skill_sets = {
            'Data Scientist': ['Python', 'Machine Learning', 'SQL', 'Statistics', 'Data Visualization'],
            'Software Engineer': ['Java', 'Python', 'JavaScript', 'Algorithms', 'System Design'],
            'Data Analyst': ['SQL', 'Excel', 'Tableau', 'Statistics', 'Data Analysis'],
            'DevOps Engineer': ['AWS', 'Docker', 'Kubernetes', 'CI/CD', 'Linux'],
            'Machine Learning Engineer': ['Python', 'TensorFlow', 'PyTorch', 'Deep Learning', 'MLOps'],
            'Frontend Developer': ['JavaScript', 'React', 'HTML', 'CSS', 'TypeScript'],
            'Backend Developer': ['Python', 'Node.js', 'Database', 'API', 'Microservices'],
            'Full Stack Developer': ['JavaScript', 'Python', 'React', 'Node.js', 'Database'],
            'Cloud Architect': ['AWS', 'Azure', 'GCP', 'Cloud Security', 'Architecture'],
            'Product Manager': ['Product Strategy', 'Agile', 'Leadership', 'Communication', 'Roadmapping']
        }
        return skill_sets.get(role, ['Python', 'SQL', 'Problem Solving'])

class enhancedLearningAPI:
    """Enhanced Free Learning API with more platforms and learning paths"""
    
    def __init__(self):
        # Expanded platform URLs with more learning platforms
        self.platform_urls = {
            # Academic & University Platforms
            'Coursera': 'https://www.coursera.org/search?query=',
            'edX': 'https://www.edx.org/search?q=',
            'MIT OpenCourseWare': 'https://ocw.mit.edu/search/?q=',
            'Stanford Online': 'https://online.stanford.edu/search?query=',
            'Harvard Online': 'https://online-learning.harvard.edu/catalog?keywords=',
            'Khan Academy': 'https://www.khanacademy.org/search?page_search_query=',
            'OpenLearn': 'https://www.open.edu/openlearn/search?q=',
            'Saylor Academy': 'https://learn.saylor.org/course/index.php?search=',
            'UC Berkeley Online': 'https://online.berkeley.edu/search/?q=',
            
            # Tech & Coding Platforms
            'freeCodeCamp': 'https://www.freecodecamp.org/search?q=',
            'Codecademy': 'https://www.codecademy.com/catalog?query=',
            'Udacity': 'https://www.udacity.com/courses/all?search=',
            'Pluralsight': 'https://www.pluralsight.com/search?q=',
            'Udemy': 'https://www.udemy.com/courses/search/?q=',
            'LinkedIn Learning': 'https://www.linkedin.com/learning/search?keywords=',
            'Skillshare': 'https://www.skillshare.com/en/search?query=',
            'FutureLearn': 'https://www.futurelearn.com/search?q=',
            
            # Corporate Training Platforms
            'Microsoft Learn': 'https://docs.microsoft.com/en-us/learn/browse/?terms=',
            'Google Digital Garage': 'https://learndigital.withgoogle.com/digitalgarage/courses?q=',
            'AWS Training': 'https://aws.amazon.com/training/search/?q=',
            'IBM Skills': 'https://www.ibm.com/training/search?query=',
            'Cisco Networking Academy': 'https://www.netacad.com/courses/all-courses?search=',
            'Oracle University': 'https://education.oracle.com/search-results?keywords=',
            'Salesforce Trailhead': 'https://trailhead.salesforce.com/en/search?keywords=',
            'Red Hat Training': 'https://www.redhat.com/en/services/training/all-courses?search=',
            
            # Programming Practice Platforms
            'LeetCode': 'https://leetcode.com/problemset/all/?search=',
            'HackerRank': 'https://www.hackerrank.com/domains?search=',
            'Codewars': 'https://www.codewars.com/kata/search/?q=',
            'Exercism': 'https://exercism.org/tracks?search=',
            'Kaggle Learn': 'https://www.kaggle.com/learn?search=',
            
            # Video Learning Platforms
            'YouTube Learning': 'https://www.youtube.com/results?search_query=learn+',
            'O\'Reilly Online': 'https://www.oreilly.com/search/?query=',
            'Packt': 'https://www.packtpub.com/search?query=',
            
            # International Platforms
            'Alison': 'https://alison.com/courses?query=',
            'Future Skills': 'https://futureskillsprime.in/course-catalog?search=',
            'NPTEL': 'https://onlinecourses.nptel.ac.in/search?search=',
            'Coursera for Campus': 'https://www.coursera.org/campus?query=',
            
            # Specialized Tech Platforms
            'fast.ai': 'https://course.fast.ai/',
            'DeepLearning.AI': 'https://www.deeplearning.ai/courses/?search=',
            'DataCamp': 'https://www.datacamp.com/search?q=',
            'Brilliant': 'https://brilliant.org/search/?q=',
            'Scrimba': 'https://scrimba.com/search?query=',
            
            # Project-Based Learning
            'Frontend Mentor': 'https://www.frontendmentor.io/challenges?search=',
            'The Odin Project': 'https://www.theodinproject.com/paths?search=',
            'Full Stack Open': 'https://fullstackopen.com/en/',
            'App Academy Open': 'https://open.appacademy.io/learn/search?search=',
            
            # Language Learning for Tech
            'Duolingo for Schools': 'https://schools.duolingo.com/search?q=',
            'Babbel': 'https://www.babbel.com/search?q=',
            'Rosetta Stone': 'https://www.rosettastone.com/lp/search/?q=',
            
            # Free Certification Providers
            'Google Certifications': 'https://grow.google/certificates/?search=',
            'Microsoft Certifications': 'https://docs.microsoft.com/en-us/learn/certifications/browse/?search=',
            'AWS Certifications': 'https://aws.amazon.com/certification/?search=',
            'Cisco Certifications': 'https://www.cisco.com/c/en/us/training-events/training-certifications/certifications.html?search='
        }
        
        # Comprehensive course database with real URLs
        self.popular_courses = {
            'python': [
                {
                    'name': 'Python for Everybody Specialization',
                    'platform': 'Coursera',
                    'instructor': 'University of Michigan',
                    'level': 'Beginner',
                    'duration': '3 months',
                    'rating': 4.8,
                    'description': 'Learn to program and analyze data with Python, develop programs, and work with data',
                    'url': 'https://www.coursera.org/specializations/python',
                    'price': 'Free to audit',
                    'skills': ['Python', 'Programming', 'Data Structures', 'Web Scraping'],
                    'certification': True
                },
                {
                    'name': 'Learn Python 3',
                    'platform': 'freeCodeCamp',
                    'instructor': 'freeCodeCamp Team',
                    'level': 'Beginner',
                    'duration': '300 hours',
                    'rating': 4.9,
                    'description': 'Comprehensive Python course with certification and real-world projects',
                    'url': 'https://www.freecodecamp.org/learn/scientific-computing-with-python/',
                    'price': 'Free',
                    'skills': ['Python', 'Algorithms', 'Problem Solving', 'Debugging'],
                    'certification': True
                },
                {
                    'name': 'CS50\'s Introduction to Programming with Python',
                    'platform': 'Harvard Online',
                    'instructor': 'Harvard University',
                    'level': 'Beginner',
                    'duration': '10 weeks',
                    'rating': 4.9,
                    'description': 'Harvard\'s introduction to programming using Python for beginners',
                    'url': 'https://cs50.harvard.edu/python/2022/',
                    'price': 'Free',
                    'skills': ['Python', 'CS Fundamentals', 'Problem Solving'],
                    'certification': False
                }
            ],
            'machine learning': [
                {
                    'name': 'Machine Learning Specialization',
                    'platform': 'Coursera',
                    'instructor': 'Andrew Ng (Stanford)',
                    'level': 'Intermediate',
                    'duration': '4 months',
                    'rating': 4.9,
                    'description': 'The most popular ML course worldwide - learn ML, data mining, and statistical pattern recognition',
                    'url': 'https://www.coursera.org/specializations/machine-learning-introduction',
                    'price': 'Free to audit',
                    'skills': ['Machine Learning', 'Python', 'Statistics', 'Algorithms'],
                    'certification': True
                },
                {
                    'name': 'Machine Learning Crash Course',
                    'platform': 'Google',
                    'instructor': 'Google AI',
                    'level': 'Intermediate',
                    'duration': '15 hours',
                    'rating': 4.8,
                    'description': 'Practical ML course with TensorFlow by Google, includes exercises and case studies',
                    'url': 'https://developers.google.com/machine-learning/crash-course',
                    'price': 'Free',
                    'skills': ['Machine Learning', 'TensorFlow', 'AI', 'Neural Networks'],
                    'certification': True
                },
                {
                    'name': 'Practical Deep Learning for Coders',
                    'platform': 'fast.ai',
                    'instructor': 'Jeremy Howard',
                    'level': 'Intermediate',
                    'duration': '7 weeks',
                    'rating': 4.9,
                    'description': 'Cutting-edge deep learning course focused on practical applications with PyTorch',
                    'url': 'https://course.fast.ai/',
                    'price': 'Free',
                    'skills': ['Deep Learning', 'PyTorch', 'Computer Vision', 'NLP'],
                    'certification': False
                }
            ],
            'data science': [
                {
                    'name': 'Data Science Specialization',
                    'platform': 'Coursera',
                    'instructor': 'Johns Hopkins University',
                    'level': 'Intermediate',
                    'duration': '10 months',
                    'rating': 4.7,
                    'description': '10-course data science specialization covering the entire data science pipeline',
                    'url': 'https://www.coursera.org/specializations/jhu-data-science',
                    'price': 'Free to audit',
                    'skills': ['Data Science', 'R', 'Statistics', 'Machine Learning'],
                    'certification': True
                },
                {
                    'name': 'IBM Data Science Professional Certificate',
                    'platform': 'Coursera',
                    'instructor': 'IBM',
                    'level': 'Beginner',
                    'duration': '3 months',
                    'rating': 4.6,
                    'description': 'Launch your career in data science with this comprehensive IBM certificate',
                    'url': 'https://www.coursera.org/professional-certificates/ibm-data-science',
                    'price': 'Free trial',
                    'skills': ['Data Science', 'Python', 'SQL', 'Data Visualization'],
                    'certification': True
                },
                {
                    'name': 'Kaggle Learn',
                    'platform': 'Kaggle',
                    'instructor': 'Kaggle Team',
                    'level': 'Beginner',
                    'duration': 'Self-paced',
                    'rating': 4.8,
                    'description': 'Hands-on data science courses with practical exercises and competitions',
                    'url': 'https://www.kaggle.com/learn',
                    'price': 'Free',
                    'skills': ['Data Science', 'Python', 'ML', 'Data Analysis'],
                    'certification': True
                }
            ],
            'aws': [
                {
                    'name': 'AWS Cloud Practitioner Essentials',
                    'platform': 'AWS Training',
                    'instructor': 'AWS',
                    'level': 'Beginner',
                    'duration': '6 hours',
                    'rating': 4.7,
                    'description': 'Official AWS fundamentals and certification preparation course',
                    'url': 'https://www.aws.training/Details/eLearning?id=60697',
                    'price': 'Free',
                    'skills': ['AWS', 'Cloud Computing', 'Cloud Fundamentals'],
                    'certification': True
                },
                {
                    'name': 'AWS Solutions Architect Associate',
                    'platform': 'freeCodeCamp',
                    'instructor': 'Andrew Brown',
                    'level': 'Intermediate',
                    'duration': '15 hours',
                    'rating': 4.8,
                    'description': 'Complete course to pass AWS Solutions Architect Associate certification',
                    'url': 'https://www.freecodecamp.org/news/pass-the-aws-certified-solutions-architect-exam-with-this-free-15-hour-course/',
                    'price': 'Free',
                    'skills': ['AWS', 'Cloud Architecture', 'Networking', 'Security'],
                    'certification': True
                }
            ],
            'javascript': [
                {
                    'name': 'The Complete JavaScript Course 2024',
                    'platform': 'Udemy',
                    'instructor': 'Jonas Schmedtmann',
                    'level': 'All Levels',
                    'duration': '69 hours',
                    'rating': 4.7,
                    'description': 'Modern JavaScript from the beginning - all the way up to JS expert level',
                    'url': 'https://www.udemy.com/course/the-complete-javascript-course/',
                    'price': 'Paid (often on sale)',
                    'skills': ['JavaScript', 'ES6+', 'Async Programming', 'OOP'],
                    'certification': True
                },
                {
                    'name': 'JavaScript Algorithms and Data Structures',
                    'platform': 'freeCodeCamp',
                    'instructor': 'freeCodeCamp Team',
                    'level': 'Intermediate',
                    'duration': '300 hours',
                    'rating': 4.9,
                    'description': 'Master JavaScript by solving coding challenges and building projects',
                    'url': 'https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures/',
                    'price': 'Free',
                    'skills': ['JavaScript', 'Algorithms', 'Data Structures', 'Problem Solving'],
                    'certification': True
                }
            ],
            'react': [
                {
                    'name': 'React - The Complete Guide',
                    'platform': 'Udemy',
                    'instructor': 'Maximilian Schwarzmüller',
                    'level': 'All Levels',
                    'duration': '48 hours',
                    'rating': 4.7,
                    'description': 'Dive in and learn React.js from scratch with hands-on projects',
                    'url': 'https://www.udemy.com/course/react-the-complete-guide-incl-redux/',
                    'price': 'Paid (often on sale)',
                    'skills': ['React', 'Redux', 'Hooks', 'React Router'],
                    'certification': True
                },
                {
                    'name': 'Full Stack Open',
                    'platform': 'University of Helsinki',
                    'instructor': 'Matti Luukkainen',
                    'level': 'Intermediate',
                    'duration': '6 months',
                    'rating': 4.9,
                    'description': 'Learn React, Redux, Node.js, MongoDB, GraphQL and TypeScript in one go',
                    'url': 'https://fullstackopen.com/en/',
                    'price': 'Free',
                    'skills': ['React', 'Node.js', 'MongoDB', 'GraphQL'],
                    'certification': False
                }
            ],
            'sql': [
                {
                    'name': 'SQL for Data Science',
                    'platform': 'Coursera',
                    'instructor': 'University of California, Davis',
                    'level': 'Beginner',
                    'duration': '4 weeks',
                    'rating': 4.6,
                    'description': 'Learn SQL fundamentals and apply them to query and analyze data',
                    'url': 'https://www.coursera.org/learn/sql-for-data-science',
                    'price': 'Free to audit',
                    'skills': ['SQL', 'Database', 'Data Analysis', 'Query Optimization'],
                    'certification': True
                },
                {
                    'name': 'Learn SQL',
                    'platform': 'Codecademy',
                    'instructor': 'Codecademy Team',
                    'level': 'Beginner',
                    'duration': '8 hours',
                    'rating': 4.7,
                    'description': 'Interactive SQL course with hands-on practice and projects',
                    'url': 'https://www.codecademy.com/learn/learn-sql',
                    'price': 'Free',
                    'skills': ['SQL', 'Database Design', 'Queries', 'Joins'],
                    'certification': True
                }
            ]
        }
        
        # Learning paths for different career tracks
        self.learning_paths = {
            'Data Scientist': [
                {'step': 1, 'skill': 'Python Programming', 'duration': '2 months', 'resources': ['Coursera', 'freeCodeCamp']},
                {'step': 2, 'skill': 'Statistics & Probability', 'duration': '1 month', 'resources': ['Khan Academy', 'MIT OCW']},
                {'step': 3, 'skill': 'SQL & Databases', 'duration': '1 month', 'resources': ['Codecademy', 'Coursera']},
                {'step': 4, 'skill': 'Data Visualization', 'duration': '1 month', 'resources': ['Tableau Public', 'Kaggle']},
                {'step': 5, 'skill': 'Machine Learning', 'duration': '3 months', 'resources': ['Coursera', 'fast.ai']},
                {'step': 6, 'skill': 'Big Data Tools', 'duration': '2 months', 'resources': ['AWS', 'Databricks']}
            ],
            'Software Engineer': [
                {'step': 1, 'skill': 'Programming Fundamentals', 'duration': '2 months', 'resources': ['freeCodeCamp', 'CS50']},
                {'step': 2, 'skill': 'Data Structures & Algorithms', 'duration': '2 months', 'resources': ['LeetCode', 'Coursera']},
                {'step': 3, 'skill': 'Web Development', 'duration': '3 months', 'resources': ['The Odin Project', 'Full Stack Open']},
                {'step': 4, 'skill': 'System Design', 'duration': '2 months', 'resources': ['Educative', 'YouTube']},
                {'step': 5, 'skill': 'Version Control (Git)', 'duration': '2 weeks', 'resources': ['GitHub', 'Atlassian']},
                {'step': 6, 'skill': 'Testing & Deployment', 'duration': '1 month', 'resources': ['Udemy', 'Pluralsight']}
            ],
            'DevOps Engineer': [
                {'step': 1, 'skill': 'Linux & Bash', 'duration': '1 month', 'resources': ['Linux Foundation', 'freeCodeCamp']},
                {'step': 2, 'skill': 'Networking Fundamentals', 'duration': '1 month', 'resources': ['Cisco', 'Professor Messer']},
                {'step': 3, 'skill': 'Cloud Computing', 'duration': '2 months', 'resources': ['AWS', 'Google Cloud']},
                {'step': 4, 'skill': 'Containers (Docker)', 'duration': '1 month', 'resources': ['Docker Docs', 'Pluralsight']},
                {'step': 5, 'skill': 'Orchestration (Kubernetes)', 'duration': '2 months', 'resources': ['Kubernetes.io', 'Udacity']},
                {'step': 6, 'skill': 'CI/CD & Automation', 'duration': '1 month', 'resources': ['Jenkins', 'GitHub Actions']}
            ]
        }
    
    def get_platform_badge_class(self, platform: str) -> str:
        """Get CSS class for platform badge"""
        platform_classes = {
            'Coursera': 'platform-badge-coursera',
            'edX': 'platform-badge-edx',
            'Udemy': 'platform-badge-udemy',
            'freeCodeCamp': 'platform-badge-fcc',
            'Khan Academy': 'platform-badge-khan',
            'LinkedIn Learning': 'platform-badge-linkedin',
            'YouTube Learning': 'platform-badge-youtube',
            'MIT OpenCourseWare': 'platform-badge-mit',
            'Google': 'platform-badge-google',
            'Microsoft Learn': 'platform-badge-microsoft',
            'Codecademy': 'platform-badge-codecademy',
            'Pluralsight': 'platform-badge-pluralsight',
            'FutureLearn': 'platform-badge-futurelearn',
            'Skillshare': 'platform-badge-skillshare',
            'Udacity': 'platform-badge-udacity',
            'Alison': 'platform-badge-alison',
            'Harvard Online': 'platform-badge-harvard',
            'Stanford Online': 'platform-badge-stanford',
            'Cisco Networking Academy': 'platform-badge-cisco',
            'IBM Skills': 'platform-badge-ibm',
            'AWS Training': 'platform-badge-aws',
            'Oracle University': 'platform-badge-oracle',
            'Salesforce Trailhead': 'platform-badge-salesforce',
            'Red Hat Training': 'platform-badge-redhat',
            'fast.ai': 'platform-badge-fastai',
            'Kaggle Learn': 'platform-badge-khan',
            'LeetCode': 'platform-badge-fcc',
            'HackerRank': 'platform-badge-fcc'
        }
        return platform_classes.get(platform, 'platform-badge')
    
    def get_courses(self, skills: List[str], platform: str = "all", count: int = 8) -> List[Dict]:
        """Get courses with real URLs from multiple platforms"""
        courses = []
        
        for skill in skills[:5]:
            skill_lower = skill.lower()
            
            if skill_lower in self.popular_courses:
                courses.extend(self.popular_courses[skill_lower])
            else:
                platforms_to_search = []
                if platform == "all":
                    platforms_to_search = ['Coursera', 'freeCodeCamp', 'edX', 'Udemy', 'Udacity', 
                                         'LinkedIn Learning', 'YouTube Learning', 'Microsoft Learn']
                else:
                    platforms_to_search = [platform]
                
                for platform_name in platforms_to_search:
                    if platform_name in self.platform_urls:
                        encoded_skill = urllib.parse.quote(skill)
                        search_url = f"{self.platform_urls[platform_name]}{encoded_skill}"
                        
                        course_levels = ['Beginner', 'Intermediate', 'Advanced']
                        durations = ['4 weeks', '2 months', '3 months', '6 months']
                        instructors = ['Industry Expert', 'University Professor', 'Senior Developer']
                        
                        courses.append({
                            'name': f'Master {skill} - Complete Course',
                            'platform': platform_name,
                            'instructor': random.choice(instructors),
                            'level': random.choice(course_levels),
                            'duration': random.choice(durations),
                            'rating': round(random.uniform(4.0, 4.9), 1),
                            'description': f'Comprehensive course to master {skill} with hands-on projects',
                            'url': search_url,
                            'price': random.choice(['Free', 'Free to audit', 'Free trial', 'Paid']),
                            'skills': [skill],
                            'certification': random.choice([True, False])
                        })
                        
                        if len(courses) >= count * 2:
                            break
            
            if len(courses) >= count * 2:
                break
        
        unique_courses = []
        seen_urls = set()
        for course in courses:
            if course['url'] not in seen_urls:
                seen_urls.add(course['url'])
                unique_courses.append(course)
        
        return unique_courses[:count]
    
    def get_learning_path(self, role: str) -> List[Dict]:
        """Get structured learning path for a role"""
        return self.learning_paths.get(role, [])
    
    def get_certifications(self, role: str) -> List[Dict]:
        """Get certification recommendations with real URLs"""
        certs = {
            'Data Scientist': [
                {
                    'name': 'Google Data Analytics Professional Certificate',
                    'provider': 'Google',
                    'level': 'Professional',
                    'duration': '6 months',
                    'cost': 'Free trial',
                    'url': 'https://www.coursera.org/professional-certificates/google-data-analytics',
                    'skills': ['Data Analysis', 'SQL', 'R', 'Tableau']
                },
                {
                    'name': 'IBM Data Science Professional Certificate',
                    'provider': 'IBM',
                    'level': 'Professional',
                    'duration': '3 months',
                    'cost': 'Free to audit',
                    'url': 'https://www.coursera.org/professional-certificates/ibm-data-science',
                    'skills': ['Data Science', 'Python', 'ML', 'Data Visualization']
                },
                {
                    'name': 'AWS Certified Data Analytics - Specialty',
                    'provider': 'Amazon',
                    'level': 'Advanced',
                    'duration': '3 months',
                    'cost': '$300',
                    'url': 'https://aws.amazon.com/certification/certified-data-analytics-specialty/',
                    'skills': ['AWS', 'Big Data', 'Analytics', 'Data Lakes']
                }
            ],
            'Software Engineer': [
                {
                    'name': 'Meta Back-End Developer Professional Certificate',
                    'provider': 'Meta',
                    'level': 'Professional',
                    'duration': '8 months',
                    'cost': 'Free to audit',
                    'url': 'https://www.coursera.org/professional-certificates/meta-back-end-developer',
                    'skills': ['Python', 'Django', 'API Development', 'Database']
                },
                {
                    'name': 'Oracle Certified Professional, Java SE Developer',
                    'provider': 'Oracle',
                    'level': 'Professional',
                    'duration': '6 months',
                    'cost': '$245',
                    'url': 'https://education.oracle.com/java-se-8-programmer-ii/pexam_1Z0-809',
                    'skills': ['Java', 'OOP', 'Multithreading', 'Collections']
                },
                {
                    'name': 'Microsoft Certified: Azure Developer Associate',
                    'provider': 'Microsoft',
                    'level': 'Associate',
                    'duration': '4 months',
                    'cost': '$165',
                    'url': 'https://docs.microsoft.com/en-us/learn/certifications/azure-developer/',
                    'skills': ['Azure', '.NET', 'Cloud Development', 'DevOps']
                }
            ],
            'DevOps Engineer': [
                {
                    'name': 'Google Cloud DevOps Engineer Professional Certificate',
                    'provider': 'Google',
                    'level': 'Professional',
                    'duration': '6 months',
                    'cost': 'Free trial',
                    'url': 'https://www.coursera.org/professional-certificates/google-cloud-devops',
                    'skills': ['GCP', 'Kubernetes', 'CI/CD', 'Infrastructure']
                },
                {
                    'name': 'AWS Certified DevOps Engineer - Professional',
                    'provider': 'Amazon',
                    'level': 'Professional',
                    'duration': '6 months',
                    'cost': '$300',
                    'url': 'https://aws.amazon.com/certification/certified-devops-engineer-professional/',
                    'skills': ['AWS', 'DevOps', 'Automation', 'Monitoring']
                },
                {
                    'name': 'Docker Certified Associate (DCA)',
                    'provider': 'Docker',
                    'level': 'Associate',
                    'duration': '3 months',
                    'cost': '$195',
                    'url': 'https://www.docker.com/certification/',
                    'skills': ['Docker', 'Containers', 'Orchestration', 'Security']
                }
            ],
            'Machine Learning Engineer': [
                {
                    'name': 'TensorFlow Developer Certificate',
                    'provider': 'Google',
                    'level': 'Professional',
                    'duration': '3 months',
                    'cost': '$100',
                    'url': 'https://www.tensorflow.org/certificate',
                    'skills': ['TensorFlow', 'Deep Learning', 'Neural Networks']
                },
                {
                    'name': 'AWS Certified Machine Learning - Specialty',
                    'provider': 'Amazon',
                    'level': 'Specialty',
                    'duration': '4 months',
                    'cost': '$300',
                    'url': 'https://aws.amazon.com/certification/certified-machine-learning-specialty/',
                    'skills': ['AWS ML', 'SageMaker', 'MLOps', 'Deep Learning']
                }
            ]
        }
        return certs.get(role, [])
    
    def get_all_platforms(self) -> List[str]:
        """Get list of all available platforms"""
        return list(self.platform_urls.keys())

class EnhancedCareerRecommender:
    def __init__(self):
        self.job_api = FreeJobAPI()
        self.learning_api = EnhancedLearningAPI()
        self.resume_parser = ResumeParser()
        self.job_roles = self._create_job_roles_dataset()
    
    def _create_job_roles_dataset(self) -> pd.DataFrame:
        """Create job roles dataset"""
        data = {
            'role': [
                'Data Scientist', 'Machine Learning Engineer', 'Data Analyst',
                'Software Engineer', 'Frontend Developer', 'Backend Developer',
                'Full Stack Developer', 'DevOps Engineer', 'Cloud Architect',
                'Product Manager', 'Business Analyst', 'UX/UI Designer',
                'Data Engineer', 'AI Research Scientist', 'Mobile Developer',
                'Cybersecurity Analyst', 'Blockchain Developer', 'Game Developer',
                'QA Engineer', 'System Administrator', 'Network Engineer'
            ],
            'required_skills': [
                'Python, Machine Learning, Statistics, SQL, Data Visualization',
                'Python, Deep Learning, TensorFlow, PyTorch, Mathematics',
                'SQL, Excel, Data Analysis, Statistics, Tableau',
                'Java, Python, Algorithms, System Design, Git',
                'JavaScript, React, HTML, CSS, TypeScript',
                'Python, Node.js, Database, API, Docker',
                'JavaScript, Python, React, Node.js, Database',
                'AWS, Docker, Kubernetes, CI/CD, Linux',
                'AWS, Azure, GCP, Cloud Security, Architecture',
                'Product Strategy, Agile, Leadership, Communication',
                'Business Analysis, SQL, Requirements, Documentation',
                'UI/UX Design, Figma, User Research, Prototyping',
                'Python, SQL, ETL, Data Warehousing, Big Data',
                'Machine Learning, Research, Python, Mathematics',
                'Swift, Kotlin, Mobile Development, iOS, Android',
                'Network Security, Ethical Hacking, SIEM, Firewalls',
                'Solidity, Ethereum, Smart Contracts, Cryptography',
                'C++, Unity, Game Design, 3D Modeling',
                'Testing, Automation, Selenium, Test Cases',
                'Linux, Windows Server, Active Directory, Virtualization',
                'Networking, CCNA, Routing, Switching, Security'
            ],
            'experience_level': [3, 4, 2, 3, 2, 3, 3, 4, 5, 5, 2, 3, 3, 4, 2, 3, 3, 3, 2, 3, 3],
            'salary_range': [
                '$120k-$160k', '$140k-$180k', '$80k-$110k', '$100k-$140k', 
                '$90k-$130k', '$100k-$140k', '$100k-$140k', '$120k-$160k',
                '$140k-$200k', '$130k-$180k', '$70k-$100k', '$80k-$120k',
                '$110k-$150k', '$150k-$200k', '$90k-$130k', '$90k-$130k',
                '$100k-$150k', '$80k-$120k', '$70k-$100k', '$80k-$110k',
                '$85k-$120k'
            ],
            'demand_level': ['High', 'Very High', 'High', 'Very High', 'High', 
                           'High', 'Very High', 'High', 'Very High', 'High',
                           'Medium', 'High', 'Very High', 'High', 'High',
                           'Very High', 'High', 'Medium', 'Medium', 'Medium', 'High'],
            'growth_outlook': ['35%', '40%', '25%', '30%', '28%', '32%', '35%', 
                             '38%', '42%', '30%', '22%', '28%', '45%', '50%', '26%',
                             '33%', '35%', '20%', '18%', '15%', '20%']
        }
        return pd.DataFrame(data)
    
    def calculate_match_score(self, user_skills: List[str], user_experience: int, 
                            target_role: str) -> Tuple[float, List[str], List[str]]:
        """Calculate match score"""
        role_data = self.job_roles[self.job_roles['role'] == target_role]
        if role_data.empty:
            return 0.0, [], []
            
        role_data = role_data.iloc[0]
        required_skills = [skill.strip().lower() for skill in role_data['required_skills'].split(',')]
        
        user_skills_lower = [skill.lower() for skill in user_skills]
        
        matched_skills = []
        missing_skills = []
        
        for skill in required_skills:
            if any(skill in user_skill or user_skill in skill for user_skill in user_skills_lower):
                matched_skills.append(skill.title())
            else:
                missing_skills.append(skill.title())
        
        skill_score = len(matched_skills) / max(len(required_skills), 1)
        
        required_exp = role_data['experience_level']
        if user_experience >= required_exp:
            exp_score = 1.0
        else:
            exp_score = user_experience / max(required_exp, 1)
        
        total_score = 0.7 * skill_score + 0.3 * exp_score
        
        return min(round(total_score * 100, 2), 100), matched_skills, missing_skills
    
    def recommend_careers(self, user_skills: List[str], user_experience: int, top_n: int = 5):
        """Get career recommendations"""
        recommendations = []
        
        for role in self.job_roles['role']:
            score, matched, missing = self.calculate_match_score(user_skills, user_experience, role)
            role_data = self.job_roles[self.job_roles['role'] == role].iloc[0]
            
            job_openings = self.job_api.get_job_openings(role)
            courses = self.learning_api.get_courses(missing[:3])
            learning_path = self.learning_api.get_learning_path(role)
            certifications = self.learning_api.get_certifications(role)
            
            recommendations.append({
                'role': role,
                'match_score': score,
                'matched_skills': matched,
                'missing_skills': missing,
                'salary_range': role_data['salary_range'],
                'experience_level': role_data['experience_level'],
                'demand_level': role_data['demand_level'],
                'growth_outlook': role_data['growth_outlook'],
                'job_openings': job_openings,
                'courses': courses,
                'learning_path': learning_path,
                'certifications': certifications
            })
        
        recommendations.sort(key=lambda x: x['match_score'], reverse=True)
        return recommendations[:top_n]

def display_learning_path(learning_path):
    """Display structured learning path"""
    if not learning_path:
        return st.info("No learning path available for this role.")
    
    st.markdown("### 🛣️ Learning Path")
    
    for step in learning_path:
        resources_html = ""
        for resource in step['resources']:
            resources_html += f'<span class="skill-badge">{resource}</span> '
        
        st.markdown(f"""
        <div class="path-step">
            <div style="display: flex; align-items: center; margin-bottom: 10px;">
                <span class="path-step-number">{step['step']}</span>
                <h4 style="margin: 0;">{step['skill']}</h4>
            </div>
            <p style="margin: 5px 0; color: #555;">
                <strong>⏱️ Duration:</strong> {step['duration']}
            </p>
            <p style="margin: 5px 0; color: #555;">
                <strong>📚 Resources:</strong><br>
                {resources_html}
            </p>
        </div>
        """, unsafe_allow_html=True)

# ========== RESUME ANALYSIS FUNCTIONS ==========

def analyze_resume(career_recommender, uploaded_file):
    """Analyze resume and store results in session state"""
    try:
        # Show progress
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Step 1: Parse resume
        status_text.text("📄 Parsing resume...")
        progress_bar.progress(25)
        time.sleep(0.5)
        
        resume_data = career_recommender.resume_parser.parse_resume(uploaded_file)
        st.session_state.resume_data = resume_data
        
        # Step 2: Extract information
        status_text.text("🔍 Extracting skills and experience...")
        progress_bar.progress(50)
        time.sleep(0.5)
        
        # Step 3: Generate recommendations
        status_text.text("🎯 Finding career matches...")
        progress_bar.progress(75)
        time.sleep(0.5)
        
        if resume_data['skills']:
            recommendations = career_recommender.recommend_careers(
                resume_data['skills'], 
                resume_data['experience']
            )
            st.session_state.recommendations = recommendations
        else:
            st.session_state.recommendations = []
        
        # Step 4: Complete
        status_text.text("✅ Analysis complete!")
        progress_bar.progress(100)
        time.sleep(0.5)
        
        # Clear progress indicators
        progress_bar.empty()
        status_text.empty()
        
        st.success("Resume analysis complete!")
        
    except Exception as e:
        st.error(f"Error analyzing resume: {str(e)}")
        # Provide default data
        st.session_state.resume_data = {
            'skills': ['Python', 'SQL', 'Communication', 'Problem Solving'],
            'experience': 2,
            'education': ['Bachelor\'s Degree'],
            'raw_text': 'Sample resume data'
        }
        st.session_state.recommendations = career_recommender.recommend_careers(
            ['Python', 'SQL', 'Communication'], 2
        )

def display_resume_results(career_recommender):
    """Display resume analysis results"""
    resume_data = st.session_state.resume_data
    
    st.markdown("### 📊 Resume Analysis Results")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 🛠️ Skills Found")
        if resume_data['skills']:
            for skill in resume_data['skills'][:8]:
                st.markdown(f"<span class='skill-badge'>{skill}</span>", unsafe_allow_html=True)
            if len(resume_data['skills']) > 8:
                st.caption(f"+ {len(resume_data['skills']) - 8} more skills")
        else:
            st.info("No specific skills detected")
    
    with col2:
        st.markdown("#### 🎓 Education")
        if resume_data['education']:
            for edu in resume_data['education']:
                st.markdown(f"• {edu}")
        else:
            st.info("Education information not found")
    
    with col3:
        st.markdown("#### 💼 Experience")
        st.markdown(f"**{resume_data['experience']} years**")
        st.progress(min(resume_data['experience'] / 10, 1.0))
    
    # Show extracted text preview
    with st.expander("📝 View Extracted Text"):
        st.text(resume_data['raw_text'][:500] + "..." if len(resume_data['raw_text']) > 500 else resume_data['raw_text'])

def show_resume_analysis(career_recommender):
    """Resume analysis interface"""
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Resume upload section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Upload Your Resume")
        uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"], 
                                         label_visibility="collapsed")
        
        # Custom upload area styling
        st.markdown("""
        <div style="border: 2px dashed #667eea; border-radius: 15px; padding: 3rem; 
                   text-align: center; background: #f8f9fa; margin: 1rem 0;">
            <h3 style="color: #667eea;">📁 Drag & Drop or Click to Upload</h3>
            <p style="color: #555;">Supports PDF files</p>
            <p style="color: #888;"><small>We'll extract your skills, experience, and education</small></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 💡 Tips")
        tips = [
            "✅ Make sure your resume is text-based",
            "✅ Include your skills clearly",
            "✅ Mention years of experience",
            "✅ Include education details"
        ]
        for tip in tips:
            st.markdown(f"• {tip}")
    
    # Process resume button
    if uploaded_file is not None:
        if st.button("🔍 Analyze Resume", type="primary", use_container_width=True):
            analyze_resume(career_recommender, uploaded_file)
    
    # Display results if available
    if st.session_state.resume_data:
        display_resume_results(career_recommender)
    
    # Display recommendations if available
    if st.session_state.recommendations:
        display_recommendations(career_recommender)

def show_career_match(career_recommender):
    """Manual career matching"""
    st.markdown("## 🎯 Career Matching")
    
    # Check for existing profile data
    if hasattr(st.session_state, 'profile_skills'):
        default_skills = st.session_state.profile_skills
        default_experience = st.session_state.profile_experience
    else:
        default_skills = "Python, SQL, Machine Learning, Data Analysis, AWS"
        default_experience = 3
    
    # Input form
    with st.form("career_match_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            skills_input = st.text_area(
                "Your Skills & Technologies",
                default_skills,
                height=120
            )
            
            experience = st.slider("Years of Experience", 0, 30, default_experience)
        
        with col2:
            education = st.selectbox(
                "Education Level",
                ["High School", "Bachelor's", "Master's", "PhD", "Other"]
            )
            
            interests = st.multiselect(
                "Career Interests",
                ["Data Science", "Software Engineering", "Cloud", "AI/ML", 
                 "Product", "UX/UI", "DevOps", "Business"],
                default=["Data Science", "Software Engineering"]
            )
        
        submitted = st.form_submit_button("🔍 Find Career Matches", use_container_width=True)
    
    if submitted and skills_input:
        skills = [s.strip() for s in skills_input.split(",")]
        
        with st.spinner("Analyzing your profile..."):
            recommendations = career_recommender.recommend_careers(skills, experience)
            
            if recommendations:
                st.success(f"Found {len(recommendations)} career matches!")
                
                for i, rec in enumerate(recommendations):
                    with st.container():
                        st.markdown(f"### {i+1}. {rec['role']} - {rec['match_score']}% Match")
                        st.markdown(f"**Salary:** {rec['salary_range']} | **Demand:** {rec['demand_level']}")
                        st.progress(rec['match_score'] / 100)
                        st.markdown("---")
            else:
                st.warning("No career matches found")

def show_live_jobs(career_recommender):
    """Live job search with enhanced UI"""
    st.markdown("## 💼 Live Job Search")
    
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        role = st.text_input(
            "Job Role / Keywords",
            "Data Scientist",
            placeholder="e.g., Software Engineer, Data Analyst, DevOps..."
        )
    
    with col2:
        location = st.text_input(
            "Location",
            "remote",
            placeholder="e.g., remote, New York, San Francisco..."
        )
    
    with col3:
        count = st.selectbox(
            "Results",
            [5, 10, 15, 20],
            index=1
        )
    
    if st.button("🔍 Search Jobs", type="primary", use_container_width=True):
        with st.spinner(f"Searching for {role} jobs in {location}..."):
            jobs = career_recommender.job_api.get_job_openings(role, location, count)
            
            if jobs:
                st.success(f"Found {len(jobs)} jobs for '{role}' in '{location}'")
                
                # Display jobs in columns
                cols = st.columns(2)
                for idx, job in enumerate(jobs):
                    with cols[idx % 2]:
                        # Format skills as badges
                        skills_html = ""
                        for skill in job.get('skills', [])[:5]:
                            skills_html += f'<span class="skill-badge">{skill}</span> '
                        
                        html_content = f"""
                        <div class="job-card fade-in">
                            <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 10px;">
                                <h4 style="margin: 0; color: #2c3e50;">{job['title']}</h4>
                                <span class="platform-badge">{job.get('platform', 'Job Board')}</span>
                            </div>
                            
                            <p style="margin: 5px 0; color: #555;">
                                <strong style="color: #667eea;">🏢 Company:</strong> {job['company']}
                            </p>
                            
                            <p style="margin: 5px 0; color: #555;">
                                <strong style="color: #667eea;">📍 Location:</strong> {job['location']}
                            </p>
                            
                            <p style="margin: 5px 0; color: #555;">
                                <strong style="color: #667eea;">💼 Type:</strong> {job.get('type', 'Full-time')}
                            </p>
                            
                            <p style="margin: 5px 0; color: #555;">
                                <strong style="color: #667eea;">📅 Posted:</strong> {job['posted']}
                            </p>
                            
                            <p style="margin: 10px 0;">
                                <span class="salary-badge">💰 {job['salary']}</span>
                            </p>
                            
                            <p style="margin: 10px 0; color: #555; font-size: 0.9rem;">
                                {job['description']}
                            </p>
                            
                            <div style="margin: 10px 0;">
                                <strong style="color: #667eea;">🛠️ Skills:</strong><br>
                                {skills_html}
                            </div>
                            
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 15px;">
                                <span style="color: #666; font-size: 0.9rem;">
                                    ⏳ {job.get('experience', '2+ years')}
                                </span>
                                <a href="{job['url']}" target="_blank" class="job-link-button">
                                    Apply Now
                                </a>
                            </div>
                        </div>
                        """
                        st.markdown(html_content, unsafe_allow_html=True)
            else:
                st.warning(f"No jobs found for '{role}' in '{location}'")

def show_insights(career_recommender):
    """Market insights"""
    st.markdown("## 📈 Career Insights")
    
    def create_salary_chart(career_recommender):
        """Create salary chart"""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        roles = career_recommender.job_roles['role'].tolist()
        salaries = [int(s.split('-')[0].replace('$', '').replace('k', '')) 
                    for s in career_recommender.job_roles['salary_range']]
        
        colors = ['#667eea' if i % 2 == 0 else '#764ba2' for i in range(len(roles))]
        
        bars = ax.barh(roles, salaries, color=colors, alpha=0.8)
        ax.set_xlabel('Salary ($ thousands)')
        ax.set_title('💰 Average Salary by Role', fontsize=16, fontweight='bold')
        
        for bar, salary in zip(bars, salaries):
            ax.text(bar.get_width() + 2, bar.get_y() + bar.get_height()/2,
                    f'${salary}k', va='center', fontweight='bold')
        
        plt.tight_layout()
        return fig
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 💰 Salary Trends")
        fig = create_salary_chart(career_recommender)
        st.pyplot(fig)
    
    with col2:
        st.markdown("### 🚀 Top Roles 2024")
        st.dataframe(career_recommender.job_roles[['role', 'demand_level', 'salary_range']], use_container_width=True)
    
    st.markdown("### 💡 Tips")
    st.info("""
    1. **Upload your resume** for personalized career recommendations
    2. **Focus on high-demand skills** like AI, Cloud, and Data Science
    3. **Continuous learning** is key to career growth
    4. **Network effectively** on professional platforms
    """)

def display_recommendations(career_recommender):
    """Display career recommendations with learning paths"""
    recommendations = st.session_state.recommendations
    
    if not recommendations:
        st.warning("No recommendations found. Please try with a different resume.")
        return
    
    st.markdown("---")
    st.markdown("## 🎯 Career Recommendations")
    
    for i, rec in enumerate(recommendations):
        with st.container():
            # Header with match score
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.markdown(f"### {i+1}. {rec['role']}")
            with col2:
                if rec['match_score'] >= 80:
                    badge_class = "match-badge-high"
                elif rec['match_score'] >= 60:
                    badge_class = "match-badge-medium"
                else:
                    badge_class = "match-badge-low"
                st.markdown(f'<div class="{badge_class}">{rec["match_score"]}% Match</div>', unsafe_allow_html=True)
            with col3:
                st.markdown(f"**{rec['demand_level']}**")
            
            # Details
            detail_cols = st.columns(4)
            with detail_cols[0]:
                st.metric("💰 Salary", rec['salary_range'])
            with detail_cols[1]:
                st.metric("📈 Growth", rec['growth_outlook'])
            with detail_cols[2]:
                st.metric("💼 Min Exp", f"{rec['experience_level']}+ yrs")
            with detail_cols[3]:
                st.progress(rec['match_score'] / 100)
            
            # Tabs for details
            tab1, tab2, tab3, tab4 = st.tabs(["📊 Skills Match", "💼 Job Openings", "🎓 Learning Path", "📜 Certifications"])
            
            with tab1:
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**✅ Your Matching Skills**")
                    for skill in rec['matched_skills'][:5]:
                        st.markdown(f"<span class='skill-badge'>{skill}</span>", unsafe_allow_html=True)
                    if len(rec['matched_skills']) == 0:
                        st.info("No matching skills found")
                with col2:
                    st.markdown("**📚 Skills to Develop**")
                    for skill in rec['missing_skills'][:5]:
                        st.markdown(f"<span class='skill-badge' style='background: #dc3545;'>{skill}</span>", unsafe_allow_html=True)
                    if len(rec['missing_skills']) == 0:
                        st.success("Great! You have all required skills!")
            
            with tab2:
                if rec['job_openings']:
                    for job in rec['job_openings'][:2]:
                        # Format skills as badges
                        skills_html = ""
                        for skill in job.get('skills', [])[:5]:
                            skills_html += f'<span class="skill-badge">{skill}</span> '
                        
                        html_content = f"""
                        <div class="job-card fade-in">
                            <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 10px;">
                                <h4 style="margin: 0; color: #2c3e50;">{job['title']}</h4>
                                <span class="platform-badge">{job.get('platform', 'Job Board')}</span>
                            </div>
                            
                            <p style="margin: 5px 0; color: #555;">
                                <strong style="color: #667eea;">🏢 Company:</strong> {job['company']}
                            </p>
                            
                            <p style="margin: 5px 0; color: #555;">
                                <strong style="color: #667eea;">📍 Location:</strong> {job['location']}
                            </p>
                            
                            <p style="margin: 5px 0; color: #555;">
                                <strong style="color: #667eea;">📅 Posted:</strong> {job['posted']}
                            </p>
                            
                            <p style="margin: 10px 0;">
                                <span class="salary-badge">💰 {job['salary']}</span>
                            </p>
                            
                            <div style="margin: 10px 0;">
                                <strong style="color: #667eea;">🛠️ Skills:</strong><br>
                                {skills_html}
                            </div>
                            
                            <a href="{job['url']}" target="_blank" class="job-link-button">
                                View Job Details
                            </a>
                        </div>
                        """
                        st.markdown(html_content, unsafe_allow_html=True)
                else:
                    st.info("No current job openings found")
            
            with tab3:
                # Display learning path
                if 'learning_path' in rec and rec['learning_path']:
                    display_learning_path(rec['learning_path'])
                else:
                    # Display courses if no specific learning path
                    if rec['courses']:
                        st.markdown("### 📚 Recommended Courses")
                        cols = st.columns(2)
                        for idx, course in enumerate(rec['courses'][:4]):
                            with cols[idx % 2]:
                                badge_class = career_recommender.learning_api.get_platform_badge_class(course['platform'])
                                level_class = {
                                    'Beginner': 'level-badge-beginner',
                                    'Intermediate': 'level-badge-intermediate',
                                    'Advanced': 'level-badge-advanced'
                                }.get(course['level'], 'level-badge-beginner')
                                
                                html_content = f"""
                                <div class="course-card fade-in">
                                    <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 10px;">
                                        <h5 style="margin: 0; color: #2c3e50;">{course['name']}</h5>
                                        <div>
                                            <span class="{level_class}" style="margin-right: 5px;">{course['level']}</span>
                                            <span class="{badge_class}" style="padding: 2px 6px; border-radius: 10px; 
                                                  font-size: 0.7rem;">{course['platform']}</span>
                                        </div>
                                    </div>
                                    
                                    <p style="margin: 5px 0; color: #555; font-size: 0.9rem;">
                                        {course.get('description', 'Master this skill')}
                                    </p>
                                    
                                    <div style="display: flex; justify-content: space-between; margin-top: 10px;">
                                        <span style="color: #666; font-size: 0.8rem;">
                                            ⏱️ {course.get('duration', 'Self-paced')}
                                        </span>
                                        <a href="{course['url']}" target="_blank" 
                                           style="background: #667eea; color: white; padding: 5px 10px; 
                                                  border-radius: 5px; text-decoration: none; font-size: 0.8rem;">
                                            View
                                        </a>
                                    </div>
                                </div>
                                """
                                st.markdown(html_content, unsafe_allow_html=True)
                    else:
                        st.info("No courses found")
            
            with tab4:
                if rec.get('certifications'):
                    for cert in rec['certifications'][:2]:
                        html_content = f"""
                        <div style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                                   border-radius: 12px; padding: 15px; margin: 10px 0;
                                   border-left: 4px solid #4CAF50;">
                            <h5 style="margin: 0; color: #2c3e50;">{cert['name']}</h5>
                            <p style="margin: 5px 0; color: #555;">
                                <strong>Provider:</strong> {cert['provider']}
                            </p>
                            <div style="display: flex; justify-content: space-between; margin: 10px 0;">
                                <span style="color: #666;">⏱️ {cert['duration']}</span>
                                <span style="color: #666;">💰 {cert['cost']}</span>
                                <span style="color: #4CAF50; font-weight: bold;">{cert['level']}</span>
                            </div>
                            <a href="{cert['url']}" target="_blank" class="course-link-button">
                                📜 View Certification
                            </a>
                        </div>
                        """
                        st.markdown(html_content, unsafe_allow_html=True)
                else:
                    st.info("No certifications found for this role")
            
            st.markdown("---")

def show_free_courses(career_recommender):
    """Enhanced course search with more platforms"""
    st.markdown("## 🎓 Advanced Course Search")
    
    # Platform selection
    platforms = career_recommender.learning_api.get_all_platforms()
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        skill = st.text_input("Skill to learn", "python", 
                            placeholder="e.g., Python, Machine Learning, Web Development...")
    
    with col2:
        platform_filter = st.selectbox(
            "Platform",
            ["All Platforms"] + sorted(platforms)[:20]  # Show first 20 platforms
        )
    
    with col3:
        level_filter = st.selectbox(
            "Level",
            ["All Levels", "Beginner", "Intermediate", "Advanced"]
        )
    
    if st.button("🔍 Search Courses", type="primary", use_container_width=True):
        with st.spinner(f"Searching for {skill} courses..."):
            courses = career_recommender.learning_api.get_courses(
                [skill], 
                platform_filter if platform_filter != "All Platforms" else "all"
            )
            
            # Apply level filter
            if level_filter != "All Levels":
                courses = [c for c in courses if c['level'] == level_filter]
            
            if courses:
                st.success(f"Found {len(courses)} courses for '{skill}'")
                
                # Display platform statistics
                platform_counts = {}
                for course in courses:
                    platform = course['platform']
                    platform_counts[platform] = platform_counts.get(platform, 0) + 1
                
                if platform_counts:
                    st.markdown("### 📊 Available on Platforms:")
                    cols = st.columns(min(6, len(platform_counts)))
                    for idx, (platform, count) in enumerate(list(platform_counts.items())[:6]):
                        with cols[idx % 6]:
                            badge_class = career_recommender.learning_api.get_platform_badge_class(platform)
                            st.markdown(f"""
                            <div style="text-align: center; padding: 10px; border-radius: 10px; 
                                      background: #f8f9fa; margin: 5px;">
                                <div class="{badge_class}" style="padding: 5px 10px; border-radius: 15px; 
                                      margin-bottom: 5px; display: inline-block;">
                                    {platform[:15]}{'...' if len(platform) > 15 else ''}
                                </div>
                                <div style="font-size: 0.9rem; color: #666;">
                                    {count} course{'' if count == 1 else 's'}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                
                # Display courses
                cols = st.columns(2)
                for idx, course in enumerate(courses):
                    with cols[idx % 2]:
                        badge_class = career_recommender.learning_api.get_platform_badge_class(course['platform'])
                        level_class = {
                            'Beginner': 'level-badge-beginner',
                            'Intermediate': 'level-badge-intermediate',
                            'Advanced': 'level-badge-advanced'
                        }.get(course['level'], 'level-badge-beginner')
                        
                        cert_badge = "✅" if course.get('certification', False) else "📘"
                        
                        html_content = f"""
                        <div class="learning-path-card fade-in">
                            <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 10px;">
                                <h4 style="margin: 0; color: #2c3e50;">{course['name']}</h4>
                                <div>
                                    <span class="{level_class}" style="margin-right: 5px;">{course['level']}</span>
                                    <span class="{badge_class}" style="padding: 3px 8px; border-radius: 12px; 
                                          font-size: 0.8rem;">{course['platform']}</span>
                                </div>
                            </div>
                            
                            <p style="margin: 5px 0; color: #555;">
                                <strong style="color: #667eea;">👨‍🏫 Instructor:</strong> {course.get('instructor', 'Industry Expert')}
                            </p>
                            
                            <div style="display: flex; justify-content: space-between; margin: 10px 0;">
                                <span style="color: #555;">
                                    <strong>⏱️</strong> {course['duration']}
                                </span>
                                <span style="color: #555;">
                                    <strong>⭐</strong> {course.get('rating', 4.5)}/5.0
                                </span>
                                <span style="color: #555;">
                                    <strong>{cert_badge}</strong> {course.get('price', 'Free')}
                                </span>
                            </div>
                            
                            <p style="margin: 10px 0; color: #666; font-size: 0.9rem;">
                                {course.get('description', 'Master this skill with hands-on projects')}
                            </p>
                            
                            <div style="margin: 10px 0;">
                                {''.join([f'<span class="skill-badge">{s}</span> ' for s in course.get('skills', [skill])[:3]])}
                            </div>
                            
                            <a href="{course['url']}" target="_blank" class="course-link-button" 
                               style="display: block; text-align: center;">
                                🚀 Access on {course['platform']}
                            </a>
                        </div>
                        """
                        st.markdown(html_content, unsafe_allow_html=True)
            else:
                st.info("No courses found. Try a different skill or filter!")

def main_app():
    # Initialize components
    career_recommender = EnhancedCareerRecommender()
    
    # Sidebar with menu-style navigation
    with st.sidebar:
        st.markdown("""
        <style>
        /* Custom styling for sidebar menu */
        .sidebar-menu {
            background: #f8f9fa;
            border-radius: 15px;
            padding: 10px;
            margin-bottom: 20px;
        }
        .menu-item {
            padding: 12px 15px;
            margin: 5px 0;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            font-weight: 500;
            color: #333;
        }
        .menu-item:hover {
            background: linear-gradient(135deg, #667eea20 0%, #764ba220 100%);
            transform: translateX(5px);
        }
        .menu-item.active {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        }
        .menu-icon {
            margin-right: 10px;
            font-size: 1.2rem;
        }
        .sidebar-divider {
            height: 1px;
            background: linear-gradient(90deg, transparent, #667eea, transparent);
            margin: 20px 0;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # App Logo/Title
        st.markdown("""
        <div style="text-align: center; margin-bottom: 30px;">
            <h3 style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                      -webkit-background-clip: text; 
                      -webkit-text-fill-color: transparent; 
                      font-weight: 800; margin-bottom: 5px;">
                🚀 CareerSense.AI
            </h3>
            <p style="color: #666; font-size: 0.9rem;">Your Career Growth Companion</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation Menu
        st.markdown("### 📍 Navigation")
        st.markdown('<div class="sidebar-menu">', unsafe_allow_html=True)
        
        # Define menu items
        menu_items = [
            ("📄", "Resume Analysis", "resume"),
            ("🎯", "Career Match", "match"),
            ("💼", "Live Jobs", "jobs"),
            ("🎓", "Free Courses", "courses"),
            ("📈", "Insights", "insights")
        ]
        
        # Get current page from URL or session state
        if 'current_page' not in st.session_state:
            st.session_state.current_page = "resume"
        
        # Display menu items
        for icon, label, page_key in menu_items:
            is_active = st.session_state.current_page == page_key
            
            if is_active:
                st.markdown(f"""
                <div class="menu-item active">
                    <span class="menu-icon">{icon}</span>
                    <span>{label}</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                if st.button(f"{icon} {label}", key=f"btn_{page_key}", 
                           use_container_width=True, 
                           help=f"Go to {label}"):
                    st.session_state.current_page = page_key
                    st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Quick Analysis Section
        st.markdown("### ⚡ Quick Analysis")
        with st.expander("Fill your profile", expanded=True):
            quick_skills = st.text_area(
                "Your Skills (comma separated)",
                "Python, SQL, Data Analysis, AWS",
                height=100,
                key="quick_skills_input"
            )
            
            quick_experience = st.slider("Years of Experience", 0, 20, 3, 
                                        key="quick_exp_slider")
            
            if st.button("🚀 Analyze Profile", use_container_width=True,
                        type="primary"):
                st.session_state.profile_skills = quick_skills
                st.session_state.profile_experience = quick_experience
                st.session_state.recommendations = None
                st.success("Profile saved! Go to Career Match for analysis.")
    
    # Get the current page from session state
    app_mode = st.session_state.current_page
    
    # Map page keys to display names
    page_display_map = {
        "resume": "📄 Resume Analysis",
        "match": "🎯 Career Match",
        "jobs": "💼 Live Jobs",
        "courses": "🎓 Free Courses",
        "insights": "📈 Insights"
    }
    
    # Main content header
    st.markdown(f'<h1 class="main-header">{page_display_map.get(app_mode, "CareerSense.AI")}</h1>', unsafe_allow_html=True)
    
    # Route to correct page based on selected menu
    if app_mode == "resume":
        show_resume_analysis(career_recommender)
    elif app_mode == "match":
        show_career_match(career_recommender)
    elif app_mode == "jobs":
        show_live_jobs(career_recommender)
    elif app_mode == "courses":
        show_free_courses(career_recommender)
    elif app_mode == "insights":
        show_insights(career_recommender)

if __name__ == "__main__":
    main_app()