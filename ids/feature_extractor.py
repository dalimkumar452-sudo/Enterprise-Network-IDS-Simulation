def extract_features(flow: dict) -> dict:
    dur = max(flow.get('duration_seconds', 0.001), 0.001)
    pkts = flow.get('packet_count', 1)
    bytes_c = flow.get('byte_count', 0)
    
    flow['bytes_per_second'] = bytes_c / dur
    flow['packets_per_second'] = pkts / dur
    flow['average_packet_size'] = bytes_c / max(pkts, 1)
    flow['failure_ratio'] = flow.get('failed_connection_count', 0) / max(flow.get('connection_count', 1), 1)
    flow['syn_ratio'] = flow.get('syn_count', 0) / max(pkts, 1)
    
    return flow