import pandas as pd
import os
from utils import BRONZE_DIR, log

def ingest_bronze():
    log("Starting bronze ingestion...")

    # Load raw CSV files
    students = pd.read_csv(os.path.join(BRONZE_DIR, "students.csv"))
    schools  = pd.read_csv(os.path.join(BRONZE_DIR, "schools.csv"))
    regions  = pd.read_csv(os.path.join(BRONZE_DIR, "regional_stats.csv"))

    log(f"Students  loaded : {students.shape}")
    log(f"Schools   loaded : {schools.shape}")
    log(f"Regions   loaded : {regions.shape}")

    # Basic validation — check required columns exist
    assert 'student_id' in students.columns, "Missing column: student_id"
    assert 'school_id'  in schools.columns,  "Missing column: school_id"
    assert 'region'     in regions.columns,  "Missing column: region"

    log("✅ Bronze ingestion complete")

    return students, schools, regions


if __name__ == "__main__":
    ingest_bronze()