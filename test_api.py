import httpx
import os
from dotenv import load_dotenv

load_dotenv()

r = httpx.post(
    "https://api.anthropic.com/v1/messages",
    headers={
        "x-api-key": os.getenv("ANTHROPIC_API_KEY", ""),
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    },
    json={
        "model": "claude-sonnet-4-5",
        "max_tokens": 100,
        "messages": [{"role": "user", "content": "hi"}]
    }
)
print(r.status_code)
print(r.text)