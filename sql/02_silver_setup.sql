-- ============================================
-- SILVER LAYER SETUP
-- ============================================

USE SCHEMA SCHOOL_PERFORMANCE.SILVER;

CREATE OR REPLACE TABLE STUDENTS_SILVER (
    student_id          VARCHAR,
    full_name           VARCHAR,
    age                 FLOAT,
    gender              VARCHAR,
    grade_level         VARCHAR,
    school_id           VARCHAR,
    math_score          FLOAT,
    science_score       FLOAT,
    french_score        FLOAT,
    arabic_score        FLOAT,
    philosophy_score    FLOAT,
    attendance_pct      FLOAT,
    study_hours_per_day FLOAT,
    internet_access     VARCHAR,
    parent_education    VARCHAR,
    scholarship         VARCHAR,
    enrollment_date     DATE,
    average_score       FLOAT,
    status              VARCHAR
);

CREATE OR REPLACE TABLE SCHOOLS_SILVER (
    school_id            VARCHAR,
    school_name          VARCHAR,
    school_type          VARCHAR,
    milieu               VARCHAR,
    province             VARCHAR,
    region               VARCHAR,
    capacity             INT,
    num_teachers         INT,
    infrastructure_score FLOAT,
    digital_equipment    VARCHAR,
    year_founded         INT
);

CREATE OR REPLACE TABLE REGIONAL_STATS_SILVER (
    region                      VARCHAR,
    taux_reussite_national_pct  FLOAT,
    taux_pauvrete_pct           FLOAT,
    taux_alphabetisation_pct    FLOAT,
    couverture_internet_pct     FLOAT,
    depense_par_eleve_mad       FLOAT,
    taux_abandon_scolaire_pct   FLOAT,
    ratio_eleves_par_enseignant FLOAT,
    nb_etablissements           INT
);