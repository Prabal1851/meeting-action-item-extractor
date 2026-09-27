# Meeting Action Item Extractor

Converts meeting transcripts into structured action items (task, owner, deadline, confidence) using the Gemini API.

## Setup
1. `pip install -r requirements.txt`
2. Add your Gemini API key to `.env` as `GEMINI_API_KEY=your_key`
3. `streamlit run app.py`

## How it works
- `extractor.py` — calls Gemini API to extract action items from transcript text
- `logic/schema.py` — Pydantic schema for structured output
- `logic/validators.py` — flags missing owners, invalid dates, duplicates
- `app.py` — Streamlit UI for upload and results display