import collections

# Simple sliding window baseline for synthetic anomaly detection
history = collections.deque(maxlen=100)

def calculate_anomaly_score(flow: dict) -> float:
    rate = flow.get('packets_per_second', 0)
    
    if len(history) < 10:
        history.append(rate)
        return 0.0
        
    avg_rate = sum(history) / len(history)
    history.append(rate)
    
    if avg_rate == 0: return 0.0
    
    deviation = abs(rate - avg_rate) / avg_rate
    score = min(deviation * 20, 100.0) # Map deviation to a 0-100 score
    return score