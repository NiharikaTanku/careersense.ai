import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import re
import json
import io
import base64
from datetime import datetime
from typing import Dict, List, Tuple
import random
import pdfplumber
import PyPDF2
from io import BytesIO
import time
import urllib.parse

# Page config
st.set_page_config(
    page_title="CareerSense.AI - Resume to Career",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------
# Global CSS (your full stylesheet)
# -------------------------
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
    
    .skill-badge-missing {
        display: inline-block;
        background: linear-gradient(135deg, #ffc107 0%, #fd7e14 100%);
        color: black;
        padding: 4px 12px;
        margin: 2px 4px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
    }
    
    /* Job cards */
    .job-card {
        background: white;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        border-left: 4px solid #667eea;
        transition: transform 0.2s ease;
    }
    .job-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    /* Course cards */
    .course-card {
        background: white;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        border-left: 4px solid #4CAF50;
        transition: transform 0.2s ease;
    }
    .course-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    /* Platform badges */
    .platform-badge {
        background: linear-gradient(135deg, #6c757d, #495057);
        color: white;
        padding: 2px 8px;
        border-radius: 10px;
        font-size: 0.7rem;
        font-weight: 600;
    }
    .platform-badge-coursera { background: linear-gradient(135deg, #0056D2, #003D82); color: white; }
    .platform-badge-edx { background: linear-gradient(135deg, #00A2B1, #007B8A); color: white; }
    .platform-badge-udemy { background: linear-gradient(135deg, #EC5252, #992337); color: white; }
    .platform-badge-fcc { background: linear-gradient(135deg, #0A0A23, #000000); color: white; }
    .platform-badge-youtube { background: linear-gradient(135deg, #FF0000, #CC0000); color: white; }

    /* Level badges */
    .level-badge-beginner { background: linear-gradient(135deg, #28a745, #1e7e34); color: white; padding: 2px 8px; border-radius: 10px; font-size: 0.7rem; font-weight: 600; }
    .level-badge-intermediate { background: linear-gradient(135deg, #ffc107, #e0a800); color: black; padding: 2px 8px; border-radius: 10px; font-size: 0.7rem; font-weight: 600; }
    .level-badge-advanced { background: linear-gradient(135deg, #dc3545, #c82333); color: white; padding: 2px 8px; border-radius: 10px; font-size: 0.7rem; font-weight: 600; }

    /* Salary badges */
    .salary-badge { background: linear-gradient(135deg, #20c997, #17a2b8); color: white; padding: 3px 10px; border-radius: 15px; font-weight: 600; font-size: 0.8rem; }

    /* Match badges */
    .match-badge-high { background: linear-gradient(135deg, #28a745, #20c997); color: white; padding: 4px 12px; border-radius: 15px; font-weight: bold; font-size: 0.9rem; text-align: center; }
    .match-badge-medium { background: linear-gradient(135deg, #ffc107, #fd7e14); color: white; padding: 4px 12px; border-radius: 15px; font-weight: bold; font-size: 0.9rem; text-align: center; }
    .match-badge-low { background: linear-gradient(135deg, #dc3545, #e83e8c); color: white; padding: 4px 12px; border-radius: 15px; font-weight: bold; font-size: 0.9rem; text-align: center; }

    /* Buttons */
    .job-link-button { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 6px 15px; border-radius: 20px; text-decoration: none; font-weight: 600; font-size: 0.8rem; display: inline-block; transition: all 0.3s ease; border: none; cursor: pointer; }
    .job-link-button:hover { transform: translateY(-2px); box-shadow: 0 3px 10px rgba(102, 126, 234, 0.3); color: white; text-decoration: none; }
    .course-link-button { background: linear-gradient(135deg, #4CAF50, #45a049); color: white; padding: 6px 15px; border-radius: 20px; text-decoration: none; font-weight: 600; font-size: 0.8rem; display: inline-block; transition: all 0.3s ease; border: none; cursor: pointer; }
    .course-link-button:hover { transform: translateY(-2px); box-shadow: 0 3px 10px rgba(76, 175, 80, 0.3); color: white; text-decoration: none; }

    .learning-path-container { background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border-radius: 10px; padding: 15px; margin: 15px 0; border-left: 4px solid #667eea; }
    .path-step { background: white; border-radius: 8px; padding: 12px; margin: 8px 0; box-shadow: 0 1px 5px rgba(0,0,0,0.03); border-left: 3px solid #4CAF50; }
    .path-step-number { background: #4CAF50; color: white; width: 25px; height: 25px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; font-weight: bold; margin-right: 8px; font-size: 0.8rem; }
    
    /* Career Overview Card */
    .overview-card {
        background: white;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        border-left: 4px solid #667eea;
    }
    
    /* Metrics Grid for Overview */
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 10px;
        margin: 15px 0;
    }
    
    .metric-box {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 8px;
        padding: 12px;
        text-align: center;
        border: 1px solid #e0e0e0;
    }
    
    .metric-label {
        font-size: 0.75rem;
        color: #6c757d;
        margin-bottom: 3px;
        font-weight: 500;
    }
    
    .metric-value {
        font-size: 1rem;
        font-weight: 700;
        color: #2c3e50;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        background-color: #f8f9fa;
        padding: 4px;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 40px;
        white-space: pre-wrap;
        background-color: white;
        border-radius: 8px;
        color: #495057;
        border: 1px solid #dee2e6;
        font-weight: 500;
        padding: 0 15px;
        font-size: 0.85rem;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #667eea !important;
        color: white !important;
        border-color: #667eea !important;
    }

    /* Custom scrollbar */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #f1f1f1; border-radius: 8px; }
    ::-webkit-scrollbar-thumb { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 8px; }
    ::-webkit-scrollbar-thumb:hover { background: linear-gradient(135deg, #5a6fd8 0%, #6a3f8f 100%); }

    /* Card animations */
    @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
    .fade-in { animation: fadeIn 0.3s ease-out; }

    /* Navigation button styling */
    .stButton > button {
        width: 100% !important;
        margin-bottom: 8px !important;
        height: 45px !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        transition: all 0.3s ease !important;
    }

    /* Active button styling */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border-color: #667eea !important;
        color: white !important;
        box-shadow: 0 2px 5px rgba(102, 126, 234, 0.2) !important;
    }

    /* Inactive button styling */
    .stButton > button[kind="secondary"] {
        background: linear-gradient(135deg, #6c757d 0%, #495057 100%) !important;
        border-color: #6c757d !important;
        color: white !important;
    }

    /* Hover effects */
    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1) !important;
    }

    .stButton > button[kind="primary"]:hover {
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3) !important;
    }
    
    /* Career Card */
  /*  .career-card {
        background: white;
        border-radius: 15px;
        padding: 20px;
        margin: 20px 0;
        box-shadow: 0 6px 20px rgba(0,0,0,0.08);
        border-top: 5px solid #667eea;
    }
            */
</style>
""", unsafe_allow_html=True)

# -------------------------
# Session state initialization
# -------------------------
if 'resume_data' not in st.session_state:
    st.session_state.resume_data = None
if 'recommendations' not in st.session_state:
    st.session_state.recommendations = None
if 'current_page' not in st.session_state:
    st.session_state.current_page = "resume"

# -------------------------
# Resume parsing & helper classes
# -------------------------
class ResumeParser:
    """Parse resumes from PDF and extract skills, experience, and education"""
    def __init__(self):
        self.common_skills = [
            'python','java','javascript','sql','aws','azure','gcp','tensorflow','pytorch',
            'pandas','numpy','scikit-learn','docker','kubernetes','react','node.js',
            'html','css','tableau','power bi','spark','hadoop','nlp','computer vision',
            'linux','git','jenkins'
        ]

    def extract_text_from_pdf(self, pdf_file) -> str:
        text = ""
        try:
            pdf_file.seek(0)
            with pdfplumber.open(BytesIO(pdf_file.read())) as pdf:
                for i, page in enumerate(pdf.pages):
                    # extract first few pages only for speed
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                        if i >= 6:
                            break
        except Exception:
            # fallback to PyPDF2
            try:
                pdf_file.seek(0)
                reader = PyPDF2.PdfReader(pdf_file)
                for i, page in enumerate(reader.pages):
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                        if i >= 6:
                            break
            except Exception:
                return ""
        return text

    def extract_skills(self, text: str) -> List[str]:
        if not text:
            return []
        txt = text.lower()
        found = []
        for s in self.common_skills:
            if s in txt and s.title() not in found:
                found.append(s.title())
        return found[:30]

    def extract_experience(self, text: str) -> int:
        if not text:
            return 0
        patterns = [r'(\d+)\s+years?', r'(\d+)\+?\s+yrs?', r'(\d+)\s+yrs?']
        for pat in patterns:
            m = re.search(pat, text.lower())
            if m:
                try:
                    return int(m.group(1))
                except:
                    continue
        return 2

    def extract_education(self, text: str) -> List[str]:
        if not text:
            return []
        edu_words = ['bachelor', 'master', 'phd', 'degree', 'university', 'college']
        sentences = re.split(r'[.!?\n]', text)
        out = []
        for s in sentences:
            if any(w in s.lower() for w in edu_words) and len(s.strip()) > 10:
                out.append(s.strip())
                if len(out) >= 3:
                    break
        return out

    def parse_resume(self, file) -> Dict:
        text = self.extract_text_from_pdf(file)
        if not text or len(text.strip()) < 20:
            return {
                'skills': ['Python', 'SQL', 'Communication'],
                'experience': 2,
                'education': ['Bachelor\'s Degree'],
                'raw_text': text or ''
            }
        return {
            'skills': self.extract_skills(text),
            'experience': self.extract_experience(text),
            'education': self.extract_education(text),
            'raw_text': text[:2000]
        }

# -------------------------
# Free Job provider (fallback & demo)
# -------------------------
class FreeJobAPI:
    """Generates friendly job-like results and job board URLs"""
    def __init__(self):
        self.platform_urls = {
            'Indeed': 'https://www.indeed.com/jobs?q=',
            'LinkedIn': 'https://www.linkedin.com/jobs/search?keywords=',
            'Glassdoor': 'https://www.glassdoor.com/Job/jobs.htm?sc.keyword=',
            'WeWorkRemotely': 'https://weworkremotely.com/categories/remote-',
            'AngelList': 'https://angel.co/jobs?keyword=',
            'Google Jobs': 'https://www.google.com/search?q='
        }
        self.sample_companies = ['TechCorp Solutions','Digital Innovations Inc','Cloud Systems LLC','Data Analytics Pro','AI Research Labs','Web Development Hub','Mobile First Tech','Enterprise Solutions Inc']

    def get_job_openings(self, role: str, location: str='remote', count: int=8) -> List[Dict]:
        jobs = []
        encoded = urllib.parse.quote(role + " " + location)
        platforms = list(self.platform_urls.keys())
        for i in range(count):
            platform = platforms[i % len(platforms)]
            jobs.append({
                'title': f"{role}",
                'company': random.choice(self.sample_companies),
                'location': location.title(),
                'salary': random.choice(['₹8–12 LPA','₹10–15 LPA','₹12–20 LPA']),
                'posted': f'{random.randint(1,10)} days ago',
                'description': f'Seeking an experienced {role} to join an exciting team. Strong communication and technical skills required.',
                'skills': random.sample(['Python','SQL','Machine Learning','AWS','Docker','Kubernetes','React','Node.js'], k=4),
                'url': f"{self.platform_urls.get(platform)}{encoded}",
                'platform': platform,
                'experience': f'{random.randint(1,6)}+ years',
                'type': random.choice(['Full-time','Remote','Contract'])
            })
        return jobs

# -------------------------
# Enhanced Learning API (courses & paths)
# -------------------------
class EnhancedLearningAPI:
    def __init__(self):
        self.platform_urls = {
            'Coursera': 'https://www.coursera.org/search?query=',
            'freeCodeCamp': 'https://www.freecodecamp.org/search?q=',
            'edX': 'https://www.edx.org/search?q=',
            'Udemy': 'https://www.udemy.com/courses/search/?q=',
            'YouTube': 'https://www.youtube.com/results?search_query=learn+'
        }
        # Expanded course catalog
        self.popular_courses = {
            'python': [
                {'name':'Python for Everybody','platform':'Coursera','url':'https://www.coursera.org/specializations/python','description':'Complete Python programming course for beginners to advanced'},
                {'name':'Python Crash Course','platform':'YouTube','url':'https://www.youtube.com/results?search_query=python+crash+course','description':'Quick introduction to Python programming'}
            ],
            'machine learning': [
                {'name':'Machine Learning (Andrew Ng)','platform':'Coursera','url':'https://www.coursera.org/learn/machine-learning','description':'The most popular ML course by Andrew Ng'},
                {'name':'ML with Python','platform':'freeCodeCamp','url':'https://www.freecodecamp.org/learn/machine-learning-with-python','description':'Free machine learning curriculum'}
            ],
            'sql': [
                {'name':'SQL for Data Science','platform':'Coursera','url':'https://www.coursera.org/learn/sql-for-data-science','description':'Learn SQL specifically for data analysis'},
                {'name':'SQL Tutorial','platform':'YouTube','url':'https://www.youtube.com/results?search_query=sql+tutorial','description':'Complete SQL tutorial for beginners'}
            ],
            'aws': [
                {'name':'AWS Cloud Practitioner','platform':'Coursera','url':'https://www.coursera.org/learn/aws-cloud-practitioner','description':'AWS fundamentals certification prep'},
                {'name':'AWS Tutorial','platform':'YouTube','url':'https://www.youtube.com/results?search_query=aws+tutorial','description':'Complete AWS tutorial series'}
            ],
            'react': [
                {'name':'React JS Course','platform':'freeCodeCamp','url':'https://www.freecodecamp.org/news/tag/react/','description':'Learn React JS from scratch'},
                {'name':'React Tutorial','platform':'YouTube','url':'https://www.youtube.com/results?search_query=react+tutorial','description':'Modern React tutorial'}
            ]
        }
        self.learning_paths = {
            'Data Scientist': [
                {'step':1,'skill':'Python Programming','duration':'2 months','resources':['Coursera','Kaggle']},
                {'step':2,'skill':'Statistics & Probability','duration':'1 month','resources':['Khan Academy','edX']},
                {'step':3,'skill':'Machine Learning Basics','duration':'2 months','resources':['Coursera','Fast.ai']},
                {'step':4,'skill':'Data Visualization','duration':'1 month','resources':['Tableau','Matplotlib']},
                {'step':5,'skill':'Real-world Projects','duration':'2 months','resources':['Kaggle','GitHub']}
            ],
            'Software Engineer': [
                {'step':1,'skill':'Data Structures & Algorithms','duration':'2 months','resources':['LeetCode','Coursera']},
                {'step':2,'skill':'Programming Language','duration':'2 months','resources':['freeCodeCamp','Udemy']},
                {'step':3,'skill':'Version Control (Git)','duration':'2 weeks','resources':['GitHub','YouTube']},
                {'step':4,'skill':'Framework (React/Node)','duration':'2 months','resources':['Documentation','Tutorials']},
                {'step':5,'skill':'Build Portfolio Projects','duration':'2 months','resources':['GitHub','Personal Projects']}
            ],
            'DevOps Engineer': [
                {'step':1,'skill':'Linux Fundamentals','duration':'1 month','resources':['Linux Academy','YouTube']},
                {'step':2,'skill':'Cloud Computing (AWS)','duration':'2 months','resources':['AWS Training','Coursera']},
                {'step':3,'skill':'Containers (Docker)','duration':'1 month','resources':['Docker Docs','YouTube']},
                {'step':4,'skill':'Orchestration (K8s)','duration':'2 months','resources':['Kubernetes Docs','Udemy']},
                {'step':5,'skill':'CI/CD Pipeline','duration':'1 month','resources':['Jenkins','GitHub Actions']}
            ],
            'Data Analyst': [
                {'step':1,'skill':'SQL Fundamentals','duration':'1 month','resources':['Mode Analytics','Coursera']},
                {'step':2,'skill':'Excel/Spreadsheets','duration':'1 month','resources':['Google Sheets','YouTube']},
                {'step':3,'skill':'Data Visualization','duration':'1 month','resources':['Tableau','Power BI']},
                {'step':4,'skill':'Python for Analysis','duration':'2 months','resources':['DataCamp','Kaggle']},
                {'step':5,'skill':'Business Analytics','duration':'1 month','resources':['Case Studies','Practice']}
            ]
        }

    def get_platform_badge_class(self, platform: str) -> str:
        return {
            'Coursera':'platform-badge-coursera',
            'edX':'platform-badge-edx',
            'Udemy':'platform-badge-udemy',
            'freeCodeCamp':'platform-badge-fcc',
            'YouTube':'platform-badge-youtube'
        }.get(platform, 'platform-badge')

    def get_courses(self, skills: List[str], count: int=8) -> List[Dict]:
        courses = []
        for s in skills[:4]:
            key = s.lower()
            if key in self.popular_courses:
                courses.extend(self.popular_courses[key])
            else:
                # fallback synthesized course
                courses.append({
                    'name':f'Master {s} - Complete Course',
                    'platform':'YouTube',
                    'url':f'https://www.youtube.com/results?search_query={urllib.parse.quote(s)}',
                    'description':f'Learn {s} from beginner to advanced level'
                })
            if len(courses) >= count:
                break
        return courses[:count]

    def get_learning_path(self, role: str) -> List[Dict]:
        return self.learning_paths.get(role, [])

# -------------------------
# Career recommender using above building blocks
# -------------------------
class EnhancedCareerRecommender:
    def __init__(self):
        self.job_api = FreeJobAPI()
        self.learning_api = EnhancedLearningAPI()
        self.resume_parser = ResumeParser()
        self.job_roles = self._create_job_roles_dataset()

    def _create_job_roles_dataset(self) -> pd.DataFrame:
        data = {
            'role':['Data Scientist','Software Engineer','DevOps Engineer','Data Analyst'],
            'required_skills':['Python,Machine Learning,SQL','html,css,Java,Python,Algorithms','AWS,Docker,Kubernetes','SQL,Excel,Tableau'],
            'experience_level':[3,3,3,2],
            'salary_range':['$120k-$160k','$100k-$140k','$110k-$150k','$80k-$110k'],
            'demand_level':['High','Very High','High','High'],
            'growth_outlook':['35%','30%','38%','25%']
        }
        return pd.DataFrame(data)

    def calculate_match_score(self, user_skills: List[str], user_experience: int, target_role: str) -> Tuple[float,List[str],List[str]]:
        role_row = self.job_roles[self.job_roles['role']==target_role]
        if role_row.empty:
            return 0.0,[],[]
        req = [s.strip().lower() for s in role_row.iloc[0]['required_skills'].split(',')]
        lower = [s.lower() for s in user_skills]
        matched = [r.title() for r in req if any(r in u or u in r for u in lower)]
        missing = [r.title() for r in req if r.title() not in matched]
        skill_score = len(matched)/max(len(req),1)
        req_exp = role_row.iloc[0]['experience_level']
        exp_score = 1.0 if user_experience >= req_exp else user_experience/max(req_exp,1)
        total = 0.7*skill_score + 0.3*exp_score
        return round(min(total*100,100),2), matched, missing

    def recommend_careers(self, user_skills: List[str], user_experience: int, top_n: int=5):
        recs = []
        for role in self.job_roles['role']:
            score, matched, missing = self.calculate_match_score(user_skills, user_experience, role)
            row = self.job_roles[self.job_roles['role']==role].iloc[0]
            jobs = self.job_api.get_job_openings(role, 'remote', 8)
            courses = self.learning_api.get_courses(missing[:3])
            learning_path = self.learning_api.get_learning_path(role)
            recs.append({
                'role': role,
                'match_score': score,
                'matched_skills': matched,
                'missing_skills': missing,
                'salary_range': row['salary_range'],
                'experience_level': row['experience_level'],
                'demand_level': row['demand_level'],
                'growth_outlook': row['growth_outlook'],
                'job_openings': jobs,
                'courses': courses,
                'learning_path': learning_path
            })
        recs = sorted(recs, key=lambda x: x['match_score'], reverse=True)
        return recs[:top_n]

# -------------------------
# UI helper renderers
# -------------------------
def render_job_card(job: Dict):
    skills_html = ''.join([f'<span class="skill-badge" style="font-size:0.7rem; padding:2px 8px;">{s}</span> ' for s in job.get('skills', [])[:3]])
    html = f"""
    <div class="job-card fade-in">
      <div style="display:flex; justify-content:space-between; align-items:start; margin-bottom:8px;">
        <h4 style="margin:0; color:#2c3e50; font-size:1rem;">{job.get('title','')}</h4>
        <span class="platform-badge" style="font-size:0.65rem;">{job.get('platform','')[:10]}</span>
      </div>
      <p style="margin:3px 0; color:#555; font-size:0.9rem;"><strong style="color:#667eea;">🏢 Company:</strong> {job.get('company','')}</p>
      <p style="margin:3px 0; color:#555; font-size:0.9rem;"><strong style="color:#667eea;">📍 Location:</strong> {job.get('location','')}</p>
      <p style="margin:5px 0;"><span class="salary-badge">💰 {job.get('salary','')}</span></p>
      <div style="margin:10px 0; font-size:0.8rem;"><strong style="color:#667eea;">🛠️ Skills:</strong><br>{skills_html}</div>
      <div style="display:flex; justify-content:space-between; align-items:center; margin-top:12px;">
        <span style="color:#666; font-size:0.8rem;">⏳ {job.get('experience','2+ years')}</span>
        <a href="{job.get('url','#')}" target="_blank" class="job-link-button">Apply Now</a>
      </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def render_course_card(course: Dict, learning_api: EnhancedLearningAPI):
    platform_badge = learning_api.get_platform_badge_class(course.get('platform','YouTube'))
    html = f"""
    <div class="course-card fade-in">
      <div style="display:flex; justify-content:space-between; align-items:start;">
        <h4 style="margin:0; color:#2c3e50; font-size:1rem;">{course.get('name','')}</h4>
        <span class="{platform_badge}" style="font-size:0.65rem;">{course.get('platform','')}</span>
      </div>
      <p style="color:#555; margin-top:8px; font-size:0.9rem;">{course.get('description','')}</p>
      <div style="margin-top:12px;">
        <a href="{course.get('url')}" target="_blank" class="course-link-button">View Course</a>
      </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def display_learning_path(learning_path: List[Dict]):
    if not learning_path:
        st.info("No learning path available")
        return
    
    for step in learning_path[:5]:
        resources_html = ' '.join([f'<span class="skill-badge" style="font-size:0.7rem; padding:2px 6px;">{r}</span>' for r in step.get('resources',[])])
        st.markdown(f"""
            <div class="path-step">
              <div style="display:flex; align-items:center; margin-bottom:5px;">
                <span class="path-step-number">{step.get('step')}</span>
                <h5 style="margin:0; font-size:0.9rem;">{step.get('skill')}</h5>
              </div>
              <p style="margin:2px 0; font-size:0.8rem;"><strong>⏱️ Duration:</strong> {step.get('duration')}</p>
              <p style="margin:2px 0; font-size:0.8rem;"><strong>📚 Resources:</strong> {resources_html}</p>
            </div>
        """, unsafe_allow_html=True)

def display_role_tabs(role_data: Dict, cr: EnhancedCareerRecommender, index: int):
    """Display 4 tabs side by side for each role"""
    
    # Display the role header with match score
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown(f"### {index + 1}. {role_data['role']}")
    with col2:
        cls = "match-badge-high" if role_data['match_score']>=80 else ("match-badge-medium" if role_data['match_score']>=60 else "match-badge-low")
        st.markdown(f"<div class='{cls}' style='text-align:center; margin-top:10px;'>{role_data['match_score']}% Match</div>", unsafe_allow_html=True)
    
    # Create 4 tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Career Overview", "🛣️ Learning Path", "🎓 Courses", "💼 Job Openings"])
    
    with tab1:
        # Career Overview Tab
        st.markdown("#### Career Overview")
        
        # Metrics grid
        html = f"""
        <div class="overview-card">
            <div class="metrics-grid">
                <div class="metric-box">
                    <div class="metric-label">Salary Range</div>
                    <div class="metric-value">{role_data['salary_range']}</div>
                </div>
                <div class="metric-box">
                    <div class="metric-label">Growth Outlook</div>
                    <div class="metric-value">{role_data['growth_outlook']}</div>
                </div>
                <div class="metric-box">
                    <div class="metric-label">Min Experience</div>
                    <div class="metric-value">{role_data['experience_level']}+ yrs</div>
                </div>
                <div class="metric-box">
                    <div class="metric-label">Demand Level</div>
                    <div class="metric-value">{role_data['demand_level']}</div>
                </div>
            </div>
            
           
        </div>

        """

        
        # Add matched skills
        if role_data['matched_skills']:
            html+='<h5 style="color:#2c3e50; margin-bottom:10px;">✅ Matching Skills</h5>'
            for skill in role_data['matched_skills'][:8]:
                
                html += f'<span class="skill-badge">{skill}</span> '
        else:
            html += '<p style="color: #6c757d; font-style: italic;">No matching skills found</p>'
        
        html += """
                
            
           
        """
        
        # Add missing skills
       
        if role_data['missing_skills']:
            html+='<h5 style="color:#2c3e50; margin-bottom:10px;">📚 Skills to Develop</h5>'
            
            for skill in role_data['missing_skills'][:8]:
                 html += f'<span class="skill-badge-missing">{skill}</span> '
                
        else:
            html += '<p style="color: #6c757d; font-style: italic;">All required skills matched!</p>'
        
        html += """
                </div>
            </div>
        </div>
        """
        
        st.markdown(html, unsafe_allow_html=True)
    
    with tab2:
        # Learning Path Tab
        st.markdown("#### Learning Path")
        display_learning_path(role_data['learning_path'])
    
    with tab3:
        # Courses Tab
        st.markdown("#### Recommended Courses")
        if role_data['courses']:
            for course in role_data['courses'][:4]:
                render_course_card(course, cr.learning_api)
        else:
            st.info("No courses available")
    
    with tab4:
        # Job Openings Tab
        st.markdown("#### Job Openings")
        if role_data['job_openings']:
            for job in role_data['job_openings'][:4]:
                render_job_card(job)
        else:
            st.info("No job openings available")

# -------------------------
# Resume analysis flow
# -------------------------
def analyze_resume_and_recommend(cr: EnhancedCareerRecommender, uploaded_file):
    try:
        progress = st.progress(0)
        status = st.empty()
        status.text("📄 Parsing resume")
        progress.progress(25)
        resume_data = cr.resume_parser.parse_resume(uploaded_file)
        st.session_state.resume_data = resume_data
        status.text("🔍 Generating recommendations")
        progress.progress(60)
        recommendations = cr.recommend_careers(resume_data['skills'], resume_data['experience'])
        st.session_state.recommendations = recommendations
        progress.progress(100)
        status.empty()
        progress.empty()
        st.success("Analysis complete")
    except Exception as e:
        st.error(f"Failed to analyze resume: {e}")
        st.session_state.resume_data = {'skills':['Python','SQL'],'experience':2,'education':['Bachelor'],'raw_text':''}
        st.session_state.recommendations = cr.recommend_careers(['Python','SQL'], 2)

def display_resume_results():
    rd = st.session_state.resume_data
    st.markdown("### 📊 Resume Analysis Results")
    c1,c2,c3 = st.columns(3)
    with c1:
        st.markdown("#### 🛠 Skills Found")
        if rd['skills']:
            for s in rd['skills'][:10]:
                st.markdown(f"<span class='skill-badge'>{s}</span>", unsafe_allow_html=True)
    with c2:
        st.markdown("#### 🎓 Education")
        if rd['education']:
            for e in rd['education']:
                st.markdown(f"- {e}")
    with c3:
        st.markdown("#### 💼 Experience")
        st.markdown(f"**{rd['experience']} years**")
        st.progress(min(rd['experience']/10,1.0))
    with st.expander("📝 Extracted Text"):
        st.text(rd.get('raw_text','')[:1000])

# -------------------------
# Main UI pages
# -------------------------
def show_resume_page(cr: EnhancedCareerRecommender):
    st.markdown("<br>", unsafe_allow_html=True)
    col1,col2 = st.columns([2,1])
    with col1:
        st.markdown("### Upload Your Resume (PDF)")
        uploaded_file = st.file_uploader("Choose PDF", type=["pdf"])
        if uploaded_file:
            if st.button("🔍 Analyze Resume", use_container_width=True):
                analyze_resume_and_recommend(cr, uploaded_file)
    with col2:
        st.markdown("### Tips")
        st.markdown("- Use a text-based PDF (not scanned) for best extraction")
        st.markdown("- Mention skills and years of experience clearly")
    
    if st.session_state.resume_data:
        display_resume_results()
    
    if st.session_state.recommendations:
        display_recommendations(cr)

def display_recommendations(cr: EnhancedCareerRecommender):
    recs = st.session_state.recommendations
    if not recs:
        return
    
    st.markdown("---")
    st.markdown("## 🎯 Career Recommendations")
    
    for i, rec in enumerate(recs):
        # Create a card for each role with 4 tabs
        st.markdown(f'<div class="career-card">', unsafe_allow_html=True)
        display_role_tabs(rec, cr, i)
        st.markdown('</div>', unsafe_allow_html=True)

def show_match_page(cr: EnhancedCareerRecommender):
    st.markdown("## 🎯 Career Matching")
    default_skills = "Python, SQL, Machine Learning"
    default_exp = 3
    
    with st.form("match_form"):
        skills_in = st.text_area("Your skills (comma separated)", default_skills, height=120)
        exp = st.slider("Years of experience", 0, 30, default_exp)
        submit = st.form_submit_button("Find Matches")
    
    if submit:
        skills = [s.strip() for s in skills_in.split(',') if s.strip()]
        recs = cr.recommend_careers(skills, exp)
        
        if recs:
            st.success(f"Found {len(recs)} career matches")
            
            for i, r in enumerate(recs):
                # Display each role with 4 tabs
                st.markdown(f'<div class="career-card">', unsafe_allow_html=True)
                display_role_tabs(r, cr, i)
                st.markdown('</div>', unsafe_allow_html=True)

def fetch_and_render_jobs(cr: EnhancedCareerRecommender):
    st.markdown("## 💼 Live Job Search")
    col1, col2, col3 = st.columns([2,2,1])
    with col1:
        role = st.text_input("Role / Keywords", "Data Scientist")
    with col2:
        location = st.text_input("Location", "remote")
    with col3:
        count = st.selectbox("Results", [5,10,15,20], index=1)
    
    if st.button("🔍 Search Jobs", use_container_width=True):
        with st.spinner("Searching..."):
            jobs = cr.job_api.get_job_openings(role, location, count)
            
            # Display jobs
            st.markdown(f"### 💼 Job Openings for '{role}' in '{location}'")
            cols = st.columns(2)
            for idx, j in enumerate(jobs):
                with cols[idx % 2]:
                    render_job_card(j)

def show_courses_page(cr: EnhancedCareerRecommender):
    st.markdown("## 🎓 Free Courses")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        skill = st.text_input("Search skill", "Python")
    with col2:
        platform = st.selectbox("Platform", ["All", "Coursera", "freeCodeCamp", "Udemy", "YouTube"])
    
    if st.button("Search Courses", use_container_width=True):
        courses = cr.learning_api.get_courses([skill], 12)
        if courses:
            st.markdown(f"### 🎓 Courses for '{skill}'")
            cols = st.columns(2)
            for i, c in enumerate(courses):
                with cols[i % 2]:
                    render_course_card(c, cr.learning_api)
        else:
            st.info("No courses found")

def show_insights_page(cr: EnhancedCareerRecommender):
    st.markdown("## 📈 Insights")
    
    # Salary chart
    fig, ax = plt.subplots(figsize=(10,6))
    roles = cr.job_roles['role'].tolist()
    salaries = [int(s.split('-')[0].replace('$','').replace('k','')) for s in cr.job_roles['salary_range']]
    ax.barh(roles, salaries, color=['#667eea','#764ba2','#667eea','#764ba2'][:len(roles)])
    ax.set_xlabel('Salary ($ thousands)')
    ax.set_title('Average Salary by Role')
    st.pyplot(fig)
    
    # Skills demand
    st.markdown("### 📊 Top In-Demand Skills")
    skills_data = {
        'Skill': ['Python', 'SQL', 'AWS', 'Machine Learning', 'Docker', 'React', 'Kubernetes', 'Java'],
        'Demand': ['Very High', 'High', 'High', 'Very High', 'High', 'High', 'High', 'Medium'],
        'Average Salary': ['$120k', '$110k', '$130k', '$140k', '$125k', '$115k', '$135k', '$105k']
    }
    skills_df = pd.DataFrame(skills_data)
    st.dataframe(skills_df, use_container_width=True)
    
    # Career roles comparison
    st.markdown("### 🎯 Career Roles Comparison")
    st.dataframe(cr.job_roles[['role','demand_level','salary_range','growth_outlook']], use_container_width=True)

# -------------------------
# Main app layout + sidebar
# -------------------------
def main_app():
    cr = EnhancedCareerRecommender()
    
    # Sidebar
    with st.sidebar:
        st.markdown("""
            <div style="text-align:center;">
                <h3 style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip:text; -webkit-text-fill-color:transparent; font-weight:800;">🚀 CareerSense.AI</h3>
                <p style="color:#666; margin-top:0;">Your career growth companion</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### Navigation")
        
        # Navigation items
        nav_items = [
            ("📄 Resume Analysis", "resume"),
            ("🎯 Career Match", "match"),
            ("💼 Live Jobs", "jobs"),
            ("🎓 Free Courses", "courses"),
            ("📈 Insights", "insights")
        ]
        
        current_page = st.session_state.get('current_page', 'resume')
        
        # Create navigation buttons
        for label, page_key in nav_items:
            # Determine if this button is active
            is_active = (current_page == page_key)
            button_type = "primary" if is_active else "secondary"
            
            if st.button(
                label, 
                key=f"nav_{page_key}",
                use_container_width=True,
                type=button_type
            ):
                st.session_state.current_page = page_key
                st.rerun()
        
        st.markdown("---")
        
        st.markdown("⚡ Quick Profile")
        qskills = st.text_area("Skills (comma separated)", "Python, SQL")
        qexp = st.slider("Experience", 0, 20, 2)
        if st.button("Save Quick Profile", use_container_width=True): 
            st.session_state.profile_skills = [s.strip() for s in qskills.split(',') if s.strip()]
            st.session_state.profile_experience = qexp
            st.success("Profile saved")

    # header
    page = st.session_state.get('current_page','resume')
    title_map = {
        'resume':'CareerSense.AI',
        'match':'🎯 Career Match',
        'jobs':'💼 Live Jobs',
        'courses':'🎓 Free Courses',
        'insights':'📈 Insights'
    }
    st.markdown(f"<h1 class='main-header'>{title_map.get(page,'CareerSense.AI')}</h1>", unsafe_allow_html=True)

    # route
    if page == 'resume':
        show_resume_page(cr)
    elif page == 'match':
        show_match_page(cr)
    elif page == 'jobs':
        fetch_and_render_jobs(cr)
    elif page == 'courses':
        show_courses_page(cr)
    elif page == 'insights':
        show_insights_page(cr)
    else:
        st.info("Select a page from the sidebar")

if __name__ == "__main__":
    main_app()