# Security & Compliance Checklist (RC-v1)

This checklist confirms the security measures implemented in the application.

## Threat Model
* **Threat:** Exposure of the Google API key.
* **Mitigation:** The key is stored securely in `.streamlit/secrets.toml` and is not hardcoded in the source code.

## Data Security
* **Data in Transit:** All API calls to the Google Gemini service are encrypted using HTTPS.
* **Data at Rest:** No sensitive PII (Personally Identifiable Information) is stored in a database.

## Access Control
* The application's access is public, but API key management is restricted to authorized personnel.

## Vulnerability Scans
* **Action:** A security audit of Python dependencies will be performed using a tool like `pip-audit` or `Snyk` before deployment. Any critical issues will be fixed.