MODEL_VERSION = "v2.0"

HIGH_RISK_WORDS = [
    "offshore", "million", "fraud", "scam", "transfer",
    "illegal", "bribe", "launder", "suspicious"
]

MEDIUM_RISK_WORDS = [
    "urgent", "immediately", "deadline", "warning",
    "attention", "alert", "pending", "review"
]

def predict(text: str):
    text_lower = text.lower()

    if any(word in text_lower for word in HIGH_RISK_WORDS):
        label = "HIGH_RISK"
        confidence = 0.9
    elif any(word in text_lower for word in MEDIUM_RISK_WORDS):
        label = "MEDIUM_RISK"
        confidence = 0.7
    else:
        label = "LOW_RISK"
        confidence = 0.5

    return {
        "predicted_label": label,
        "confidence_score": confidence,
        "model_version": MODEL_VERSION,
    }







# Version 1 
"""import random
MODEL_VERSION = "v1.0"
def predict(text: str):
    text_lower = text.lower()

    if "offshore" in text_lower or "million" in text_lower:
        label = "HIGH_RISK"
        confidence = round(random.uniform(0.80, 0.95), 2)
    elif "urgent" in text_lower:
        label = "MEDIUM_RISK"
        confidence = round(random.uniform(0.60, 0.79), 2)
    else:
        label = "LOW_RISK"
        confidence = round(random.uniform(0.40, 0.59), 2)

    return {
        "predicted_label": label,
        "confidence_score": confidence,
        "model_version": MODEL_VERSION,
    }

    """