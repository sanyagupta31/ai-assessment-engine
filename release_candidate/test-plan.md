# Test Plan: AI-Powered Dynamic Assessment Engine (RC-v1)

This document outlines the testing strategy for the AI-Powered Dynamic Assessment Engine, ensuring its readiness for production.

## Scope
The testing will cover the core functionality of the application, including:
- **AI Skill Extraction:** Verifying the model's ability to extract and deduplicate skills from a job description. This involves testing the `extract_skills()` and `clean_skills()` functions.
- **AI Question Generation:** Validating that the `generate_questions()` function correctly produces the specified number of MCQs and coding questions.
- **Assessment Flow:** A complete end-to-end test of the user journey from data input to report generation.
- **Scoring & Reporting:** Verifying that the application's scoring logic is accurate and that the CSV report exports the correct data.

## Exclusions
- **Odoo CRM Integration:** This functionality is a separate, planned deliverable and is not included in this test plan.
- **High-Volume Performance Testing:** Initial testing will focus on functionality rather than stress testing under heavy load.

## Environments
Testing will be conducted in the following environments:
- **Development (`dev`):** The local environment used for active development.
- **Staging (`staging`):** A pre-production environment that mirrors the production setup for final testing.

## Test Types
- **Unit Testing:** Automated tests for helper functions to ensure their isolated functionality.
- **Integration Testing:** Verification of the connection and data exchange with the Google Gemini API.
- **End-to-End (E2E) Testing:** A comprehensive test of the complete application flow.
- **UI Testing:** Manual and automated checks to ensure all Streamlit components render correctly and are interactive.

## Entry & Exit Criteria
- **Test Entry:** All code has been merged and is deployed to the staging environment.
- **Test Exit:** All critical E2E tests pass, and no high-priority bugs are open.