import traceback
import google.generativeai as genai

def get_learning_recommendations(topic: str) -> str:
    # Fixed multi-line string configuration (replaced mismatched opening triple/closing single quotes)
    prompt = f"""You are an AI tutor. The student wants to learn about: {topic}.
Suggest a structured and adaptive learning path including key topics, order of learning, and resources.
Include beginner, intermediate, and advanced levels if needed."""
    
    try:
        model = genai.GenerativeModel(model_name="models/gemini-2.5-flash")
        response = model.generate_content(prompt)
        print("Gemini raw response completed.")
        
        if hasattr(response, "text"):
            return response.text
        elif hasattr(response, "parts") and response.parts:
            return response.parts[0].text
        else:
            return "Could not extract content from Gemini response."
    except Exception as e:
        traceback.print_exc()
        return f"Error occurred: {str(e)}"