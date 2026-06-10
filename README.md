# e-sera FastAPI Backend

Backend REST compatible avec les `ApiRepos` Flutter.

## Lancer

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Base de données par défaut : SQLite `backend/esera.db`.

## Variables utiles

- `DATABASE_URL`, par défaut `sqlite:///./esera.db`
- `SECRET_KEY`, à changer en production
- `ACCESS_TOKEN_EXPIRE_MINUTES`, par défaut `10080`
- `GEMINI_API_KEY`, clé utilisée par Google GenAI pour traduire les posts
- `TRANSLATION_MODEL`, par défaut `gemini-2.5-flash`
- `TRANSLATION_TIMEOUT_SECONDS`, par défaut `30.0`
- `AI_MODEL`, par défaut `gemini-2.5-flash`, utilisé pour les résumés
- `SUMMARIZE_TIMEOUT_SECONDS`, par défaut `30.0`
- `MODEL` et `TIMEOUT_SECONDS` restent acceptés comme alias communs pour traduction et résumé
