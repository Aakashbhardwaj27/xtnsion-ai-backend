from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from app.services.azure_openai import get_chat_completion, identify_intent

router = APIRouter()


class ChatRequest(BaseModel):
    query: str
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    markdown_response: str
    voice_transcript: str
    source_documents: Optional[List[str]] = None


# Mock appointment agent logic
def mock_appointment_agent_response(query: str) -> dict:
    return {
        "markdown_response": (
            "### 📅 Appointment Booked Successfully\n\n"
            f"Your appointment request for: **{query}** has been received.\n\n"
            "- 📍 *Location:* Downtown Dental Clinic\n"
            "- 🕒 *Time:* We will contact you to confirm an available slot.\n\n"
            "Thank you for choosing us! 🦷"
        ),
        "voice_transcript": f"I've noted your appointment request. We will contact you soon to confirm the time.",
    }


@router.post("/query", response_model=ChatResponse)
async def chat_query(request: ChatRequest):
    if not request.query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    intent = await identify_intent(request.query)
    print(f"Intent identified: {intent}")

    if intent == "document_agent":
        result = await get_chat_completion(request.query)
    elif intent == "appointment_agent":
        result = mock_appointment_agent_response(request.query)
    else:
        result = await get_chat_completion(request.query)

    print(result)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])

    return ChatResponse(
        markdown_response=result["markdown_response"],
        voice_transcript=result["voice_transcript"],
    )
