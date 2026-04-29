# SprintIQ (Spatial Feynman) - Intelligent Agile Estimation System

## Executive Summary

SprintIQ is an advanced, machine learning-driven estimation system optimized for Agile software development. It leverages Natural Language Processing (NLP) to analyze user stories and predict their implementation complexity in standard Story Points (Fibonacci sequence). 

Designed to reduce the subjectivity and time overhead of traditional estimation ceremonies like Planning Poker, SprintIQ provides engineering teams with consistent, data-backed baselines for their sprint planning. The system bridges the gap between human intuition and empirical data, ensuring more predictable delivery cycles.

## Core Features

### AI-Driven Estimation
The core of SprintIQ is a regression model trained on a massive dataset of real-world software requirements. It analyzes the semantic structure of a user story—identifying technical keywords, scope indicators, and complexity signals—to output an objective complexity score.

### Fibonacci Scale Integration
Predictions are automatically mapped to the standard Agile Fibonacci scale (1, 2, 3, 5, 8, 13), ensuring seamless integration with existing project management tools and methodologies (Scrum/Kanban).

### Confidence Metrics
Beyond simple numbers, the system provides a confidence assessment (High/Medium/Low) for each estimate. This enables teams to quickly accept high-confidence estimates and focus their discussion time on low-confidence items that may carry hidden risks or ambiguity.

### Continuous Learning Loop
The system includes a feedback mechanism where meaningful deviations between predicted and actual effort can be captured. This data allows the model to be retrained, enabling it to adapt to a specific team's velocity and estimation style over time.

## Technical Architecture

### Backend: FastAPI
The application core is built on **FastAPI**, chosen for its high-performance asynchronous capabilities and automatic validation. It serves as the inference engine, handling prediction requests with minimal latency.

### Frontend: Jinja2 & TailwindCSS
The user interface is server-side rendered using **Jinja2** templates and styled with **TailwindCSS**. This approach delivers a lightweight, responsive, and professional "Dark Mode" experience without the overhead of a heavy client-side framework.

### Machine Learning: Scikit-Learn
The estimation engine utilizes **Scikit-Learn**.
*   **Vectorization**: TF-IDF (Term Frequency-Inverse Document Frequency) transforms raw text into weighted numerical vectors, emphasizing technical terms over common stopwords.
*   **Model**: A **Random Forest Regressor** is employed for its robustness in handling non-linear relationships and its resistance to overfitting on high-dimensional text data.

### Data Storage
*   **Training Data**: The model is trained on a curated dataset of over **40,000 real-world user stories** mined from diverse open-source projects.
*   **History & Feedback**: Operational history and user feedback are stored in structured CSV files, ensuring data portability and simplicity.

## Project Structure

```text
spatial-feynman/
├── app/                      # FastAPI Backend & Frontend Logic
│   ├── core/                 # App configurations & Storage logic
│   ├── models/               # Pydantic models
│   ├── routes/               # API endpoints
│   ├── services/             # Business logic (inference service)
│   ├── static/               # CSS, JS, Images
│   ├── templates/            # Jinja2 templates
│   └── utils/                # Helper functions
├── data/
│   ├── raw/                  # Original CSV sources
│   ├── processed/            # Merged dataset and SQLite DB
│   └── tracker/              # Feedback and history logs
├── docs/                     # Documentation & Evaluation reports
├── ml_artifacts/             # Saved Model & Vectorizer
├── scripts/                  # Utility & ML scripts
│   ├── training/             # train_model.py
│   ├── evaluation/           # evaluate_model.py
│   └── utils/                # DB/CSV utility tools
├── logs/                     # System & error logs
└── temp/                     # Temporary files & scratch outputs
```

## Installation and Setup

### Prerequisites
*   Python 3.9 or higher
*   pip (Python Package Installer)

### 1. Environment Setup
Clone the repository and install the necessary dependencies:

```bash
pip install -r requirements.txt
```

### 2. Model Training
Before the application can be used, the machine learning model must be trained on the dataset. This process generates the model artifacts (`model.joblib`) required for inference.

```bash
python scripts/training/train_model.py
```

*Note: This script uses the `data/processed/merged_real_data.csv` dataset containing ~40,000 records.*

### 3. Usage
Start the application server:

```bash
uvicorn app.main:app --reload
```

Access the interface at: `http://127.0.0.1:8000`

## API Documentation

The system exposes a RESTful API for integration with external tools (Jira, Trello, custom pipelines).

### Predict Endpoint
**POST** `/predict`

Returns a complexity estimate for a single user story.

**Request Body:**
```json
{
  "user_story": "As a developer, I want to migrate the user database to PostgreSQL to improve query performance."
}
```

**Response:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "predicted_story_points": 8,
  "confidence": "high",
  "model_used": "RandomForestRegressor",
  "created_at": "2026-02-06T12:00:00"
}
```

## Credits

**Founder & Lead Developer**: Alla Rishi Venkatesh
*   **Role**: Architect & AI Developer
*   **Institution**: B.Tech Student

**Copyright © 2026 Alla Rishi Venkatesh. All Rights Reserved.**
This software and its underlying algorithms are the proprietary intellectual property of Alla Rishi Venkatesh. Unauthorized commercial use is prohibited.
