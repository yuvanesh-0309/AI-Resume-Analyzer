
import streamlit as st
import re
import json
from urllib.request import Request, urlopen
from pypdf import PdfReader


# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI-Powered Resume Analyzer")

st.write(
    "Analyze your resume, identify skill gaps, "
    "and get AI-powered career recommendations."
)

st.divider()


# ==========================================
# 2. SKILLS DATABASE
# ==========================================

skills_database = [
    "python", "java", "c++", "c", "c#", "javascript",
    "html", "css", "php",
    "machine learning", "deep learning",
    "artificial intelligence", "natural language processing",
    "computer vision", "reinforcement learning",
    "generative ai", "large language models",
    "data science", "data analysis", "data visualization",
    "exploratory data analysis", "statistics",
    "probability", "data preprocessing",
    "feature engineering",
    "pandas", "numpy", "matplotlib", "seaborn",
    "scikit-learn", "scipy", "tensorflow",
    "pytorch", "keras", "opencv", "xgboost",
    "streamlit", "flask", "django", "react", "node.js",
    "sql", "mysql", "postgresql", "mongodb",
    "database management",
    "power bi", "tableau", "excel", "power query",
    "git", "github", "gitlab", "docker",
    "jupyter notebook", "vscode",
    "aws", "azure", "google cloud",
    "nlp", "data structures", "algorithms",
    "api", "rest api"
]


# ==========================================
# 3. EXTRACT RESUME TEXT
# ==========================================

def extract_resume_text(pdf_file):

    reader = PdfReader(pdf_file)
    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    return text


# ==========================================
# 4. EXTRACT SKILLS
# ==========================================

def extract_skills(text):

    text = text.lower()
    found_skills = []

    skill_aliases = {
        "machine learning": ["ml"],
        "artificial intelligence": ["ai"],
        "natural language processing": ["nlp"],
        "exploratory data analysis": ["eda"],
        "scikit-learn": ["sklearn"],
        "pytorch": ["torch"],
        "c++": ["cpp"],
        "power bi": ["powerbi"],
        "node.js": ["nodejs"],
        "generative ai": ["genai"]
    }

    for skill in skills_database:

        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

        if re.search(pattern, text):

            found_skills.append(skill)
            continue

        aliases = skill_aliases.get(skill, [])

        for alias in aliases:

            alias_pattern = (
                r"(?<!\w)" + re.escape(alias) + r"(?!\w)"
            )

            if re.search(alias_pattern, text):

                found_skills.append(skill)
                break

    return found_skills


# ==========================================
# 5. RESUME SECTION ANALYSIS
# ==========================================

def analyze_resume_sections(resume_text):

    sections = {
        "Professional Summary": [
            "professional summary", "summary",
            "career objective", "objective"
        ],
        "Education": [
            "education", "academic background",
            "educational qualifications"
        ],
        "Work Experience": [
            "work experience", "experience",
            "employment history"
        ],
        "Projects": [
            "projects", "personal projects",
            "academic projects"
        ],
        "Technical Skills": [
            "technical skills", "skills", "key skills"
        ],
        "Certifications": [
            "certifications", "certificates"
        ],
        "Achievements": [
            "achievements", "awards", "accomplishments"
        ]
    }

    found_sections = []

    for section, headings in sections.items():

        for heading in headings:

            pattern = (
                r"(?im)^\s*" + re.escape(heading) + r"\s*:?\s*$"
            )

            if re.search(pattern, resume_text):

                found_sections.append(section)
                break

    return found_sections


# ==========================================
# 6. CONTACT DETAILS DETECTION
# ==========================================

def detect_contact_details(resume_text):

    email = re.search(
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b',
        resume_text
    )

    phone = re.search(
        r'(?<!\w)(?:\+?\d{1,3}[-.\s]?)?\d{10}(?!\w)',
        resume_text
    )

    linkedin = re.search(
        r'(https?://)?(www\.)?linkedin\.com/in/[A-Za-z0-9_-]+',
        resume_text,
        re.IGNORECASE
    )

    return {
        "Email": email.group() if email else None,
        "Phone": phone.group() if phone else None,
        "LinkedIn": linkedin.group() if linkedin else None
    }


