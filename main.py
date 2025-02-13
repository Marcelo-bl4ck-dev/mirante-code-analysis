from fastapi import FastAPI, Request
from controller.analyze_code import analyze_code, get_all_analysis
import os
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()
app = FastAPI()

class CodeRequest(BaseModel):
    code: str

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/health")
def agent_health():
    # to-do: Implement status check
    return {"status": "ok"}

@app.post("/analyze-code")
async def code_suggestions(code: CodeRequest):
    analysis = analyze_code(code)
    return {"message": "Analysis finished", "analysis": analysis, "code_snippet": code}

@app.get("/analysis")
def analysis():
    #todo: get_analysis
    all_analysis = get_all_analysis()
    return { "analysis_list": all_analysis }