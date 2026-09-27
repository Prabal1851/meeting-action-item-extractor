# Meeting Action Item Extractor

Converts meeting transcripts into structured action items (task, owner, deadline, confidence) using the Gemini API.

## Setup

1. Clone this repo
2. Install dependencies:


pip install -r requirements.txt

3. Copy `.env.example` to `.env` and add your Gemini API key:

GEMINI_API_KEY=your_key_here

   Get a free key at https://aistudio.google.com/apikey
4. Run the app:

streamlit run app.py

5. Upload a `.txt` transcript, set the meeting date, click **Extract action items**

## How it works

- `extractor.py` — calls the Gemini API to extract action items from transcript text
- `logic/schema.py` — Pydantic schema defining the structured output (task, owner, deadline, confidence)
- `logic/validators.py` — flags missing owners, invalid dates, low confidence, and duplicate tasks
- `app.py` — Streamlit UI for upload and results display

## Sample data

Two example transcripts are included in `checks/sample_transcripts/` for testing.