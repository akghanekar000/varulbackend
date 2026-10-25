
import os

from fastapi import APIRouter, HTTPException
from openai import OpenAI, APIError
from pydantic import BaseModel, Field

router = APIRouter(prefix="/ai", tags=["AI"])


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)


class ChatResponse(BaseModel):
    reply: str


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    if not os.getenv("OPENAI_API_KEY"):
        raise HTTPException(
            status_code=500,
            detail="OpenAI API key is not configured.",
        )

    try:
        client = OpenAI()

        response = client.responses.create(
                model="gpt-4.1-mini",
                input=request.message,
        )

        return ChatResponse(reply=response.output_text)

    except APIError:
        raise HTTPException(
            status_code=502,
            detail="The OpenAI API request failed. Check your API access and billing.",
        )
                    