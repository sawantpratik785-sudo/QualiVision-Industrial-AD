import sqlite3
from datetime import datetime

DB_PATH = "inspections.db"

def init_db(db_path: str = DB_PATH):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inspection_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            part_category TEXT NOT NULL,
            model_used TEXT NOT NULL,
            anomaly_score REAL NOT NULL,
            threshold REAL NOT NULL,
            verdict TEXT NOT NULL,
            latency_ms REAL NOT NULL,
            image_name TEXT
        )
    """)
    conn.commit()
    conn.close()

def log_inspection(part_category: str, model_used: str, anomaly_score: float, 
                   threshold: float, verdict: str, latency_ms: float, image_name: str, db_path: str = DB_PATH):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO inspection_records 
        (timestamp, part_category, model_used, anomaly_score, threshold, verdict, latency_ms, image_name)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        part_category,
        model_used,
        round(float(anomaly_score), 4),
        round(float(threshold), 4),
        verdict,
        round(float(latency_ms), 2),
        image_name
    ))
    conn.commit()
    conn.close()

def fetch_recent_logs(limit: int = 20, db_path: str = DB_PATH):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT timestamp, part_category, model_used, anomaly_score, threshold, verdict, latency_ms, image_name
        FROM inspection_records
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return rows

if __name__ == "__main__":
    init_db()
    log_inspection("bottle", "PatchCore", 0.842, 0.50, "DEFECT", 45.2, "001.png")
    print("Database test successful. Recent rows:", fetch_recent_logs())
