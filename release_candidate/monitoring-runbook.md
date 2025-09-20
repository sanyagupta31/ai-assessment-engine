# Monitoring & Runbook (RC-v1)

This document provides guidance on monitoring the application's health and troubleshooting common issues.

## Health Checks & Metrics
- **Health Check:** The application is considered healthy if the main page loads successfully.
- **Metrics to Monitor:**
    - API Call Success Rate (ensure 99% of calls to Gemini are successful).
    - API Call Latency (monitor the time taken for AI to respond).
    - Application Uptime.

## Common Failure Scenarios
1.  **Scenario: "AI API calls are failing."**
    - **Symptoms:** The application shows a "Could not extract any skills" or "Failed to generate questions" error. The terminal logs show a 403 or 500 error from the Gemini API.
    - **Runbook Steps:**
        1.  Verify the `GOOGLE_API_KEY` in `.streamlit/secrets.toml` is correct.
        2.  Check the Google Cloud Console for the Gemini API status and billing issues.

2.  **Scenario: "Application is not starting."**
    - **Symptoms:** The `streamlit run` command fails with an error message in the terminal.
    - **Runbook Steps:**
        1.  Confirm all dependencies are installed (`pip install -r requirements.txt`).
        2.  Check the terminal log for specific error messages (e.g., syntax errors).