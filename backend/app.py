from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import time
import sqlite3
import joblib
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ids.feature_extractor import extract_features
from ids.rule_engine import analyze_flow_rules
from ids.anomaly_detector import calculate_anomaly_score
from ids.risk_engine import calculate_risk_score
from backend.database import init_db

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

init_db()

try:
    ml_model = joblib.load('models/ids_rf_model.pkl')
except:
    ml_model = None

class FlowRecord(BaseModel):
    source_ip: str; destination_ip: str; source_port: int; destination_port: int
    protocol: str; packet_count: int; byte_count: int; duration_seconds: float
    connection_count: int; failed_connection_count: int; syn_count: int

@app.post("/api/flows")
async def ingest_flow(flow: FlowRecord):
    data = extract_features(flow.dict())
    
    rules = analyze_flow_rules(data)
    anomaly = calculate_anomaly_score(data)
    
    ml_prob = 0.0
    if ml_model:
        features = [[data['packet_count'], data['byte_count'], data['duration_seconds'], 
                     data['bytes_per_second'], data['packets_per_second'], data['connection_count'], 
                     data['failed_connection_count'], data['syn_count'], data['average_packet_size']]]
        ml_prob = ml_model.predict_proba(features)[0][1]
        
    risk_score, classification = calculate_risk_score(rules, anomaly, ml_prob)
    
    if risk_score > 40:
        rule_name = rules[0]['name'] if rules else ("ML Anomaly" if ml_prob > 0.5 else "Statistical Anomaly")
        severity = rules[0]['severity'] if rules else "MEDIUM"
        
        conn = sqlite3.connect('ids_simulation.db')
        c = conn.cursor()
        c.execute("INSERT INTO alerts (timestamp, source_ip, destination_ip, rule_name, severity, risk_score, status) VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (int(time.time()), data['source_ip'], data['destination_ip'], rule_name, severity, risk_score, "NEW"))
        conn.commit(); conn.close()
        
    return {"status": "processed", "classification": classification, "risk_score": risk_score}

@app.get("/api/dashboard/stats")
async def get_stats():
    conn = sqlite3.connect('ids_simulation.db')
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM alerts")
    alerts_count = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM alerts WHERE status='NEW'")
    open_alerts = c.fetchone()[0]
    conn.close()
    
    return {"total_alerts": alerts_count, "open_alerts": open_alerts}

@app.get("/api/alerts")
async def get_alerts():
    conn = sqlite3.connect('ids_simulation.db')
    c = conn.cursor()
    c.execute("SELECT alert_id, timestamp, source_ip, destination_ip, rule_name, severity, risk_score, status FROM alerts ORDER BY alert_id DESC LIMIT 20")
    alerts = [{"id": r[0], "ts": r[1], "src": r[2], "dst": r[3], "rule": r[4], "severity": r[5], "risk": r[6], "status": r[7]} for r in c.fetchall()]
    conn.close()
    return alerts

@app.put("/api/alerts/{alert_id}/status")
async def update_status(alert_id: int, status: str):
    conn = sqlite3.connect('ids_simulation.db')
    c = conn.cursor()
    c.execute("UPDATE alerts SET status = ? WHERE alert_id = ?", (status, alert_id))
    conn.commit(); conn.close()
    return {"message": "Updated"}