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
    # Fallback values
    result = {
        "category": "Emergency",
        "urgency": "MEDIUM",
        "required_resources": "Assessment required",
        "summary": description[:50] + "...",
        "hindi_summary": "विवरण उपलब्ध नहीं है",
        "recommendations": "Contact local authorities"
    }

    if not os.getenv("GEMINI_API_KEY"):
        print("WARNING: GEMINI_API_KEY not found. Using fallback values.")
        return result

    try:
        # Step 1: Classification
        classify_response = model.generate_content(CLASSIFICATION_PROMPT.format(description=description))
        try:
            text = classify_response.text.strip()
            if text.startswith("```json"):
                text = text[7:-3].strip()
            classification = json.loads(text)
            result["category"] = classification.get("category", result["category"])
            result["urgency"] = classification.get("urgency", result["urgency"])
            result["required_resources"] = classification.get("required_resources", result["required_resources"])
        except Exception as e:
            print(f"AI Classification Error: {e}")

        # Step 2: Summarization
        try:
            summary_response = model.generate_content(SUMMARIZATION_PROMPT.format(description=description))
            result["summary"] = summary_response.text.strip()
        except Exception as e:
            print(f"AI Summarization Error: {e}")

        # Step 3: Translation
        try:
            hindi_response = model.generate_content(TRANSLATION_PROMPT.format(summary=result["summary"]))
            result["hindi_summary"] = hindi_response.text.strip()
        except Exception as e:
            print(f"AI Translation Error: {e}")

        # Step 4: Recommendation
        try:
            recommend_response = model.generate_content(
                RECOMMENDATION_PROMPT.format(
                    category=result["category"],
                    location=location,
                    dataset=ngo_dataset
                )
            )
            result["recommendations"] = recommend_response.text.strip()
        except Exception as e:
            print(f"AI Recommendation Error: {e}")

    except Exception as e:
        print(f"Critical AI Workflow Error: {e}")
    
    return result
