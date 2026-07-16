import os
import pandas as pd
from snowflake.connector import connect

# ── Paths ──────────────────────────────────────────────
BASE_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRONZE_DIR  = os.path.join(BASE_DIR, "data", "1_bronze")
SILVER_DIR  = os.path.join(BASE_DIR, "data", "2_silver")
GOLD_DIR    = os.path.join(BASE_DIR, "data", "3_gold")

# ── Snowflake connection ────────────────────────────────
def get_snowflake_connection():
    conn = connect(
        account   = os.getenv("SNOWFLAKE_ACCOUNT"),
        user      = os.getenv("SNOWFLAKE_USER"),
        password  = os.getenv("SNOWFLAKE_PASSWORD"),
        warehouse = os.getenv("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH"),
        database  = os.getenv("SNOWFLAKE_DATABASE",  "SCHOOL_PERFORMANCE"),
        schema    = os.getenv("SNOWFLAKE_SCHEMA",     "BRONZE")
    )
    return conn

# ── Simple logger ───────────────────────────────────────
def log(message):
    print(f"[LOG] {message}")