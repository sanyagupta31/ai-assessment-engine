import streamlit as st
import google.generativeai as genai
import json
import pandas as pd
import random
import uuid

# --- Page Config ---
st.set_page_config(
    page_title="AI-Powered Dynamic Assessment Engine",
    page_icon="🤖",
    layout="wide"
)

# --- Constants ---
MODEL_CONFIG = {
    "temperature": 0.4,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
    "response_mime_type": "application/json",
}
MODEL_NAME = "gemini-1.5-flash"

SKILL_EXTRACTION_PROMPT = """
Analyze the job description for a "{role_title}" and extract the top 7 unique technical skills. Ensure there are no duplicates and no overlapping skills (e.g., treat "Java" and "Core Java" as one). Return a valid JSON list of strings.
"""

QUESTION_GENERATION_PROMPT = """
Generate {num_questions} questions for the skill: "{skill}".
You must include:
- 2 multiple-choice questions (MCQ).
- 1 short coding snippet or fill-in-the-blank question.
Return a valid JSON list of objects. Each object must have these fields: "skill", "type" (either "MCQ" or "Coding"), "question", "options" (a dictionary with keys "A", "B", "C", etc. for MCQs, otherwise null), and "correct_answer" (the key for MCQ, e.g., "A", or the text for Coding).
"""

# --- Helper Functions ---
@st.cache_data
def get_gemini_model():
    """Initializes and returns the Gemini model, caching it for performance."""
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    return genai.GenerativeModel(model_name=MODEL_NAME, generation_config=MODEL_CONFIG)

def clean_skills(skills):
    """Removes case-insensitive duplicates from a list of skills."""
    seen = set()
    unique_skills = []
    for s in skills:
        s_low = s.lower().strip()
        if s_low not in seen:
            seen.add(s_low)
            unique_skills.append(s.strip())
    return unique_skills

def extract_skills(model, jd, role):
    """Extracts skills from a job description using the AI model."""
    try:
        prompt = SKILL_EXTRACTION_PROMPT.format(role_title=role, job_description=jd)
        response = model.generate_content(prompt)
        return clean_skills(json.loads(response.text))
    except Exception as e:
        st.error(f"Error extracting skills: {e}")
        return []

def generate_questions(model, skills, num=3):
    """Generates questions for a list of skills using the AI model."""
    all_qs = []
    for skill in skills:
        try:
            prompt = QUESTION_GENERATION_PROMPT.format(num_questions=num, skill=skill)
            response = model.generate_content(prompt)
            parsed = json.loads(response.text)
            if isinstance(parsed, dict): # Handle if model returns a single object
                parsed = [parsed]
            all_qs.extend(parsed)
        except Exception as e:
            st.warning(f"Could not generate questions for '{skill}'. Skipping. Error: {e}")
            continue
    random.shuffle(all_qs)
    return all_qs

# --- Page 1: Main Page ---
def show_main(model):
    """Displays the main page for inputting candidate and job details."""
    st.title("🤖 AI-Powered Dynamic Assessment Engine")
    st.markdown("Enter the candidate's details and the job description to generate a custom technical assessment.")

    if 'assessment_id' not in st.session_state:
        st.session_state.assessment_id = str(uuid.uuid4())[:8]

    st.subheader("Recruiter Input")
    st.session_state.candidate = st.text_input("Candidate Name")
    role = st.text_input("Role Title")
    jd = st.text_area("Job Description", height=200)

    with st.expander("⚙️ Scoring Settings"):
        strong_thr = st.slider("Strong Proficiency Threshold (≥)", 70, 100, 80)
        med_thr = st.slider("Medium Proficiency Threshold (≥)", 40, 79, 50)
        pass_thr = st.slider("Passing Score Threshold (≥)", 40, 100, 60)
        st.session_state.thresholds = (strong_thr, med_thr, pass_thr)

    if st.button("🚀 Generate Assessment", type="primary", use_container_width=True):
        if jd and role and st.session_state.candidate:
            with st.spinner("Analyzing job description and generating questions..."):
                skills = extract_skills(model, jd, role)
                if not skills:
                    st.error("Could not extract any skills. Please refine the job description or check the AI model response.")
                else:
                    questions = generate_questions(model, skills)
                    if not questions:
                        st.error("Failed to generate questions for the extracted skills. Please try again.")
                    else:
                        st.session_state.update({"skills": skills, "questions": questions, "role": role, "page": "assessment"})
                        st.rerun()
        else:
            st.warning("Please fill in all fields: Candidate Name, Role Title, and Job Description.")

