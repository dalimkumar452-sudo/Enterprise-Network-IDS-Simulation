def calculate_risk_score(rule_hits: list, anomaly_score: float, ml_prob: float) -> tuple:
    rule_score = max([r['score'] for r in rule_hits]) if rule_hits else 0
    ml_score = ml_prob * 100
    
    # Hybrid Weights
    final_score = (rule_score * 0.4) + (anomaly_score * 0.3) + (ml_score * 0.3)
    
    if final_score < 20: classification = "NORMAL"
    elif final_score < 40: classification = "LOW RISK"
    elif final_score < 60: classification = "SUSPICIOUS"
    elif final_score < 80: classification = "HIGH RISK"
    else: classification = "CRITICAL INVESTIGATION"
    
    return min(round(final_score), 100), classification