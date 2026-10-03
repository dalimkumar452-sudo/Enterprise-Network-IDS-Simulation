🛡️ Enterprise Network Intrusion Detection System (IDS) & SOC Dashboard

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-00a393.svg)
![Cybersecurity](https://img.shields.io/badge/Domain-Cybersecurity-red.svg)
![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)

## 📌 Overview
This project is a **defensive cybersecurity simulation** of a Network Intrusion Detection System (IDS). It mimics the behavior of modern enterprise NDR (Network Detection and Response) tools by ingesting synthetic network flow data, analyzing it for threats, and displaying real-time alerts on a Security Operations Center (SOC) dashboard.

**Note:** This project relies entirely on safe, synthetic data. It does not scan, probe, or attack real-world infrastructure. 

## 🚀 Key Features
*   **Synthetic Traffic Simulator:** Safely generates normal network flows and anomalous patterns (e.g., Port Scans, Brute Force, SYN Floods) using RFC 5737 reserved IP ranges.
*   **Hybrid Detection Engine:** Combines **Signature-based detection** (known threat thresholds) with **Anomaly-based detection** (statistical baseline deviations).
*   **Risk Scoring Algorithm:** Calculates a dynamic threat score (0-100) to classify severity (Low, Medium, High, Critical).
*   **Real-Time SOC Dashboard:** A responsive, dark-themed UI featuring live packet sniffing, threat metrics, and interactive alert management for SOC analysts.
*   **RESTful API Backend:** Powered by FastAPI for high-speed data ingestion and asynchronous threat scoring.

## 🛠️ Technology Stack
*   **Backend:** Python, FastAPI, SQLite
*   **Frontend:** HTML5, Tailwind CSS, Vanilla JS, Chart.js, FontAwesome
*   **Data & Analytics:** Pandas, NumPy, Scikit-Learn

## 📸 SOC Dashboard Previews

* ![Dashboard View](output/Dashboard%20View.png)
* ![Live Terminal](output/Live%20Terminal.png)

## ⚙️ Installation & Usage

### 1. Clone the repository
```bash
git clone https://github.com/dalimkumar452-sudo/Enterprise-Network-IDS-Simulation.git
cd Enterprise-Network-IDS-Simulation
2. Set up Virtual Environment & Install Dependencies
Bash
python -m venv .venv
source .venv/Scripts/activate  # On Windows
pip install -r requirements.txt
3. Generate Dataset & Initialize DB
Bash
python simulator/generate_dataset.py
4. Run the API Server
Bash
python -m uvicorn backend.app:app --reload
5. Launch the SOC Dashboard & Traffic Simulator
Open frontend/index.html in your web browser.

Open a new terminal window and run:

Bash
python simulator/traffic_simulator.py
🧠 Cybersecurity Concepts Demonstrated
Threat Triage & Alert Fatigue Management: Implemented severity classifications to help Tier 1 analysts focus on critical events.

Network Flow Analysis: Feature engineering of raw telemetry (Packets/Sec, Byte Ratios, SYN Ratios).

Incident Response Workflow: Functionality to mark alerts as Investigating, Resolved, or False Positive.

📜 Ethical Disclaimer
This project is developed exclusively for educational purposes in defensive cybersecurity. All "malicious" scenarios are mathematically simulated locally.

Built with passion for network defense by  DALIM KUMAR 