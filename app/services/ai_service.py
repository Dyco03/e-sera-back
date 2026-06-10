import asyncio
import json
import re

from fastapi import HTTPException, status
from google import genai

from app.core.config import settings


class AiService:
    def __init__(self) -> None:
        self._client = None

    async def summarize(self, text: str) -> str:
        if not settings.gemini_api_key:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Gemini API key is not configured",
            )

        try:
            summary = await asyncio.wait_for(
                asyncio.to_thread(self._summarize_sync, text.strip()),
                timeout=settings.summarize_timeout_seconds,
            )
        except TimeoutError:
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail="Summarization timeout",
            )
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Summarization failed: {exc}",
            )

        return summary

    async def suggest_replies(self, message: str) -> list[str]:
        if not settings.gemini_api_key:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Gemini API key is not configured",
            )

        try:
            replies = await asyncio.wait_for(
                asyncio.to_thread(self._suggest_replies_sync, message.strip()),
                timeout=settings.summarize_timeout_seconds,
            )
        except TimeoutError:
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail="Suggested replies timeout",
            )
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Suggested replies failed: {exc}",
            )

        return replies

    def _summarize_sync(self, text: str) -> str:
        client = self._get_client()
        prompt = (
            "Resume ce texte de post social en 1 ou 2 phrases courtes. "
            "Garde la langue principale du texte. "
            "Retourne uniquement le resume, sans explication.\n\n"
            f"Texte: {text}"
        )
        response = client.models.generate_content(
            model=settings.ai_model,
            contents=prompt,
        )
        summary = (response.text or "").strip()
        if not summary:
            raise ValueError("Gemini returned an empty summary")
        return summary

    def _suggest_replies_sync(self, message: str) -> list[str]:
        client = self._get_client()
        prompt = (
            "Genere exactement 3 reponses courtes au message suivant. "
            "Ton naturel conversationnel. Pas d'explication. "
            "Retourne uniquement un tableau JSON de 3 chaines.\n\n"
            f"Message: {message}"
        )
        response = client.models.generate_content(
            model=settings.ai_model,
            contents=prompt,
        )
        replies = self._parse_replies(response.text or "")
        if len(replies) != 3:
            raise ValueError("Gemini did not return exactly 3 replies")
        return replies

    def _parse_replies(self, raw_text: str) -> list[str]:
        text = raw_text.strip()
        if not text:
            return []

        cleaned = re.sub(r"^```(?:json)?|```$", "", text, flags=re.IGNORECASE).strip()
        try:
            decoded = json.loads(cleaned)
            if isinstance(decoded, list):
                return self._normalize_replies(decoded)
            if isinstance(decoded, dict) and isinstance(decoded.get("replies"), list):
                return self._normalize_replies(decoded["replies"])
        except json.JSONDecodeError:
            pass

        lines = [
            re.sub(r"^\s*(?:[-*]|\d+[.)])\s*", "", line).strip()
            for line in cleaned.splitlines()
        ]
        return self._normalize_replies(lines)

    def _normalize_replies(self, values: list[object]) -> list[str]:
        replies: list[str] = []
        for value in values:
            reply = str(value).strip().strip('"')
            if reply and reply not in replies:
                replies.append(reply[:80])
            if len(replies) == 3:
                break
        return replies

    def _get_client(self):
        if self._client is None:
            self._client = genai.Client(api_key=settings.gemini_api_key)
        return self._client


ai_service = AiService()
