import streamlit as st  # for ui 
import google.generativeai as genai  # for gemini api 
import json  # for ai response parsing in json format
import pandas as pd  # for result display
import random  # for questions shuffling

# --- Page Configuration ---
st.set_page_config(
    page_title="AI-Powered Dynamic Assessment Engine",  # page_title
    page_icon="🤖",  # page_icon
    layout="wide"  # page_layout
)

# --- Constants and Prompts ---
MODEL_CONFIG = {
    "temperature": 0.4,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
    "response_mime_type": "application/json",
}
MODEL_NAME = "gemini-1.5-flash"

SKILL_EXTRACTION_PROMPT = """
Analyze the job description for a "{role_title}" and extract the top 7 technical skills.
Return a valid JSON list of strings.
Example: ["Java", "Spring Boot", "SQL", "Docker", "AWS"]

Job Description:
---
{job_description}
---
"""

QUESTION_GENERATION_PROMPT = """
Generate {num_questions} multiple-choice questions for the skill: "{skill}".
Return a valid JSON list of objects. Each object must have "skill", "question", "options" (a dictionary), and "correct_answer" (the key of the correct option).

Example:
{{
    "skill": "{skill}",
    "question": "What is the primary purpose of @SpringBootApplication?",
    "options": {{
        "A": "To configure database connections",
        "B": "To enable component scanning and auto-configuration",
        "C": "To define RESTful web services",
        "D": "To manage transaction scopes"
    }},
    "correct_answer": "B"
}}
"""

# --- Core AI Functions ---
@st.cache_data
def get_gemini_model():
    """Configures and returns the Gemini model."""
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        model = genai.GenerativeModel(
            model_name=MODEL_NAME,
            generation_config=MODEL_CONFIG
        )
        return model
    except Exception:
        st.error("Google API key not found. Please add it to your Streamlit secrets.", icon="🚨")
        st.stop()

def extract_skills_from_jd(model, job_description, role_title):
    """Extracts key skills from a job description using the AI model."""
    prompt = SKILL_EXTRACTION_PROMPT.format(role_title=role_title, job_description=job_description)
    try:
        response = model.generate_content(prompt)
        return json.loads(response.text)
    except (json.JSONDecodeError, Exception) as e:
        st.error(f"Error extracting skills: {e}", icon="🚨")
        return None

def generate_assessment_questions(model, skills, num_questions_per_skill=3):
    """Generates assessment questions for a list of skills."""
    all_questions = []
    progress_bar = st.progress(0, text="Generating assessment questions... Please wait.")

    for i, skill in enumerate(skills):
        prompt = QUESTION_GENERATION_PROMPT.format(num_questions=num_questions_per_skill, skill=skill)
        try:
            response = model.generate_content(prompt)
            parsed = json.loads(response.text)

            #  Normalize: always return a list of dicts
            if isinstance(parsed, dict):
                skill_questions = [parsed]
            elif isinstance(parsed, list):
                skill_questions = [q for q in parsed if isinstance(q, dict)]
            else:
                skill_questions = []

            all_questions.extend(skill_questions)
            progress_bar.progress((i + 1) / len(skills), text=f"Generated questions for {skill}...")
        except json.JSONDecodeError:
            st.warning(f"Could not parse questions for skill: {skill}. The AI returned an invalid format.", icon="⚠️")
        except Exception as e:
            st.error(f"An error occurred while generating questions for {skill}: {e}", icon="🚨")
    
    progress_bar.empty()
    return all_questions

# --- UI Page Functions ---
def show_main_page(model):
    """Displays the main page for recruiters to input job details."""
    st.title("🤖 AI-Powered Assessment Engine")
    st.markdown("This tool generates a technical assessment based on a job description.")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("1. Enter Job Details")
        st.session_state.candidate_name = st.text_input("Candidate Name", placeholder="e.g., John Doe")
        role_title = st.text_input("Job Role Title", placeholder="e.g., Senior Java Developer")
        job_description = st.text_area("Paste Job Description Here", height=300, placeholder="Paste the full job description...")

        if st.button("🚀 Generate Assessment", type="primary", use_container_width=True):
            if not role_title or not job_description or not st.session_state.candidate_name:
                st.warning("Please provide candidate name, role title, and a job description.", icon="⚠️")
            else:
                with st.spinner("Analyzing job description and building assessment..."):
                    skills = extract_skills_from_jd(model, job_description, role_title)
                    if skills:
                        st.session_state.skills = skills
                        questions = generate_assessment_questions(model, skills)
                        if questions:
                            random.shuffle(questions)
                            st.session_state.questions = questions
                            st.session_state.role_title = role_title
                            st.session_state.page = "assessment"
                            st.rerun()
                        else:
                            st.error("Failed to generate questions. Please try again.", icon="🚨")
                    else:
                        st.error("Failed to extract skills. Please check the job description.", icon="🚨")
    
    with col2:
        st.subheader("💡 How It Works")
        st.info(
            """
            1.  **Analyze**: The AI reads the job description to identify the most critical technical skills.
            2.  **Generate**: It then creates a custom set of multiple-choice questions for each skill.
            3.  **Assess**: The candidate completes the assessment.
            4.  **Report**: A detailed report is generated for the recruiter, breaking down performance by skill.
            """
        )
        st.markdown("--- \n By Sanya")

