def analyze_flow_rules(flow: dict) -> list:
    triggered_rules = []
    
    if flow.get('connection_count', 0) > 50 and flow.get('duration_seconds', 1) < 2.0:
        triggered_rules.append({"rule_id": "IDS-001", "name": "High Connection Rate", "severity": "HIGH", "score": 75})
        
    if flow.get('failed_connection_count', 0) > 15:
        triggered_rules.append({"rule_id": "IDS-002", "name": "Repeated Failed Connections", "severity": "HIGH", "score": 80})
        
    if flow.get('syn_ratio', 0) > 0.8 and flow.get('packet_count', 0) > 50:
        triggered_rules.append({"rule_id": "IDS-004", "name": "SYN-Heavy Pattern", "severity": "CRITICAL", "score": 90})
        
    if flow.get('bytes_per_second', 0) > 1000000:
        triggered_rules.append({"rule_id": "IDS-006", "name": "Abnormally High Traffic Volume", "severity": "MEDIUM", "score": 50})
        
    return triggered_rules