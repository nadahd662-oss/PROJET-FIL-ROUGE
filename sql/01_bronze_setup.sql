-- ============================================
-- BRONZE LAYER SETUP
-- ============================================

-- Create database
CREATE DATABASE IF NOT EXISTS SCHOOL_PERFORMANCE;

-- Create schemas
CREATE SCHEMA IF NOT EXISTS SCHOOL_PERFORMANCE.BRONZE;
CREATE SCHEMA IF NOT EXISTS SCHOOL_PERFORMANCE.SILVER;
CREATE SCHEMA IF NOT EXISTS SCHOOL_PERFORMANCE.GOLD;

-- Use bronze schema
USE SCHEMA SCHOOL_PERFORMANCE.BRONZE;

-- Students table
CREATE OR REPLACE TABLE STUDENTS (
    student_id          VARCHAR,
    full_name           VARCHAR,
    age                 VARCHAR,
    gender              VARCHAR,
    grade_level         VARCHAR,
    school_id           VARCHAR,
    math_score          VARCHAR,
    science_score       VARCHAR,
    french_score        VARCHAR,
    arabic_score        VARCHAR,
    philosophy_score    VARCHAR,
    attendance_pct      VARCHAR,
    study_hours_per_day VARCHAR,
    internet_access     VARCHAR,
    parent_education    VARCHAR,
    scholarship         VARCHAR,
    enrollment_date     VARCHAR,
    average_score       VARCHAR,
    status              VARCHAR
);

-- Schools table
CREATE OR REPLACE TABLE SCHOOLS (
    school_id            VARCHAR,
    school_name          VARCHAR,
    school_type          VARCHAR,
    milieu               VARCHAR,
    province             VARCHAR,
    region               VARCHAR,
    capacity             VARCHAR,
    num_teachers         VARCHAR,
    infrastructure_score VARCHAR,
    digital_equipment    VARCHAR,
    year_founded         VARCHAR
);

-- Regional stats table
CREATE OR REPLACE TABLE REGIONAL_STATS (
    region                      VARCHAR,
    taux_reussite_national_pct  VARCHAR,
    taux_pauvrete_pct           VARCHAR,
    taux_alphabetisation_pct    VARCHAR,
    couverture_internet_pct     VARCHAR,
    depense_par_eleve_mad       VARCHAR,
    taux_abandon_scolaire_pct   VARCHAR,
    ratio_eleves_par_enseignant VARCHAR,
    nb_etablissements           VARCHAR
);

-- File format
CREATE OR REPLACE FILE FORMAT SCHOOL_PERFORMANCE.BRONZE.CSV_FORMAT
    TYPE = 'CSV'
    FIELD_DELIMITER = ','
    SKIP_HEADER = 1
    NULL_IF = ('NULL', 'null', '')
    EMPTY_FIELD_AS_NULL = TRUE;

-- Stage
CREATE OR REPLACE STAGE SCHOOL_PERFORMANCE.BRONZE.BRONZE_STAGE
    FILE_FORMAT = SCHOOL_PERFORMANCE.BRONZE.CSV_FORMAT;