import os
import json
import re
from groq import Groq
from dotenv import load_dotenv
from pathlib import Path

# Robustly find .env file
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

API_KEY = os.getenv("GROQ_API_KEY")

# Check if key is present
if API_KEY and API_KEY.startswith("gsk_"):
    client = Groq(api_key=API_KEY)
else:
    client = None
    API_KEY = None # Treat invalid/placeholder as missing

def generate_quiz_from_text(text: str):
    if not client:
        msg = "CRITICAL WARNING: GROQ_API_KEY is missing or invalid in backend/.env file."
        print(msg)
        with open("backend_error.log", "w", encoding="utf-8") as f:
            f.write(msg)
        return get_mock_quiz_data()

    prompt = """
    You are an AI that generates educational quizzes based STRICTLY on the provided text.
    Do not use outside knowledge. If the text does not contain enough information, generate fewer questions (minimum 2).
    
    Analyze the provided text and extract the following information in strict JSON format:
    1. "summary": A concise summary of the article (2-3 sentences).
    2. "key_entities": A dictionary with keys "people", "organizations", "locations", each containing a list of strings found in the text.
    3. "quiz": A list of 5 to 10 question objects. Each object must have:
       - "question": The question text (must be found in the article).
       - "options": A list of 4 distinct option strings.
       - "answer": The string text of the correct option (must be an exact match to one of the options).
       - "difficulty": "easy", "medium", or "hard".
       - "explanation": A short explanation strictly based on the text.
    4. "related_topics": A list of 5 Wikipedia-style topics for further reading.

    The output must be valid JSON only, without markdown code blocks.
    
    Article Text:
    """
    
    # Truncate text if too long (Groq Llama 3 70b has ~8k context usually, dependent on exact model limits, 
    # but let's be safe. ~20000 chars is roughly 5k tokens. 
    # llama3-70b-8192 supports 8k context. Input+Output < 8k. 
    # Let's limit input text to 15k chars to leave room for output.)
    clean_text = text[:15000]
    
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt + clean_text
                }
            ],
            temperature=0,
            max_tokens=2048,
            top_p=1,
            stream=False,
            response_format={"type": "json_object"}
        )
        
        response_text = completion.choices[0].message.content.strip()
        
        print(f"DEBUG: Raw Groq Response: {response_text[:500]}...")

        # Clean up potential markdown formatting (though json_object mode should help)
        if response_text.startswith("```"):
            response_text = re.sub(r"^```json|^```", "", response_text).strip("` \n")
            
        data = json.loads(response_text)
        
        # Validate/Fix answers
        if "quiz" in data:
            for q in data["quiz"]:
                options = q.get("options", [])
                answer = q.get("answer", "")
                
                # Ensure answer is in options
                if answer not in options:
                    clean_answer = answer.replace("Option ", "").strip()
                    if len(clean_answer) == 1 and clean_answer in "ABCD":
                        idx = ord(clean_answer) - ord('A')
                        if 0 <= idx < len(options):
                            q["answer"] = options[idx]
                            continue
                    
                    if options:
                        print(f"WARNING: Answer '{answer}' not found in options {options}. Defaulting to first option.")
                        q["answer"] = options[0]

        return data

    except json.JSONDecodeError:
        error_msg = f"JSON Decode Error. Raw response: {response_text}"
        print(error_msg)
        with open("backend_error.log", "w", encoding="utf-8") as f:
            f.write(error_msg)
        return get_mock_quiz_data()
    except Exception as e:
        import traceback
        error_msg = f"Error generating quiz: {e}\n{traceback.format_exc()}"
        print(error_msg)
        with open("backend_error.log", "w", encoding="utf-8") as f:
            f.write(error_msg)
        return get_mock_quiz_data()

def get_mock_quiz_data():
    return {
        "summary": "This is a mock summary because the Groq generation failed or no API key was provided. Please check your backend/.env file and ensure GROQ_API_KEY is allowed.",
        "key_entities": {
            "people": ["Mock Person"],
            "organizations": ["Mock Org"],
            "locations": ["Mock Location"]
        },
        "quiz": [
            {
                "question": "Why are you seeing this mock question?",
                "options": ["API Key Missing", "Groq Error", "Context Limit", "All of the above"],
                "answer": "All of the above",
                "difficulty": "easy",
                "explanation": "You need to provide a valid GROQ_API_KEY in the backend/.env file."
            }
        ],
        "related_topics": ["Groq Console", "API Keys"]
    }