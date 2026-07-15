import re
import google.generativeai as genai

def clean_json_block(text: str) -> str:
    # Remove Markdown ```json code fences if present
    return re.sub(r"```(?:json)?\n(.*?)\n```", r"\1", text, flags=re.DOTALL).strip()

def generate_quiz(text: str) -> str:
    try:
        model = genai.GenerativeModel(model_name="models/gemini-2.5-flash")
        
        prompt = f"""You are a quiz generator.
From the following passage, create 3 multiple-choice questions. Each question should include:
- A "question"
- A list of 4 "options"
- A correct "answer" that must exactly match one of the options.

Format your output as **valid JSON**, like this:
[
  {{
    "question": "What is ...?",
    "options": ["A", "B", "C", "D"],
    "answer": "A"
  }}
]

Passage:
{text}
"""
        response = model.generate_content(prompt)
        quiz_text = response.text.strip()
        
        cleaned_text = clean_json_block(quiz_text)
        return cleaned_text
    except Exception as e:
        return f"⚠️ Error in Quiz Generation: {e}"