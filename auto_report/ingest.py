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
