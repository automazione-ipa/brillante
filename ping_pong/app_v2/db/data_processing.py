import pandas as pd
import sqlite3
DB_PATH = ""
def preprocess_funding_rates():
    """
    Preprocess funding rates from the database to generate features.
    """
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM funding_rates", conn)
    conn.close()
    
    # Calculate daily averages, standard deviations, and trends
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.groupby(["exchange", "symbol"]).resample("D", on="timestamp")["rate"].agg(
        ["mean", "std", "min", "max"]
    ).reset_index()
    
    return df
