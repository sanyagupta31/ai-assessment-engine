# Deployment Guide: AI-Powered Dynamic Assessment Engine (RC-v1)

This guide provides instructions for building and deploying the application to staging and production environments.

## Environments
* **Operating System:** Linux (Ubuntu 22.04 LTS recommended)
* **Runtime:** Python 3.11+
* **Dependencies:** All dependencies are listed in `requirements.txt`.

## Configuration
* **API Key:** The Google API key must be securely stored in the `.streamlit/secrets.toml` file.
    ```ini
    # .streamlit/secrets.toml
    GOOGLE_API_KEY = "your-secret-api-key-here"
    ```

## Build & Deployment Steps
1.  **Clone the repository:** `git clone [your-repo-link]`
2.  **Navigate to the project directory:** `cd ai-assessment-engine`
3.  **Install dependencies:** `pip install -r requirements.txt`
4.  **Run the application:** `streamlit run app.py`

## Health Check
- The application's health can be confirmed by navigating to the root URL (e.g., `http://localhost:8501`). A successful load of the main page indicates that the application is running correctly.

## Rollback Procedure
- In case of a failed deployment, revert to the last working commit using `git checkout [last-known-good-commit-SHA]` and restart the application.