
import os
from groq import Groq
from dotenv import load_dotenv
from pathlib import Path

# Force load the .env file
env_path = Path('backend/.env')
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GROQ_API_KEY")
print(f"Loaded Key: {api_key[:10]}...")

try:
    client = Groq(api_key=api_key)
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Explain how an electric car works in 1 sentence.",
            }
        ],
        model="llama-3.3-70b-versatile",
    )
    print("SUCCESS!")
    print(chat_completion.choices[0].message.content)
except Exception as e:
    print(f"FAILED: {e}")
