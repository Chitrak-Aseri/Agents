# fastapi_server.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.core.models import get_model_instance
from src.agents.review_agent import ReviewAgent
import uvicorn
from dotenv import load_dotenv
import os
load_dotenv()
print(os.environ)
app = FastAPI()

class ReviewRequest(BaseModel):
    provider: dict
    model_name: str
    code: str
    file_struct: str

@app.post("/v1/api/generate")
async def generate_code_review(req: ReviewRequest):
    config = {
        "provider": req.provider,
        "model_name": req.model_name,
        # You can load additional env vars here if needed
    }

    model = get_model_instance(config)
    agent = ReviewAgent(model)

    try:
        result = agent.generate_code_review(req.code, req.file_struct)
        return result.dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

