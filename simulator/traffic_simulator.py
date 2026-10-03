import requests
import random
import time

API_URL = "http://127.0.0.1:8000/api/flows"

def send_traffic():
    while True:
        is_attack = random.random() < 0.2
        
        flow = {
            "source_ip": f"192.0.2.{random.randint(1, 100)}",
            "destination_ip": "198.51.100.20",
            "source_port": random.randint(1024, 65535),
            "destination_port": random.choice([80, 443, 22]),
            "protocol": "TCP",
            "packet_count": random.randint(5, 20) if not is_attack else random.randint(100, 500),
            "byte_count": random.randint(1000, 5000) if not is_attack else random.randint(50000, 200000),
            "duration_seconds": random.uniform(0.1, 2.0),
            "connection_count": random.randint(1, 3) if not is_attack else random.randint(50, 100),
            "failed_connection_count": 0 if not is_attack else random.randint(20, 90),
            "syn_count": random.randint(1, 3) if not is_attack else random.randint(50, 100)
        }
        
        try:
            res = requests.post(API_URL, json=flow)
            print(f"Sent Flow. Classification: {res.json()['classification']} | Risk: {res.json()['risk_score']}")
        except Exception as e:
            print("API offline.", e)
            
        time.sleep(1)

if __name__ == "__main__":
    send_traffic()