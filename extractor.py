import os
import json
from google import genai
from dotenv import load_dotenv
from logic.schema import ExtractionResult

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = "models/gemini-flash-latest"

EXTRACTION_PROMPT = """You are analyzing a meeting transcript to extract action items.

For each action item found, identify:
- task: what needs to be done (concise, imperative form)
- owner: who is responsible (use the speaker name if they assign it to themselves, or the named person if assigned to someone else; null if genuinely unclear)
- deadline: convert relative dates ("by Friday", "next week") to YYYY-MM-DD using the meeting date provided; null if no deadline mentioned
- confidence: 0-1, how confident you are this is a real actionable commitment (not a vague suggestion)
- raw_quote: the exact sentence it came from

Only extract clear commitments or assigned tasks. Skip vague statements like "we should think about X" unless someone explicitly commits to doing it.

Meeting date: {meeting_date}

Transcript:
{transcript}

Respond ONLY with valid JSON matching this structure, no other text, no markdown fences:
{{"action_items": [{{"task": "...", "owner": "...", "deadline": "...", "confidence": 0.9, "raw_quote": "..."}}]}}
"""


def call_gemini(transcript: str, meeting_date: str) -> str:
    prompt = EXTRACTION_PROMPT.format(meeting_date=meeting_date, transcript=transcript)
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )
    return response.text


def parse_extraction(raw_text: str) -> ExtractionResult:
    cleaned = raw_text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("```")[1]
        if cleaned.startswith("json"):
            cleaned = cleaned[4:]
    try:
        data = json.loads(cleaned)
        return ExtractionResult(**data)
    except Exception as e:
        raise ValueError(f"Failed to parse extraction result: {e}\nRaw output: {raw_text}")


def extract_action_items(transcript: str, meeting_date: str) -> ExtractionResult:
    raw_text = call_gemini(transcript, meeting_date)
    return parse_extraction(raw_text)


if __name__ == "__main__":
    with open("checks/sample_transcripts/test1.txt") as f:
        transcript = f.read()
    result = extract_action_items(transcript, "2026-09-27")
    print(result.model_dump_json(indent=2))