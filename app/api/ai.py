
import os

from fastapi import APIRouter, HTTPException
from huggingface_hub import InferenceClient
from huggingface_hub.errors import HfHubHTTPError
from pydantic import BaseModel, Field

router = APIRouter(prefix="/ai", tags=["AI"])

MODEL = "openai/gpt-oss-20b"


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)


class ChatResponse(BaseModel):
        reply: str


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
        token = os.getenv("HF_TOKEN")

        if not token:
                raise HTTPException(
                        status_code=500,
                        detail="HF_TOKEN is not configured.",
                )

        try:
                client = InferenceClient(
                        provider="auto",
                        api_key=token,
                )

                result = client.chat.completions.create(
                        model=MODEL,
                        messages=[
                                {
                                        "role": "user",
                                        "content": request.message,
                                }
                        ],
                        max_tokens=300,
                )

                reply = result.choices[0].message.content

                if not reply:
                        raise HTTPException(
                                status_code=502,
                                detail="The model returned an empty response.",
                        )

                return ChatResponse(reply=reply)

        except HfHubHTTPError as exc:
                raise HTTPException(
                        status_code=502,
                        detail=(
                                "Hugging Face request failed. Check model availability, "
                                "token permissions, and free-tier limits."
                        ),
                ) from exc
                                                                    