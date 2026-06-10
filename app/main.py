from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.routes import ai, auth, messages, posts, profiles, search, storage, translations
from app.core.config import settings
from app.core.database import Base, engine

Base.metadata.create_all(bind=engine)
settings.upload_dir.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="e-sera API", version="1.0.0")

allowed_origins = [
    "http://localhost",
    "http://127.0.0.1",
    "http://10.0.2.2",

    "http://esera.works",
    "https://esera.works",
    "http://api.esera.works",
    "https://api.esera.works",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_origin_regex=r"^http://(localhost|127\.0\.0\.1|10\.0\.2\.2)(:\d+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory=settings.upload_dir), name="uploads")

app.include_router(auth.router)
app.include_router(ai.router)
app.include_router(messages.router)
app.include_router(posts.router)
app.include_router(profiles.router)
app.include_router(search.router)
app.include_router(storage.router)
app.include_router(translations.router)


@app.get("/")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