# ==========================================
# 7. EDUCATION ANALYSIS
# ==========================================

def detect_education_details(resume_text):

    education_keywords = [
        "b.tech", "b.e.", "b.sc", "bca",
        "m.tech", "m.sc", "mca",
        "bachelor", "master", "phd",
        "diploma", "degree",
        "university", "college"
    ]

    text = resume_text.lower()
    found_education = []

    for keyword in education_keywords:

        if keyword in text:
            found_education.append(keyword)

    return found_education


# ==========================================
# 8. PROJECT AND EXPERIENCE ANALYSIS
# ==========================================

def analyze_projects_experience(resume_text):

    text = resume_text.lower()

    details = {
        "Projects": [
            "project", "projects",
            "developed", "built", "implemented"
        ],
        "Work Experience": [
            "internship", "intern",
            "work experience",
            "professional experience",
            "employment"
        ]
    }

    results = {}

    for category, keywords in details.items():

        found = [
            keyword for keyword in keywords
            if re.search(
                r"(?<!\w)" + re.escape(keyword) + r"(?!\w)",
                text
            )
        ]

        results[category] = found

    return results


# ==========================================
# 9. AI-POWERED FEEDBACK AND RECOMMENDATIONS
# ==========================================

def generate_ai_feedback(
    resume_text,
    job_description,
    matched_skills,
    missing_skills
):

    prompt = f"""
You are an expert resume reviewer and career advisor.

Analyze the candidate's resume against the job description.

RESUME:
{resume_text[:6000]}

JOB DESCRIPTION:
{job_description[:4000]}

MATCHED SKILLS:
{", ".join(matched_skills) if matched_skills else "None"}

MISSING SKILLS:
{", ".join(missing_skills) if missing_skills else "None"}

IMPORTANT RULES:

1. Treat matched skills as skills found in the resume.
2. Never say a matched skill is missing.
3. Do not claim skills unless the resume supports them.
4. Never invent work experience, projects or certifications.
5. Give practical suggestions suitable for college students and freshers.
6. Distinguish listed skills from skills demonstrated in projects.
7. Do not recommend adding skills already clearly mentioned.
8. Recommend projects that help develop relevant missing skills.
9. Explain how each recommended project could be built.
10. Suggest realistic improvements without exaggerating achievements.

Provide feedback using these headings:

1. Overall Resume Feedback
2. Candidate Strengths
3. Areas for Improvement
4. Specific Resume Improvement Suggestions
5. Missing Skills to Focus On
6. Recommended Projects

For each recommended project, include:
- Project title
- Project description
- Suggested technologies
- Skills the project will help develop

7. Career Development Roadmap

Provide practical next steps for improving the candidate's
resume and preparing for the target job.

Make the feedback accurate, clear and personalized.
"""

    data = {
        "model": "llama3.2:3b",
        "prompt": prompt,
        "stream": False
    }

    request = Request(
        "http://localhost:11434/api/generate",
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    with urlopen(request, timeout=180) as response:

        result = json.loads(
            response.read().decode("utf-8")
        )

    return result.get("response", "No AI feedback received.")


# ==========================================
# 10. RESUME UPLOAD
# ==========================================

st.subheader("1. Upload Your Resume")

uploaded_file = st.file_uploader(
    "Upload your resume (PDF)",
    type=["pdf"]
)


# ==========================================
# 11. JOB DESCRIPTION
# ==========================================

st.subheader("2. Enter Job Description")

job_description = st.text_area(
    "Paste the job description:",
    height=200
)


# ==========================================
# 12. ANALYZE RESUME
# ==========================================

if st.button("Analyze Resume 🚀", type="primary"):

    if uploaded_file is None:

        st.warning("Please upload your resume.")

    elif not job_description.strip():

        st.warning("Please enter a job description.")

    else:

        with st.spinner("Analyzing your resume..."):

            try:

                # Extract resume text
                resume_text = extract_resume_text(uploaded_file)

                if not resume_text.strip():

                    st.error(
                        "No text found. This may be a scanned PDF."
                    )

                else:

                    # Extract skills
                    resume_skills = extract_skills(resume_text)
                    job_skills = extract_skills(job_description)

                    # Extract additional information
                    contact_details = detect_contact_details(
                        resume_text
                    )

                    education_details = detect_education_details(
                        resume_text
                    )

                    found_sections = analyze_resume_sections(
                        resume_text
                    )

                    projects_experience = analyze_projects_experience(
                        resume_text
                    )

                    # Compare skills
                    matched_skills = [
                        skill for skill in job_skills
                        if skill in resume_skills
                    ]

                    missing_skills = [
                        skill for skill in job_skills
                        if skill not in resume_skills
                    ]

                    # Calculate match percentage
                    if job_skills:

                        score = (
                            len(matched_skills) / len(job_skills)
                        ) * 100

                    else:

                        score = 0

                    # Generate AI feedback
                    with st.spinner(
                        "Llama AI is reviewing your resume..."
                    ):

                        ai_feedback = generate_ai_feedback(
                            resume_text,
                            job_description,
                            matched_skills,
                            missing_skills
                        )

                    st.success("Resume analyzed successfully!")

                    # ==================================
                    # PHASE 5: IMPROVED USER INTERFACE
                    # ==================================

                    st.divider()

                    st.header("📊 Resume Analysis Dashboard")

                    col1, col2, col3 = st.columns(3)

                    with col1:

                        st.metric(
                            "Skill Match Score",
                            f"{score:.1f}%"
                        )

                    with col2:

                        st.metric(
                            "Skills Found",
                            len(resume_skills)
                        )

                    with col3:

                        st.metric(
                            "Missing Skills",
                            len(missing_skills)
                        )

                    st.progress(int(score))

                    # Create organized tabs
                    tab1, tab2, tab3, tab4, tab5 = st.tabs([
                        "🎯 Skills Analysis",
                        "🤖 AI Recommendations",
                        "📑 Resume Analysis",
                        "📞 Personal Details",
                        "📄 Resume Text"
                    ])

                    # ==================================
                    # TAB 1: SKILLS ANALYSIS
                    # ==================================

                    with tab1:

                        st.subheader("✅ Matching Skills")

                        if matched_skills:

                            for skill in matched_skills:
                                st.success(skill)

                        else:

                            st.info("No matching skills found.")

                        st.subheader("❌ Missing Skills")

                        if missing_skills:

                            for skill in missing_skills:
                                st.warning(skill)

                        else:

                            st.success(
                                "Your resume includes all detected "
                                "job description skills!"
                            )

                        st.subheader("💡 Improvement Suggestions")

                        if missing_skills:

                            for skill in missing_skills:

                                st.write(
                                    f"📌 Consider learning **{skill}** "
                                    "if it is relevant to your career."
                                )

                        else:

                            st.write(
                                "Continue improving your existing "
                                "skills with practical projects."
                            )

                    # ==================================
                    # TAB 2: AI RECOMMENDATIONS
                    # ==================================

                    with tab2:

                        st.subheader(
                            "🤖 AI-Powered Resume Feedback"
                        )

                        st.markdown(ai_feedback)

                    # ==================================
                    # TAB 3: RESUME ANALYSIS
                    # ==================================

                    with tab3:

                        st.subheader("🎓 Education Analysis")

                        if education_details:

                            st.success(
                                "Education-related details detected:"
                            )

                            for item in education_details:
                                st.write(f"✅ {item.upper()}")

                        else:

                            st.warning(
                                "No education-related details detected."
                            )

                        st.divider()

                        st.subheader("📑 Resume Section Analysis")

                        all_sections = [
                            "Professional Summary",
                            "Education",
                            "Work Experience",
                            "Projects",
                            "Technical Skills",
                            "Certifications",
                            "Achievements"
                        ]

                        for section in all_sections:

                            if section in found_sections:

                                st.success(
                                    f"✅ {section} section found"
                                )

                            else:

                                st.warning(
                                    f"⚠️ {section} section not detected"
                                )

                        st.divider()

                        st.subheader(
                            "💼 Projects and Work Experience Analysis"
                        )

                        for category, keywords in projects_experience.items():

                            if keywords:

                                st.success(
                                    f"✅ {category} keywords found: "
                                    f"{', '.join(keywords)}"
                                )

                            else:

                                st.warning(
                                    f"⚠️ No {category.lower()} "
                                    "keywords detected"
                                )

                        st.caption(
                            "This feature detects keywords only. "
                            "It does not verify project quality "
                            "or employment history."
                        )

                    # ==================================
                    # TAB 4: CONTACT DETAILS
                    # ==================================

                    with tab4:

                        st.subheader(
                            "📞 Contact Details Analysis"
                        )

                        for detail, value in contact_details.items():

                            if value:

                                st.success(
                                    f"✅ {detail}: {value}"
                                )

                            else:

                                st.warning(
                                    f"⚠️ {detail} not found"
                                )

                    # ==================================
                    # TAB 5: EXTRACTED RESUME TEXT
                    # ==================================

                    with tab5:

                        st.subheader(
                            "📄 Extracted Resume Text"
                        )

                        st.text_area(
                            "Resume content",
                            value=resume_text,
                            height=400,
                            disabled=True
                        )

                    # ==================================
                    # PHASE 6: DOWNLOADABLE REPORT
                    # ==================================

                    st.divider()

                    st.header("📥 Download Analysis Report")

                    report_text = f"""
==================================================
       AI-POWERED RESUME ANALYSIS REPORT
==================================================

SKILL MATCH ANALYSIS
--------------------

Skill Match Score: {score:.1f}%

Total Resume Skills: {len(resume_skills)}

Total Job Skills: {len(job_skills)}

Matching Skills:
{', '.join(matched_skills) if matched_skills else 'None'}

Missing Skills:
{', '.join(missing_skills) if missing_skills else 'None'}


EDUCATION ANALYSIS
------------------

{', '.join(education_details) if education_details else 'No education details detected'}


CONTACT DETAILS
---------------

{chr(10).join(
    f'{key}: {value if value else "Not found"}'
    for key, value in contact_details.items()
)}


RESUME SECTIONS
---------------

Sections Found:
{', '.join(found_sections) if found_sections else 'None'}

Projects and Work Experience Keywords:
{chr(10).join(
    f'{key}: {", ".join(value) if value else "None"}'
    for key, value in projects_experience.items()
)}


AI-POWERED FEEDBACK AND RECOMMENDATIONS
---------------------------------------

{ai_feedback}


GENERAL RESUME IMPROVEMENT TIPS
-------------------------------

1. Add relevant technical skills to your resume.
2. Include practical projects related to the job.
3. Highlight internships and certifications.
4. Use measurable achievements wherever possible.
5. Customize your resume for each job application.

==================================================
             END OF REPORT
==================================================
"""

                    st.download_button(
                        label="📥 Download Complete Resume Report",
                        data=report_text,
                        file_name="AI_Resume_Analysis_Report.txt",
                        mime="text/plain",
                        type="primary"
                    )

            except Exception as e:

                st.error(
                    f"Something went wrong: {e}"
                )


# ==========================================
# 13. FOOTER
# ==========================================

st.divider()

st.caption(
    "Built with Python | Streamlit | Ollama | AI Resume Analyzer"
)
