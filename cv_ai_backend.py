from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import os

app = FastAPI()

# OpenAI API-key ophalen uit omgevingsvariabelen
openai.api_key = os.getenv("OPENAI_API_KEY")

class CVRequest(BaseModel):
    cv_text: str

@app.post("/evaluate-cv")
async def evaluate_cv(request: CVRequest):
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"Schrijf een feedback over dit CV: {request.cv_text}"}]
        )
        feedback = response.choices[0].message.content
        return {"message": "Evaluatie voltooid", "feedback": feedback}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
