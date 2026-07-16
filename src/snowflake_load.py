import pandas as pd
import os
from utils import SILVER_DIR, log
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook

def load_to_snowflake():
    log("Loading data to Snowflake...")

    # Use Airflow Snowflake connection
    hook = SnowflakeHook(snowflake_conn_id='snowflake_default')
    conn = hook.get_conn()
    cursor = conn.cursor()

    # Load silver files
    students = pd.read_csv(os.path.join(SILVER_DIR, "students_silver.csv"))
    schools  = pd.read_csv(os.path.join(SILVER_DIR, "schools_silver.csv"))
    regions  = pd.read_csv(os.path.join(SILVER_DIR, "regional_stats_silver.csv"))

    # Convert column names to uppercase for Snowflake
    students.columns = students.columns.str.upper()
    schools.columns  = schools.columns.str.upper()
    regions.columns  = regions.columns.str.upper()

    # Truncate and reload silver tables
    cursor.execute("USE SCHEMA SCHOOL_PERFORMANCE.SILVER")

    cursor.execute("TRUNCATE TABLE STUDENTS_SILVER")
    from snowflake.connector.pandas_tools import write_pandas
    write_pandas(conn, students, "STUDENTS_SILVER")
    log("✅ STUDENTS_SILVER loaded")

    cursor.execute("TRUNCATE TABLE SCHOOLS_SILVER")
    write_pandas(conn, schools, "SCHOOLS_SILVER")
    log("✅ SCHOOLS_SILVER loaded")

    cursor.execute("TRUNCATE TABLE REGIONAL_STATS_SILVER")
    write_pandas(conn, regions, "REGIONAL_STATS_SILVER")
    log("✅ REGIONAL_STATS_SILVER loaded")

    # Rebuild gold layer
    cursor.execute("USE SCHEMA SCHOOL_PERFORMANCE.GOLD")
    cursor.execute("""
        CREATE OR REPLACE TABLE GOLD_MASTER AS
        SELECT s.*,
               sc.school_name, sc.school_type, sc.milieu, sc.province, sc.region,
               sc.capacity, sc.num_teachers, sc.infrastructure_score,
               sc.digital_equipment, sc.year_founded,
               r.taux_reussite_national_pct, r.taux_pauvrete_pct,
               r.taux_alphabetisation_pct, r.couverture_internet_pct,
               r.depense_par_eleve_mad, r.taux_abandon_scolaire_pct,
               r.ratio_eleves_par_enseignant, r.nb_etablissements
        FROM SCHOOL_PERFORMANCE.SILVER.STUDENTS_SILVER s
        LEFT JOIN SCHOOL_PERFORMANCE.SILVER.SCHOOLS_SILVER sc ON s.school_id = sc.school_id
        LEFT JOIN SCHOOL_PERFORMANCE.SILVER.REGIONAL_STATS_SILVER r ON sc.region = r.region
    """)
    log("✅ GOLD_MASTER rebuilt in Snowflake")

    conn.close()
    log("✅ Snowflake load complete")


if __name__ == "__main__":
    load_to_snowflake()