# ReliefLink AI 🆘

ReliefLink AI is an emergency and disaster support assistant that intelligently organizes and prioritizes emergency requests using AI.

## Features
- **Emergency Intake**: Users can submit requests with location and description.
- **AI Workflow Engine**:
  - **Classification**: Detects category and urgency (LOW to CRITICAL).
  - **Summarization**: Generates volunteer-friendly summaries.
  - **Translation**: Translates summaries into Hindi.
  - **Recommendation**: Suggests nearby NGOs from a local dataset.
- **Real-time Dashboard**: Displays request stats, category distribution, and recent activity.

## Tech Stack
- **Backend**: FastAPI, SQLAlchemy (SQLite)
- **Frontend**: Streamlit
- **AI**: Google Gemini API
- **Data**: JSON-based NGO dataset

## Setup Instructions

### 1. Prerequisites
- Python 3.9+
- Google Gemini API Key

### 2. Environment Setup
Clone the repository and install dependencies:
```bash
pip install -r requirements.txt
```

Create a `.env` file from the example:
```bash
cp .env.example .env
```
Add your `GEMINI_API_KEY` to the `.env` file.

### 3. Run the Application

Start the Backend (FastAPI):
```bash
python -m app.main
```

Start the Frontend (Streamlit) in a new terminal:
```bash
streamlit run streamlit_app/app.py
```

## Project Structure
```
relieflink-ai/
├── app/
│   ├── main.py          # FastAPI Entry
│   ├── ai/              # AI Workflow logic
│   ├── database/        # SQLite/SQLAlchemy setup
│   ├── models/          # Pydantic/SQLAlchemy models
│   ├── prompts/         # AI Prompts
│   └── services/        # NGO lookup service
├── streamlit_app/       # Streamlit UI
├── data/                # NGO dataset
└── requirements.txt
```

## License
MIT