# --- Page 2: Assessment Page ---
def show_assessment():
    """Displays the assessment questions to the user."""
    st.title(f"Assessment for {st.session_state.candidate}")
    st.subheader(f"Role: {st.session_state.role}")
    st.write(f"Total Questions: {len(st.session_state.questions)}")
    st.info("Please answer all questions to the best of your ability.")

    with st.form("assessment_form"):
        answers = {}
        for i, q in enumerate(st.session_state.questions):
            st.markdown("---")
            st.subheader(f"Question {i+1}: {q.get('question', 'N/A')}")
            
            q_type = q.get("type", "Coding").upper()

            if q_type == "MCQ" and "options" in q and q["options"]:
                options_data = q.get("options")
                
                if isinstance(options_data, dict):
                    option_keys = sorted(options_data.keys())
                    options_list = [options_data[key] for key in option_keys]
                    
                    user_choice = st.radio("Select an answer:", options_list, key=f"q{i}", label_visibility="collapsed")
                    for key, value in options_data.items():
                        if value == user_choice:
                            answers[i] = key
                            break
                else:
                    options_list = list(options_data)
                    user_choice = st.radio("Select an answer:", options_list, key=f"q{i}", label_visibility="collapsed")
                    answers[i] = user_choice
            
            else:
                answers[i] = st.text_area("Your Answer:", key=f"q{i}", height=100)

        if st.form_submit_button("Submit Assessment", use_container_width=True, type="primary"):
            st.session_state.answers = answers
            st.session_state.page = "results"
            st.rerun()

# --- Page 3: Results Page ---
def show_results():
    """Calculates and displays the assessment results."""
    st.title("📊 Assessment Results Dashboard")
    
    st.info(f"Assessment ID: {st.session_state.assessment_id}")
    
    questions = st.session_state.questions
    answers = st.session_state.answers
    skills = st.session_state.skills
    strong_thr, med_thr, pass_thr = st.session_state.thresholds

    total_questions = len(questions)
    correct_answers = 0
    skill_scores = {s: {"correct": 0, "total": 0} for s in skills}

    for i, q in enumerate(questions):
        skill = q.get("skill")
        user_ans_str = str(answers.get(i, "")).strip().lower()
        correct_ans_val = str(q.get("correct_answer", "")).strip()

        is_correct = False
        if q.get("type") == "MCQ" and isinstance(q.get("options"), dict):
            if user_ans_str == correct_ans_val.lower():
                is_correct = True
            else:
                correct_ans_text = q["options"].get(correct_ans_val.upper(), "").strip().lower()
                if user_ans_str == correct_ans_text:
                    is_correct = True
        else:
            if user_ans_str == correct_ans_val.lower():
                is_correct = True
        
        if skill and skill in skill_scores:
            skill_scores[skill]["total"] += 1
            if is_correct:
                skill_scores[skill]["correct"] += 1
                correct_answers += 1

    overall_score = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
    
    rating = "Weak"
    if overall_score >= strong_thr: rating = "Strong"
    elif overall_score >= med_thr: rating = "Medium"

    final_status = "Fail"
    if overall_score >= pass_thr:
        final_status = "Pass"

    st.header("Overall Performance")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Overall Score", f"{overall_score:.1f}%")
    col2.metric("Proficiency Rating", rating)
    col3.metric("Final Status", final_status)
    st.progress(int(overall_score))

    if final_status == "Pass":
        st.success(f"**Result: PASS** (Score of {overall_score:.1f}% is above the passing threshold of {pass_thr}%)")
    else:
        st.error(f"**Result: FAIL** (Score of {overall_score:.1f}% is below the passing threshold of {pass_thr}%)")

    st.header("Skill-wise Breakdown")
    skill_data = []
    for skill, values in skill_scores.items():
        if values["total"] > 0:
            percentage = (values["correct"] / values["total"]) * 100
            lvl = "Weak"
            if percentage >= strong_thr: lvl = "Strong"
            elif percentage >= med_thr: lvl = "Medium"
            skill_data.append({"Skill": skill, "Score (%)": percentage, "Proficiency": lvl})
    
    if skill_data:
        df = pd.DataFrame(skill_data)
        
        # --- CHANGE: ADDING OVERALL RESULTS TO THE DATAFRAME FOR EXPORT ---
        df['Overall Score (%)'] = round(overall_score, 1)
        df['Overall Proficiency'] = rating
        df['Final Status'] = final_status
        df['Assessment ID'] = st.session_state.assessment_id
        
        # Reordering columns for better readability in the CSV
        column_order = [
            'Assessment ID', 'Skill', 'Score (%)', 'Proficiency',
            'Overall Score (%)', 'Overall Proficiency', 'Final Status'
        ]
        df = df[column_order]

        st.bar_chart(df.set_index("Skill"), y="Score (%)")
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.header("Export Report")
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Report as CSV", 
            data=csv_data, 
            file_name=f"{st.session_state.candidate}_report.csv", 
            mime="text/csv", 
            use_container_width=True
        )
    
    st.markdown("---")
    if st.button("Start New Assessment", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# --- Main App Router ---
def main():
    """Main function to route between pages."""
    try:
        model = get_gemini_model()
        
        if "page" not in st.session_state:
            st.session_state.page = "main"

        if st.session_state.page == "main":
            show_main(model)
        elif st.session_state.page == "assessment":
            show_assessment()
        elif st.session_state.page == "results":
            show_results()
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        st.error("Please ensure your Google API key is correctly configured in your Streamlit secrets and has the Gemini API enabled.")
        if st.button("Restart Application"):
            st.session_state.clear()
            st.rerun()

if __name__ == "__main__":
    main()