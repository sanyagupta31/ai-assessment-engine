# Odoo CRM Integration Plan (RC-v1)

This document outlines the proposed architecture and plan for integrating the AI Assessment Engine with Odoo CRM.

## Integration Architecture
The integration will be a **unidirectional, real-time sync** triggered by the user completing an assessment. A new backend service or API gateway will be developed to handle the secure data transfer between the Streamlit application and Odoo CRM.

## Integration Points
- **Trigger:** The sync will be initiated upon a successful assessment submission in the `show_results()` function.
- **Endpoint:** Data will be sent via an API call to a designated Odoo CRM endpoint, e.g., `POST /api/v1/assessments/`.

## Data Mapping
The following data will be mapped from our application to the Odoo CRM:
- Candidate Name (`st.session_state.candidate`) -> Contact (`name`)
- Role Title (`st.session_state.role`) -> Job Position (`job_id`)
- Overall Score (`overall_score`) -> Custom Field (`x_assessment_score`)
- Final Status (`final_status`) -> Custom Field (`x_hiring_status`)

## Sync Behavior
- The sync will be immediate upon assessment completion.
- Conflict Resolution: Given the one-way nature of the sync, conflicts are not anticipated.

## Authentication
- A secure API key will be used for authentication. This key will be stored as an environment variable, not in the source code.