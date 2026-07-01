import time
import json
import google.generativeai as genai
from src.config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

def call_gemini_with_retry(prompt: str, retries=3, backoff_factor=2):
    """Executes a Gemini LLM call implementing an exponential backoff loop."""
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    for attempt in range(retries + 1):
        try:
            response = model.generate_content(
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            return json.loads(response.text)
        except Exception as e:
            if attempt == retries:
                print(f"LLM processing failed completely after {retries} retries: {e}")
                raise e
            sleep_time = backoff_factor ** attempt
            time.sleep(sleep_time)

def process_llm_classification(transactions: list) -> list:
    """Batches transactions and uses the LLM to classify missing categories."""
    if not transactions:
        return []
    
    prompt = f"""
    You are a financial data analyst. Classify the following transactions into exactly one of these categories:
    Food, Shopping, Travel, Transport, Utilities, Cash Withdrawal, Entertainment, Other.

    Input Transactions:
    {json.dumps(transactions)}

    Return a JSON array containing ONLY the category strings in the exact same order as the input.
    Example output format: ["Food", "Shopping"]
    """
    try:
        return call_gemini_with_retry(prompt)
    except Exception:
        # Fallback: if all retries fail, default them to 'Other' so the job doesn't crash completely
        return ["Other"] * len(transactions)

def generate_narrative_summary(transactions: list) -> dict:
    """Generates a high-level JSON summary report of all transactions."""
    prompt = f"""
    Analyze these processed transactions and generate a high-level summary report:
    {json.dumps(transactions)}

    Return a JSON object matching this exact schema:
    {{
        "total_spend_usd": float,
        "total_spend_inr": float,
        "top_merchants": ["Merchant1", "Merchant2", "Merchant3"],
        "narrative": "A 2-3 sentence overview of the spending patterns and anomalies found.",
        "risk_level": "low" or "medium" or "high"
    }}
    """
    try:
        return call_gemini_with_retry(prompt)
    except Exception:
        return {
            "total_spend_usd": 0.0,
            "total_spend_inr": 0.0,
            "top_merchants": [],
            "narrative": "Failed to generate narrative summary due to LLM errors.",
            "risk_level": "high"
        }