from pydantic import BaseModel, Field


class PostTranslationRequest(BaseModel):
    text: str = Field(min_length=1)
    targetLanguage: str


class PostTranslationResponse(BaseModel):
    translatedText: str
    targetLanguage: str
