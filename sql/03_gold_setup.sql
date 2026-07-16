-- ============================================
-- GOLD LAYER SETUP
-- ============================================

USE SCHEMA SCHOOL_PERFORMANCE.GOLD;

-- Gold master table
CREATE OR REPLACE TABLE GOLD_MASTER AS
SELECT 
    s.*,
    sc.school_name, sc.school_type, sc.milieu, sc.province, sc.region,
    sc.capacity, sc.num_teachers, sc.infrastructure_score,
    sc.digital_equipment, sc.year_founded,
    r.taux_reussite_national_pct, r.taux_pauvrete_pct,
    r.taux_alphabetisation_pct, r.couverture_internet_pct,
    r.depense_par_eleve_mad, r.taux_abandon_scolaire_pct,
    r.ratio_eleves_par_enseignant, r.nb_etablissements
FROM SCHOOL_PERFORMANCE.SILVER.STUDENTS_SILVER s
LEFT JOIN SCHOOL_PERFORMANCE.SILVER.SCHOOLS_SILVER sc ON s.school_id = sc.school_id
LEFT JOIN SCHOOL_PERFORMANCE.SILVER.REGIONAL_STATS_SILVER r ON sc.region = r.region;

-- KPI Global
CREATE OR REPLACE TABLE KPI_GLOBAL AS
SELECT 
    status,
    COUNT(*) as nombre_eleves,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as taux_pct
FROM GOLD_MASTER GROUP BY status;

-- KPI Region
CREATE OR REPLACE TABLE KPI_REGION AS
SELECT 
    region,
    COUNT(*) as total_eleves,
    SUM(CASE WHEN status = 'Admis' THEN 1 ELSE 0 END) as admis,
    ROUND(SUM(CASE WHEN status = 'Admis' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as taux_reussite_pct
FROM GOLD_MASTER GROUP BY region ORDER BY taux_reussite_pct DESC;

-- KPI Type
CREATE OR REPLACE TABLE KPI_TYPE AS
SELECT 
    school_type,
    COUNT(*) as total_eleves,
    SUM(CASE WHEN status = 'Admis' THEN 1 ELSE 0 END) as admis,
    ROUND(SUM(CASE WHEN status = 'Admis' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as taux_reussite_pct
FROM GOLD_MASTER GROUP BY school_type;

-- KPI Milieu
CREATE OR REPLACE TABLE KPI_MILIEU AS
SELECT 
    milieu,
    COUNT(*) as total_eleves,
    SUM(CASE WHEN status = 'Admis' THEN 1 ELSE 0 END) as admis,
    ROUND(SUM(CASE WHEN status = 'Admis' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as taux_reussite_pct
FROM GOLD_MASTER GROUP BY milieu;

-- KPI Level
CREATE OR REPLACE TABLE KPI_LEVEL AS
SELECT 
    grade_level,
    COUNT(*) as total_eleves,
    SUM(CASE WHEN status = 'Admis' THEN 1 ELSE 0 END) as admis,
    ROUND(SUM(CASE WHEN status = 'Admis' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as taux_reussite_pct
FROM GOLD_MASTER GROUP BY grade_level;

-- KPI Engagement
CREATE OR REPLACE TABLE KPI_ENGAGEMENT AS
SELECT 
    status,
    ROUND(AVG(attendance_pct), 2) as moyenne_assiduite,
    ROUND(AVG(study_hours_per_day), 2) as moyenne_heures_etude,
    ROUND(AVG(average_score), 2) as moyenne_score
FROM GOLD_MASTER GROUP BY status;