def show_assessment_page():
    """Displays the assessment for the candidate to take."""
    st.title(f"Technical Assessment for {st.session_state.candidate_name} ({st.session_state.role_title})")
    st.warning("Please answer all questions. Once submitted, your answers cannot be changed.", icon="✍️")
    st.markdown("---")

    with st.form("assessment_form"):
        candidate_answers = {}
        for i, q in enumerate(st.session_state.questions):
            if not isinstance(q, dict):
                st.warning(f"Invalid question format at index {i}, skipping...", icon="⚠️")
                continue

            st.subheader(f"Question {i+1}")
            st.markdown(f"**Skill: `{q.get('skill', 'N/A')}`**")
            st.markdown(f"##### {q.get('question', 'No question text.')}")

            options_dict = q.get('options', {})
            if not isinstance(options_dict, dict):
                options_dict = {}

            options_list = list(options_dict.values())
            
            user_choice = st.radio(
                "Select your answer:",
                options_list,
                key=f"q_{i}",
                label_visibility="collapsed"
            )
            if user_choice:
                for key, value in options_dict.items():
                    if value == user_choice:
                        candidate_answers[i] = key
                        break
        
        submitted = st.form_submit_button("Submit Final Answers", use_container_width=True, type="primary")

    if submitted:
        st.session_state.candidate_answers = candidate_answers
        st.session_state.page = "results"
        st.rerun()

def show_results_page():
    """Calculates and displays the assessment results."""
    st.title("📊 Candidate Assessment Report")
    
    questions = st.session_state.get('questions', [])
    answers = st.session_state.get('candidate_answers', {})
    skills = st.session_state.get('skills', [])
    
    total_questions = len(questions)
    correct_answers = 0
    skill_scores = {skill: {'correct': 0, 'total': 0} for skill in skills}

    for i, q in enumerate(questions):
        if not isinstance(q, dict):
            continue
        skill = q.get('skill')
        if skill in skill_scores:
            is_correct = answers.get(i) == q.get('correct_answer')
            skill_scores[skill]['total'] += 1
            if is_correct:
                correct_answers += 1
                skill_scores[skill]['correct'] += 1
    
    overall_score = (correct_answers / total_questions) * 100 if total_questions > 0 else 0

    st.subheader(f"Report for: {st.session_state.candidate_name} ({st.session_state.role_title})")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Overall Score", f"{overall_score:.1f}%")
    col2.metric("Correct Answers", f"{correct_answers} / {total_questions}")
    
    if overall_score >= 80:
        rating, emoji = "Strong", "🏆"
    elif overall_score >= 50:
        rating, emoji = "Medium", "👍"
    else:
        rating, emoji = "Weak", "👎"
    col3.metric("Overall Rating", f"{rating} {emoji}")

    st.markdown("---")
    st.subheader("Skill-wise Performance")
    
    skill_data = []
    for skill, scores in skill_scores.items():
        if scores['total'] > 0:
            percentage = (scores['correct'] / scores['total']) * 100
            if percentage >= 80: level = "Strong"
            elif percentage >= 50: level = "Medium"
            else: level = "Weak"
            skill_data.append({
                "Skill": skill, 
                "Correct": scores['correct'], 
                "Total": scores['total'], 
                "Score (%)": percentage, 
                "Proficiency": level
            })
    
    df = pd.DataFrame(skill_data)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("**Performance Chart**")
        st.bar_chart(df, x="Skill", y="Score (%)", color="#4285F4")
    with col2:
        st.markdown("**Detailed Breakdown**")
        st.dataframe(df, hide_index=True, use_container_width=True)

    # Recruiter Export Option
    df_with_meta = df.copy()
    df_with_meta.insert(0, "Candidate Name", st.session_state.candidate_name)
    df_with_meta.insert(1, "Role Title", st.session_state.role_title)
    df_with_meta.insert(2, "Overall Score (%)", f"{overall_score:.1f}%")
    df_with_meta.insert(3, "Overall Rating", rating)

    st.download_button(
        label="📥 Download Report (CSV)",
        data=df_with_meta.to_csv(index=False),
        file_name=f"{st.session_state.candidate_name}_assessment_report.csv",
        mime="text/csv",
        use_container_width=True
    )

    if st.button("Start New Assessment", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# --- Main App Logic (Page Router) ---
model = get_gemini_model()

if "page" not in st.session_state:
    st.session_state.page = "main"

if model:
    if st.session_state.page == "main":
        show_main_page(model)
    elif st.session_state.page == "assessment":
        show_assessment_page()
    elif st.session_state.page == "results":
        show_results_page()
