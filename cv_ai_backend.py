from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import os

app = FastAPI()

# Haal de API-sleutel op uit de omgevingsvariabelen
openai.api_key = os.getenv("OPENAI_API_KEY")

class CVRequest(BaseModel):
    cv_text: str

@app.post("/evaluate-cv")
async def evaluate_cv(request: CVRequest):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Je bent een HR-expert die CV's beoordeelt en tips geeft."},
                {"role": "user", "content": f"Beoordeel dit CV en geef een score van 1-100 met verbeterpunten:\n{request.cv_text}"}
            ]
        )
        
        feedback = response["choices"][0]["message"]["content"]
        score = int([int(s) for s in feedback.split() if s.isdigit()][0])  # Extracteer score uit tekst
        
        return {"score": score, "feedback": feedback}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
