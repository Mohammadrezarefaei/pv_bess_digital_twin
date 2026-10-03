import sqlite3
import pandas as pd

class BESSDigitalTwinDB:
    def __init__(self, db_name="bess_digital_twin.db"):
        self.db_name = db_name
        self.init_db()

    def init_db(self):
        """Initialize SQLite/Turso compatible database schema."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS simulation_runs (
                run_id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                total_revenue_eur REAL,
                status TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS hourly_dispatch (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_id INTEGER,
                hour INTEGER,
                solar_mw REAL,
                price_eur REAL,
                charge_mw REAL,
                discharge_mw REAL,
                net_export_mw REAL,
                soc_mwh REAL,
                FOREIGN KEY (run_id) REFERENCES simulation_runs (run_id)
            )
        ''')
        
        conn.commit()
        conn.close()

    def save_results(self, df_results, total_revenue, status="OPTIMAL"):
        """Save simulation run and hourly results to the database."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO simulation_runs (total_revenue_eur, status)
            VALUES (?, ?)
        ''', (total_revenue, status))
        
        run_id = cursor.lastrowid
        
        for _, row in df_results.iterrows():
            cursor.execute('''
                INSERT INTO hourly_dispatch (run_id, hour, solar_mw, price_eur, charge_mw, discharge_mw, net_export_mw, soc_mwh)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                run_id,
                int(row['hour']),
                float(row['solar_mw']),
                float(row['price_eur']),
                float(row['charge_mw']),
                float(row['discharge_mw']),
                float(row['net_export_mw']),
                float(row['soc_mwh'])
            ))
            
        conn.commit()
        conn.close()
        return run_id
