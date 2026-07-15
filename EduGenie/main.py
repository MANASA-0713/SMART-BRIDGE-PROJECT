from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import json

# Import system configuration configurations
import config

# Import our processing modules
from qna import answer_question_with_gemini
from explanation_module import explain_topic
from summary_module import summarize_text
from quiz_module import generate_quiz
from learning_path import get_learning_recommendations

app = FastAPI(title="EduGenie AI Learning Assistant")

# --- Define Request Input Schemas for Swagger UI ---
class TopicRequest(BaseModel):
    topic: str

class TextRequest(BaseModel):
    text: str


@app.get("/")
def read_root():
    return {"message": "EduGenie Backend API is running successfully!"}

# 1. Q&A - GET API using Gemini
@app.get("/qa")
async def answer_question(question: str = Query(...)):
    answer = answer_question_with_gemini(question)
    return {"answer": answer}

# 2. Explanation - POST API
@app.post("/explain")
async def explain_api(payload: TopicRequest):
    topic = payload.topic
    if not topic:
        return JSONResponse(content={"error": "Please provide a topic."}, status_code=400)
    
    explanation = explain_topic(topic)
    return {"topic": topic, "explanation": explanation}

# 3. Summarization - POST API
@app.post("/summarize")
async def summarize_api(payload: TextRequest):
    text = payload.text
    if not text:
        return JSONResponse(content={"error": "Please provide text to summarize."}, status_code=400)
        
    summary = summarize_text(text)
    return {"summary": summary}

# 4. Quiz Generation - POST API
@app.post("/quiz")
async def quiz_api(payload: TextRequest):
    text = payload.text
    if not text:
        return JSONResponse(content={"error": "Please provide text for quiz."}, status_code=400)
        
    quiz_raw = generate_quiz(text)
    
    try:
        quiz_json = json.loads(quiz_raw)
        return {"quiz": quiz_json}
    except Exception:
        return {"quiz": quiz_raw}

# 5. Learning Recommendations - GET API
@app.get("/learn/recommendations")
async def learning_recommendation_api(topic: str = Query(...)):
    recommendation = get_learning_recommendations(topic)
    return {"topic": topic, "recommendation": recommendation}