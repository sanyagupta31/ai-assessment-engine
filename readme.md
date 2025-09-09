

# 🤖 AI-Powered Dynamic Assessment Engine

An AI-powered platform that generates **role-specific technical assessments** dynamically using **Gemini API**.
It analyzes a job description, extracts relevant skills, generates multiple-choice questions, and produces a detailed **candidate performance report**.

---

## ✨ Features

* 📌 **Job Description Analysis** – Extracts top technical skills from a given role description.
* 🤖 **Dynamic Question Generation** – AI creates MCQs for each skill.
* 📝 **Candidate Assessment** – Personalized test for each candidate.
* 📊 **Detailed Report** – Overall score, skill-wise performance, and recruiter-friendly CSV export.
* 🎯 **Adaptive Evaluation** – Rates candidates as **Strong 🏆**, **Medium 👍**, or **Weak 👎**.

---

## 🚀 Demo Flow

1. Recruiter inputs **Candidate Name + Role Title + Job Description**.
2. AI extracts top skills from the job description.
3. MCQs are generated dynamically for each skill.
4. Candidate answers questions in an interactive UI.
5. Recruiter receives a detailed **skill-wise performance report**.

---



## 🛠️ Tech Stack

* [Python 3.10+](https://www.python.org/)
* [Streamlit](https://streamlit.io/) – UI framework
* [Google Gemini API](https://ai.google.dev/) – AI model for skill & question generation
* [Pandas](https://pandas.pydata.org/) – Data processing & reporting

---

## ⚙️ Installation

Clone the repo:

```bash
git clone https://github.com/sanyagupta31/ai-assessment-engine.git
cd ai-assessment-engine
```

Create virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate   # On Mac/Linux
venv\Scripts\activate      # On Windows
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🔑 Setup API Key

1. Get your **Google Gemini API key** from [AI Studio](https://aistudio.google.com/).
2. In your Streamlit project folder, create a file: `.streamlit/secrets.toml`
3. Add the following:

```toml
GOOGLE_API_KEY="your_api_key_here"
```

---

## ▶️ Run the App

```bash
streamlit run app.py
```

Open the link in your browser:
👉 [http://localhost:8501](http://localhost:8501)


check out my app : https://sanyagupta31-ai-assessment-engine-app-szggmd.streamlit.app/

---

## 📊 Output

* Interactive **assessment page** for candidates.
* Auto-generated **results dashboard** with charts & tables.
* Downloadable **CSV report** for recruiters.

---

## 👩‍💻 Author

**Sanya Gupta**

