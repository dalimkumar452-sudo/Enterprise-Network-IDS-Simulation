import sqlite3

def init_db():
    conn = sqlite3.connect('ids_simulation.db')
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS alerts (
        alert_id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp INTEGER, source_ip TEXT, destination_ip TEXT, 
        rule_name TEXT, severity TEXT, risk_score INTEGER, status TEXT
    )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS dashboard_stats (
        stat_id INTEGER PRIMARY KEY AUTOINCREMENT,
        total_flows INTEGER, alerts_generated INTEGER
    )''')
    
    conn.commit()
    conn.close()