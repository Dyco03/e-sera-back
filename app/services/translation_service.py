import asyncio

from fastapi import HTTPException, status
from google import genai

from app.core.config import settings


class TranslationService:
    _languages = {
        "mg": "Malagasy",
        "malagasy": "Malagasy",
        "fr": "Francais",
        "français": "Francais",
        "french": "Francais",
        "en": "Anglais",
        "anglais": "Anglais",
        "english": "Anglais",
    }

    def __init__(self) -> None:
        self._client = None

    async def translate_post(self, text: str, target_language: str) -> dict[str, str]:
        language = self._normalize_language(target_language)
        if not settings.gemini_api_key:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Gemini API key is not configured",
            )

        try:
            translated_text = await asyncio.wait_for(
                asyncio.to_thread(self._translate_sync, text.strip(), language),
                timeout=settings.translation_timeout_seconds,
            )
        except TimeoutError:
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail="Translation timeout",
            )
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Translation failed: {exc}",
            )

        return {
            "translatedText": translated_text,
            "targetLanguage": language,
        }

    def _translate_sync(self, text: str, language: str) -> str:
        client = self._get_client()
        prompt = (
            f"Translate the following text into {language}. "
            "Return only the translation, without quotes or any explanation.\n\n"
            f"Text: {text}"
        )
        response = client.models.generate_content(
            model=settings.translation_model,
            contents=prompt,
        )
        translated_text = (response.text or "").strip()
        if not translated_text:
            raise ValueError("Gemini returned an empty translation")
        return translated_text

    def _normalize_language(self, language: str) -> str:
        key = language.strip().lower()
        if key not in self._languages:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Unsupported target language",
            )
        return self._languages[key]

    def _get_client(self):
        if self._client is None:
            self._client = genai.Client(api_key=settings.gemini_api_key)
        return self._client


translation_service = TranslationService()
