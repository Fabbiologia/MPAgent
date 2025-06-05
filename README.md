Marine Protected Area Management Plan AI Analysis

Project Overview

This project utilizes artificial intelligence to analyze Management Plans of Marine Protected Areas (MPAs) in Spanish. The AI extracts specific details from the uploaded text, evaluates regulatory quality, conservation objectives, and the relevance of cited literature to those objectives.

Objectives

The AI-driven tool will:
	•	Extract and summarize zonation and associated regulations.
	•	Identify and clearly state conservation objectives.
	•	Collect and organize cited literature.
	•	Assess protection quality using the MPA Guide framework.
	•	Evaluate conservation objectives using SMART (Specific, Measurable, Achievable, Relevant, Time-bound) criteria and feasibility.
	•	Analyze congruence between conservation objectives and themes of cited literature.

Architecture Overview

The project employs a modular, prompt-driven pipeline leveraging OpenAI’s GPT API, supported by fully open-source frameworks for document processing and management.

Tech Stack
	•	AI Model: OpenAI GPT API (supports Spanish)
	•	Document Processing: LangChain, Ollama, and PyMuPDF
	•	Data Management: SQLite or PostgreSQL (optional)
	•	Web Interface: Streamlit (interactive UI)

Workflow Diagram

User uploads MPA Management Plan PDF
│
▼
PDF processed using PyMuPDF
│
▼
Text Extraction and Preprocessing (Spanish)
│
▼
GPT-based Extraction:
- Zonation & Regulations
- Conservation Objectives
- Literature Cited
│
▼
Analytical Assessments:
- MPA Guide Framework Evaluation
- SMART Criteria & Feasibility Check
- Literature-Objective Congruence Analysis
│
▼
Results Displayed in Streamlit UI

Prompt-driven Workflow

The workflow is structured step-by-step for clarity and ease of implementation. Each step will be defined clearly with instructions for AI-assisted coding.

TODO Checklist

Document Processing
	•	Set up PDF upload and processing using PyMuPDF.
	•	Extract text accurately, ensuring Spanish language compatibility.

AI Extraction Modules
	•	Design GPT prompts for zonation and regulation extraction.
	•	Design GPT prompts for conservation objective extraction.
	•	Design GPT prompts for literature citation extraction.

Analytical Modules
	•	Implement MPA Guide-based evaluation prompts.
	•	Develop SMART criteria evaluation and feasibility checks.
	•	Create thematic analysis between cited literature and conservation objectives.

Integration & UI
	•	Develop Streamlit UI for user-friendly document uploads and displaying AI-generated reports.
	•	Test integration thoroughly to ensure smooth user experience.

Deployment & Documentation
	•	Dockerize application for streamlined deployment.
	•	Write comprehensive documentation for future maintenance and usage.

Next Steps

Once the README and TODO list are approved, proceed to STEP 1 for implementing the initial setup and document processing workflow.