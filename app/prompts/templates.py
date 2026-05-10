CLASSIFICATION_PROMPT = """
Analyze the following emergency request and categorize it.
Request: {description}

Categories: Food shortage, Medical emergency, Flood rescue, Shelter requirement, Elderly assistance, Child safety, Disaster support.
Urgency Levels: LOW, MEDIUM, HIGH, CRITICAL.

Output format (JSON only):
{{
    "category": "string",
    "urgency": "string",
    "required_resources": "string describing needed items/help"
}}
"""

SUMMARIZATION_PROMPT = """
Summarize the following emergency request into a short, volunteer-friendly description (max 20 words).
Request: {description}
"""

TRANSLATION_PROMPT = """
Translate the following summary into Hindi.
Summary: {summary}
"""

RECOMMENDATION_PROMPT = """
Based on the category '{category}' and location '{location}', recommend suitable NGOs or help contacts from the following dataset:
Dataset: {dataset}

Output format: A short string with 1-2 relevant contacts.
"""
