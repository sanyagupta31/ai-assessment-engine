

# 🤖 AI-Powered Dynamic Assessment Engine

[](https://www.python.org/)
[](https://streamlit.io/)
[](https://ai.google.dev/)

An AI-powered platform that dynamically generates **role-specific technical assessments** using the **Google Gemini API**. This tool helps recruiters streamline the technical screening process by creating relevant, on-the-fly assessments tailored to any job description.

### 🔴 [**Live Demo**](https://sanyagupta31-ai-assessment-engine-app-szggmd.streamlit.app/)

-----



## ✨ Key Features

  * **Dynamic Skill Extraction**: Intelligently parses any job description to identify the most critical technical skills.
  * **AI-Powered Question Generation**: Leverages the Gemini API to create a unique set of questions for each skill, including multiple-choice and coding snippets.
  * **Interactive Candidate Experience**: A clean, intuitive UI for candidates to take the assessment.
  * **Comprehensive Reporting**: Instantly generates a results dashboard with an overall score, proficiency ratings (**Strong** 🏆, **Medium** 👍, **Weak** 👎), and a skill-by-skill breakdown.
  * **Exportable Results**: Recruiters can download a detailed report as a **CSV file** for easy record-keeping and sharing.

-----

## 🛠️ Tech Stack

  * **Python**: Core programming language.
  * **Streamlit**: For creating the interactive web UI.
  * **Google Gemini API**: The LLM for skill extraction and question generation.
  * **Pandas**: For data manipulation and creating the final CSV report.

-----

## 🚀 Getting Started

Follow these steps to set up and run the project on your local machine.

### 1\. Clone the Repository

```bash
git clone https://github.com/sanyagupta31/ai-assessment-engine.git
cd ai-assessment-engine
```

### 2\. Create and Activate a Virtual Environment

It's recommended to use a virtual environment to manage dependencies.

  * **On macOS/Linux:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
  * **On Windows:**
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

### 3\. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4\. Set Up Your API Key

1.  Obtain your **Google Gemini API key** from [Google AI Studio](https://aistudio.google.com/).

2.  Create a file named `secrets.toml` inside a `.streamlit` folder at the root of your project: `/.streamlit/secrets.toml`.

3.  Add your API key to the `secrets.toml` file as shown below:

    ```toml
    GOOGLE_API_KEY = "your_api_key_here"
    ```

-----

## ▶️ Run the Application

Once the setup is complete, run the following command in your terminal:

```bash
streamlit run app.py
```

Your app will now be running on [http://localhost:8501](https://www.google.com/search?q=http://localhost:8501).

-----

## 🤝 Contributing

Contributions are welcome\! If you have suggestions for improvements or find a bug, please feel free to open an issue or submit a pull request.

-----

## 📝 License

This project is licensed under the MIT License.

-----

## 👩‍💻 Connect with Me

**Sanya Gupta**
My Linkedin : https://www.linkedin.com/in/sanya-gupta-2466052a6/
  