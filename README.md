# e-sera FastAPI Backend

Backend REST

## Launch

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

DataBase : SQLite 

#Useful Environment Variables
DATABASE_URL, default: sqlite:///./esera.db
SECRET_KEY,
ACCESS_TOKEN_EXPIRE_MINUTES, default: 10080
GEMINI_API_KEY, API key used by Google GenAI for post translation
TRANSLATION_MODEL, default: gemini-2.5-flash
TRANSLATION_TIMEOUT_SECONDS, default: 30.0
AI_MODEL, default: gemini-2.5-flash, used for content summarization
SUMMARIZE_TIMEOUT_SECONDS, default: 30.0
MODEL and TIMEOUT_SECONDS are still supported as shared aliases for both translation and
