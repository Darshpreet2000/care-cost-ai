# MediCompare AI Agents Backend

This project implements a backend service for MediCompare, an AI-powered platform designed to provide comprehensive analysis of medical procedure costs and hospital quality. It leverages Google's Agent Development Kit (ADK) to orchestrate a series of specialized AI agents that process user queries, retrieve data, and generate insightful reports to assist patients, clinicians, and care coordinators in making informed healthcare decisions.

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Agents Workflow](#agents-workflow)
- [Setup and Installation](#setup-and-installation)
- [API Endpoints](#api-endpoints)
- [Project Structure](#project-structure)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)

## Features

*   **Intelligent Patient Intake:** Gathers essential medical procedure and location details from users, handling clarifications as needed.
*   **Medical Coding:** Automatically maps medical procedures to standard DRG (Diagnosis Related Group) and CPT (Current Procedural Terminology) codes.
*   **Data Retrieval:** Accesses and retrieves relevant healthcare cost data (CMS) and hospital quality metrics from Google Cloud BigQuery.
*   **Hospital Recommendations:** Suggests top hospitals and treatments based on quality data.
*   **Comprehensive Reporting:** Generates detailed, structured markdown reports synthesizing all collected data and insights.
*   **Scalable Agent Orchestration:** Utilizes Google ADK for efficient management and execution of AI agents.
*   **FastAPI Backend:** Provides a robust and asynchronous API for seamless interaction.

## Architecture

The MediCompare backend is built using FastAPI and orchestrated with Google's Agent Development Kit (ADK). The core of the system is a `SequentialAgent` workflow that processes user requests through a pipeline of specialized AI agents. Data is primarily sourced from Google Cloud BigQuery.

## Agents Workflow

The system employs a sequential workflow, where each agent performs a specific task and passes its output to the next agent in the pipeline:

1.  **Intake Agent (Nurse Clara):**
    *   **Role:** Patient Intake Specialist.
    *   **Functionality:** Greets the user, extracts mandatory attributes (medical procedure, location) and optional insurance context. It handles clarification loops if information is missing or ambiguous.
    *   **Output:** `IntakeRecommendation` (JSON) indicating `handoff_to_dr_leo` (success) or `pending_clarification`.

2.  **Query Agent (Dr. Leo):**
    *   **Role:** Medical Coder.
    *   **Functionality:** Receives validated procedure and location information. It queries the `cms_healthcare_data` BigQuery table to retrieve valid DRG codes and then maps the procedure to the most appropriate DRG and CPT codes.
    *   **Output:** `QueryRecommendation` (JSON) containing the assigned DRG code, description, CPT codes, and justification.

3.  **Records Agent (Officer Priya):**
    *   **Role:** Data Officer.
    *   **Functionality:** Retrieves relevant CMS healthcare cost data and hospital quality data from BigQuery tables (`cms_healthcare_data` and `hospital_data`) based on the DRG and CPT codes.
    *   **Output:** `RecordsRecommendation` (JSON) containing the retrieved data.

4.  **Care Agent (Coordinator Maya):**
    *   **Role:** Care Planner.
    *   **Functionality:** Recommends top hospitals and treatments by fetching and analyzing quality data from the `hospital_data` BigQuery table.
    *   **Output:** `CareRecommendation` (JSON) with hospital and treatment recommendations.

5.  **Insight Agent (Dr. Elena):**
    *   **Role:** Health Economist.
    *   **Functionality:** Generates a comprehensive, long-form, and polished markdown report. It synthesizes all data and insights produced by the preceding agents (patient context, medical coding, cost data, hospital quality, recommendations) into a detailed analysis.
    *   **Output:** `InsightRecommendation` (JSON) containing the full markdown report.

## Setup and Installation

### Prerequisites

*   Python 3.9+
*   Google Cloud Project with BigQuery API enabled
*   Service Account Key for BigQuery access (JSON file)
*   `gcloud` CLI configured with Application Default Credentials (ADC) or a service account key file path provided in the `query_agent.py` and `records_agent.py` files.

### Steps

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Darshpreet2000/care-cost-ai.git
    cd care-cost-ai/mediacompare-backend
    ```

2.  **Create a virtual environment and install dependencies:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

3.  **Configure Google Cloud Credentials:**
    Ensure your Google Cloud credentials are set up. The agents use Application Default Credentials (ADC) by default. You can set this up by running:
    ```bash
    gcloud auth application-default login
    ```
    Alternatively, if you are using a service account key file, ensure the path in `agents/query_agent/agent.py` and `agents/records_agent/agent.py` is correct:
    ```python
    # Example in agents/query_agent/agent.py
    creds = service_account.Credentials.from_service_account_file(
        "/Users/darshpreetsingh/Downloads/spry-sensor-475217-k0-9f362b1b29d6.json", # Update this path
        scopes=["https://www.googleapis.com/auth/bigquery"]
    )
    ```

4.  **Set up Environment Variables:**
    Create a `.env` file in the root directory and add any necessary environment variables (e.g., for API keys if the ADK model requires them, though not explicitly shown in the provided code).

5.  **Run the FastAPI application:**
    ```bash
    uvicorn main:app --host 0.0.0.0 --port 8080 --reload
    ```
    The API will be accessible at `http://localhost:8080`.

## API Endpoints

*   **GET /**
    *   **Description:** Root endpoint, returns a simple message indicating the backend is running.
    *   **Response:** `{"message": "MediCompare backend is running"}`

*   **GET /chat**
    *   **Description:** Main chat endpoint for interacting with the AI agent workflow.
    *   **Query Parameters:**
        *   `query` (str, required): The user's input message.
        *   `user_id` (str, optional): Unique identifier for the user. If not provided, a new UUID will be generated.
        *   `session_id` (str, optional): Unique identifier for the session. If not provided, a new UUID will be generated.
    *   **Response:** Server-Sent Events (SSE) stream of agent events (messages, tool calls, tool results, pauses).

## Project Structure

```
.
├── .env                      # Environment variables
├── .gitignore                # Git ignore file
├── Dockerfile                # Dockerfile for containerization
├── execution_workflow.py     # Defines the sequential agent workflow
├── main.py                   # FastAPI application entry point and API endpoints
├── requirements.txt          # Python dependencies
├── temp.py                   # Temporary file (can be removed)
└── agents/                   # Directory containing all AI agents
    ├── __init__.py           # Python package initializer
    ├── care_agent/
    │   ├── agent.py          # Coordinator Maya (Care Planner) agent logic
    │   └── models.py         # Pydantic models for Care Agent
    ├── insight_agent/
    │   ├── agent.py          # Dr. Elena (Health Economist) agent logic
    │   └── models.py         # Pydantic models for Insight Agent
    ├── intake_agent/
    │   ├── agent.py          # Nurse Clara (Patient Intake Specialist) agent logic
    │   └── models.py         # Pydantic models for Intake Agent
    ├── query_agent/
    │   ├── agent.py          # Dr. Leo (Medical Coder) agent logic
    │   └── models.py         # Pydantic models for Query Agent
    └── records_agent/
        ├── agent.py          # Officer Priya (Data Officer) agent logic
        └── models.py         # Pydantic models for Records Agent
```

## Dependencies

The project relies on the following Python packages, as specified in `requirements.txt`:

*   `fastapi`: For building the web API.
*   `uvicorn`: ASGI server for running FastAPI.
*   `google-cloud-bigquery`: Google Cloud BigQuery client library.
*   `google-cloud-aiplatform`: Google Cloud AI Platform client library (likely for Gemini model access).
*   `google-adk`: Google Agent Development Kit for agent orchestration.
*   `python-dotenv`: For loading environment variables from a `.env` file.

## Contributing

Contributions are welcome! Please follow standard GitHub flow: fork the repository, create a feature branch, commit your changes, and open a pull request.

## License

[Specify your project's license here, e.g., MIT, Apache 2.0, etc.]
