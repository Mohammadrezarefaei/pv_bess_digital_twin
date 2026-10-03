import os
import pandas as pd
import pytest
from database.database_logger import BESSDigitalTwinDB

@pytest.fixture
def temp_db(tmp_path):
    db_path = tmp_path / "test_twin.db"
    return BESSDigitalTwinDB(db_name=str(db_path))

def test_database_logging(temp_db):
    # Mock results dataframe
    df_mock = pd.DataFrame({
        'hour': [0, 1],
        'solar_mw': [0.0, 0.0],
        'price_eur': [45.0, 50.0],
        'charge_mw': [0.0, 0.5],
        'discharge_mw': [0.0, 0.0],
        'net_export_mw': [0.0, -0.5],
        'soc_mwh': [2.0, 2.5]
    })
    
    total_rev = 125.50
    run_id = temp_db.save_results(df_mock, total_revenue=total_rev, status="OPTIMAL")
    
    assert run_id == 1
    
    # Verify records in database
    import sqlite3
    conn = sqlite3.connect(temp_db.db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT total_revenue_eur FROM simulation_runs WHERE run_id = 1")
    row = cursor.fetchone()
    conn.close()
    
    assert row[0] == 125.50
