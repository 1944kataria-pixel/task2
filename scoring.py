# scoring.py

SCORE_MAP = {
    "HIGH_MANUAL": (75, 100),
    "MEDIUM_MANUAL": (40, 74),
    "LOW_MANUAL": (0, 39),
}

def score_company(classification: str, signals: dict) -> int:
    """
    Accepts classify_company() output and raw signals,
    returns a 0–100 lead score.
    
    Scoring logic:
    - Base range from classification tier
    - Fine-tuned within that range using manual_roles + manual_keywords
    """
    base_min, base_max = SCORE_MAP.get(classification, (0, 39))
    band = base_max - base_min

    # Normalise signals to a 0.0–1.0 position within the band
    manual_roles    = min(signals.get("manual_roles", 0), 10)    # cap at 10
    manual_keywords = min(signals.get("manual_keywords", 0), 5)  # cap at 5
    scaling         = signals.get("scaling", False)

    role_score    = manual_roles / 10          # 0.0–1.0
    keyword_score = manual_keywords / 5        # 0.0–1.0
    scaling_boost = 0.15 if scaling else 0.0   # +15% nudge within band

    position = (role_score * 0.6) + (keyword_score * 0.3) + scaling_boost
    position = min(position, 1.0)              # clamp

    score = int(base_min + position * band)
    return score