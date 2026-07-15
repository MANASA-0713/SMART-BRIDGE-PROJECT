import google.generativeai as genai

def summarize_text(text: str) -> str:
    try:
        model = genai.GenerativeModel(model_name="models/gemini-2.5-flash")
        prompt = f"Summarize the following text in simple language:\n\n{text}"
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"⚠️ Error in Summary: {e}"
    