from openai import OpenAI
from app.config import OPENAI_API_KEY
from app.services.retriever import retrieve_relevant_chunks

# Create standard OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)


import json
import re
from openai import OpenAI
from app.config import OPENAI_API_KEY
from app.services.retriever import retrieve_relevant_chunks

# Create OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)


def fix_single_quotes_to_double(json_str: str) -> str:
    # Only applies if keys and values are enclosed in single quotes
    json_str = json_str.strip()

    # Replace single quotes around property names and values with double quotes
    json_str = re.sub(r"(?<=\{|,)\s*'([^']+)'\s*:", r'"\1":', json_str)  # Keys
    json_str = re.sub(r":\s*'([^']+)'\s*(?=,|\})", r': "\1"', json_str)  # String values

    return json_str


async def get_chat_completion(user_query: str) -> dict:
    try:
        context_chunks = retrieve_relevant_chunks(user_query)
        context = "\n---\n".join(context_chunks)

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an intelligent AI assistant named XtnsionAI, working at a dental clinic. "
                        "Always return a valid JSON object with exactly two fields:\n"
                        '{ "markdown_response": "...", "voice_transcript": "..." }\n'
                        "Do not add extra text before or after JSON. Use double quotes for all keys and values."
                    ),
                },
                {
                    "role": "user",
                    "content": f"Context:\n{context}\n\nQuestion:\n{user_query}",
                },
            ],
            temperature=0.7,
            max_tokens=700,
        )

        message_content = response.choices[0].message.content.strip()
        print("🔍 Raw OpenAI Response:\n", repr(message_content))

        try:
            return json.loads(message_content)  # First try raw
        except json.JSONDecodeError:
            # Try fixing bad quotes and parse again
            fixed_json = fix_single_quotes_to_double(message_content)
            return json.loads(fixed_json)

    except json.JSONDecodeError as e:
        print("❌ JSON Decode Error:", e)
        return {"error": "Invalid JSON format in LLM response after attempted fix."}

    except Exception as e:
        print("❌ Unexpected error in get_chat_completion:", e)
        return {"error": str(e)}


async def identify_intent(user_query: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an AI classifier named XtnsionAI, for a dental clinic assistant.\n"
                        "Classify the user's query into one of the following intents:\n"
                        "- `document_agent`: The query is about treatment info, doctor details, insurance, procedures, symptoms, services, etc.\n"
                        "- `appointment_agent`: The query is about booking, rescheduling, canceling, or checking appointments. This intent will only be used when the user explicitly mentions booking or scheduling an appointment.\n\n"
                        "Respond with **only** one of the two labels: `document_agent` or `appointment_agent`. No explanation.\n\n"
                        "Examples:\n"
                        "- 'What treatments do you offer?' → document_agent\n"
                        "- 'Tell me about Dr. Smith' → document_agent\n"
                        "- 'I need to book an appointment for cleaning next Monday' → appointment_agent\n"
                        "- 'Can I schedule my checkup for next week?' → appointment_agent\n"
                        "- 'Is my appointment for Friday confirmed?' → appointment_agent\n"
                        "- 'What is root canal treatment?' → document_agent\n"
                    ),
                },
                {
                    "role": "user",
                    "content": user_query,
                },
            ],
            temperature=0,
            max_tokens=10,
        )

        intent = response.choices[0].message.content.strip()
        if intent not in ["document_agent", "appointment_agent"]:
            raise ValueError(f"Unexpected intent: {intent}")
        return intent

    except Exception as e:
        return "document_agent"  # default fallback
