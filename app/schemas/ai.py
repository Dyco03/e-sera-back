from pydantic import BaseModel, Field


class SummarizeRequest(BaseModel):
    text: str = Field(min_length=1)


class SummarizeResponse(BaseModel):
    summary: str


class SuggestRepliesRequest(BaseModel):
    message: str = Field(min_length=1)


class SuggestRepliesResponse(BaseModel):
    replies: list[str] = Field(min_length=3, max_length=3)
