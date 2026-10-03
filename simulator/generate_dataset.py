import pandas as pd
import random
import time
import os

os.makedirs('data', exist_ok=True)

def generate_dataset(num_records=5000):
    data = []
    scenarios = ['NORMAL', 'SUSPICIOUS']
    
    for _ in range(num_records):
        scenario = random.choices(scenarios, weights=[0.8, 0.2])[0]
        timestamp = int(time.time()) - random.randint(0, 86400 * 30)
        
        src_ip = f"192.0.2.{random.randint(1, 254)}"
        dst_ip = f"198.51.100.{random.randint(1, 50)}"
        protocol = random.choice(['TCP', 'UDP'])
        
        if scenario == 'NORMAL':
            pkt_cnt = random.randint(5, 50)
            bytes_cnt = pkt_cnt * random.randint(40, 1500)
            dur = random.uniform(0.1, 10.0)
            conn_cnt = random.randint(1, 5)
            fail_cnt = 0
            syn_cnt = random.randint(1, conn_cnt * 2)
            label = 0
            scenario_type = 'NORMAL_WEB'
        else:
            attack_type = random.choice(['HIGH_CONN', 'PORT_PROBE', 'SYN_HEAVY'])
            if attack_type == 'HIGH_CONN':
                conn_cnt = random.randint(50, 200)
                pkt_cnt = conn_cnt * random.randint(1, 5)
                bytes_cnt = pkt_cnt * 50
                dur = random.uniform(0.5, 2.0)
                fail_cnt = random.randint(10, conn_cnt)
                syn_cnt = conn_cnt
                scenario_type = 'REPEATED_FAILED_CONNECTIONS'
            elif attack_type == 'PORT_PROBE':
                conn_cnt = random.randint(20, 100)
                pkt_cnt = conn_cnt
                bytes_cnt = pkt_cnt * 64
                dur = random.uniform(1.0, 5.0)
                fail_cnt = conn_cnt
                syn_cnt = conn_cnt
                scenario_type = 'MULTI_PORT_PROBING_PATTERN'
            else:
                conn_cnt = random.randint(10, 50)
                pkt_cnt = random.randint(100, 500)
                bytes_cnt = pkt_cnt * 64
                dur = random.uniform(0.1, 1.0)
                fail_cnt = 0
                syn_cnt = int(pkt_cnt * 0.9)
                scenario_type = 'SYN_HEAVY_PATTERN'
            label = 1
            
        data.append([
            timestamp, src_ip, dst_ip, random.randint(1024, 65535), random.randint(20, 443), protocol,
            pkt_cnt, bytes_cnt, dur, conn_cnt, fail_cnt, syn_cnt, random.randint(0, 2),
            bytes_cnt/pkt_cnt, label, scenario_type
        ])
        
    df = pd.DataFrame(data, columns=[
        'timestamp', 'source_ip', 'destination_ip', 'source_port', 'destination_port', 'protocol',
        'packet_count', 'byte_count', 'duration_seconds', 'connection_count', 'failed_connection_count',
        'syn_count', 'rst_count', 'average_packet_size', 'label', 'scenario_type'
    ])
    df.to_csv('data/network_traffic.csv', index=False)
    print("Dataset generated at data/network_traffic.csv")

if __name__ == "__main__":
    generate_dataset()