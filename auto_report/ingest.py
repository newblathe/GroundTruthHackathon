# ------------------------------------------------------------
# ingest.py
# Responsible for loading data from multiple sources:
#   1. CSV files
#   2. JSON files
#   3. SQL queries
#   4. SQLite databases
#
# The ingestion layer abstracts away input differences so the downstream pipeline always receives a clean pandas DataFrame.
# ------------------------------------------------------------

import pandas as pd
import sqlite3
from sqlalchemy import create_engine

def ingest_csv(file):
    return pd.read_csv(file)

def ingest_json(file):
    return pd.read_json(file)

def ingest_sql(query, connection_string):
    engine = create_engine(connection_string)
    df = pd.read_sql(query, engine)
    return df

def ingest_sqlite(query, db_path):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df
