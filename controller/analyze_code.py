from db_connection import db_instance
from google import genai
from models import AnalysisHistory
import os

def get_code_suggestions(code):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("A chave da API do Gemini não foi configurada corretamente.")

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.0-flash", 
        contents=f"Você é um assistente de código que sugere melhorias. Analise este código Python e sugira melhorias: \n\n{code}"
    )
    return str(response.candidates[0].content.parts[0].text)

def analyze_code(code):

    # call openai
    analysis = get_code_suggestions(code)


    # Get a session
    session = db_instance.get_session()

    # Insert a record
    new_analysis = AnalysisHistory(
        code_snippet=f"{code}",
        suggestion=analysis
    )

    session.add(new_analysis)
    session.commit()
    session.close()
    return analysis

def get_all_analysis():

    # Get a session
    session = db_instance.get_session()
    all_analysis = session.query(AnalysisHistory).all()

    session.close()
    return all_analysis