import google.generativeai as genai
import os
import json
from dotenv import load_dotenv
from ..prompts.templates import (
    CLASSIFICATION_PROMPT,
    SUMMARIZATION_PROMPT,
    TRANSLATION_PROMPT,
    RECOMMENDATION_PROMPT
)

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

async def run_ai_workflow(description: str, location: str, ngo_dataset: str):
    # Step 1: Classification
    classify_response = model.generate_content(CLASSIFICATION_PROMPT.format(description=description))
    try:
        # Clean up potential markdown formatting in JSON response
        text = classify_response.text.strip()
        if text.startswith("```json"):
            text = text[7:-3].strip()
        classification = json.loads(text)
    except:
        classification = {"category": "Other", "urgency": "MEDIUM", "required_resources": "General help"}

    # Step 2: Summarization
    summary_response = model.generate_content(SUMMARIZATION_PROMPT.format(description=description))
    summary = summary_response.text.strip()

    # Step 3: Translation
    hindi_response = model.generate_content(TRANSLATION_PROMPT.format(summary=summary))
    hindi_summary = hindi_response.text.strip()

    # Step 4: Recommendation
    recommend_response = model.generate_content(
        RECOMMENDATION_PROMPT.format(
            category=classification.get("category"),
            location=location,
            dataset=ngo_dataset
        )
    )
    recommendations = recommend_response.text.strip()

    return {
        "category": classification.get("category"),
        "urgency": classification.get("urgency"),
        "required_resources": classification.get("required_resources"),
        "summary": summary,
        "hindi_summary": hindi_summary,
        "recommendations": recommendations
    }
