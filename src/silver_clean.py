import pandas as pd
import numpy as np
import os
from utils import SILVER_DIR, log

def clean_students(df):
    log("Cleaning students...")

    # Reset index
    df = df.reset_index(drop=True)

    # Step 1 : Remove duplicates
    df = df.drop_duplicates()
    df = df.drop_duplicates(subset='student_id', keep='first')

    # Step 2 : Strip whitespace from all text columns
    for col in df.select_dtypes(include='object').columns:
        df[col] = df[col].str.strip()

    # Step 3 : Normalize categories
    df['gender'] = df['gender'].replace({
        'Masculin': 'M', 'MASCULIN': 'M', 'masculin': 'M', 'Homme': 'M', 'homme': 'M',
        'Féminin': 'F', 'FEMININ': 'F', 'feminin': 'F'
    })
    df['grade_level'] = df['grade_level'].replace({
        '2ème bac': '2ème Bac', '2eme BAC': '2ème Bac',
        '1ere bac': '1ère Bac', '1 Bac': '1ère Bac',
        'tronc commun': 'Tronc Commun', 'TC': 'Tronc Commun'
    })
    df['status'] = df['status'].replace({
        'ADMIS': 'Admis', 'admis': 'Admis', 'Reçu': 'Admis',
        'ajourné': 'Ajourné', 'AJOURNE': 'Ajourné',
        'recalé': 'Recalé'
    })
    df['internet_access'] = df['internet_access'].replace({
        'oui': 'Oui', 'OUI': 'Oui', 'yes': 'Oui',
        'non': 'Non', 'NON': 'Non', 'no': 'Non'
    })

    # Step 4 : Fix age
    df['age'] = df['age'].replace({'seize': '16', 'dix-sept': '17',
                                    'nr': np.nan, 'inconnu': np.nan})
    df['age'] = pd.to_numeric(df['age'], errors='coerce')
    df.loc[df['age'] < 14, 'age'] = np.nan
    df.loc[df['age'] > 19, 'age'] = np.nan

    # Step 5 : Fix numeric columns
    for col, dirty in {
        'math_score':     ['non noté', 'n.a', 'absent', '?', '--'],
        'attendance_pct': ['nr', 'n.a.', '—', 'inconnu'],
        'average_score':  ['erreur', '--', 'n.a.']
    }.items():
        df[col] = df[col].replace({v: np.nan for v in dirty})
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df.loc[df['math_score'] < 0, 'math_score']             = np.nan
    df.loc[df['math_score'] > 20, 'math_score']            = np.nan
    df.loc[df['attendance_pct'] < 0, 'attendance_pct']     = np.nan
    df.loc[df['attendance_pct'] > 100, 'attendance_pct']   = np.nan
    df.loc[df['study_hours_per_day'] < 0, 'study_hours_per_day']  = np.nan
    df.loc[df['study_hours_per_day'] > 16, 'study_hours_per_day'] = np.nan

    # Step 6 : Standardize dates
    df['enrollment_date'] = pd.to_datetime(
        df['enrollment_date'], dayfirst=True, errors='coerce', format='mixed'
    )

    # Step 7 : Impute gender from first name
    male_names = ['khalid','tariq','rachid','mehdi','mouad','omar','youssef',
                  'amine','karim','hamza','ilyas','othmane','adam','bilal',
                  'soufiane','ayoub','zakaria','saad','anass','reda','nabil',
                  'hicham','fouad','abdelhamid','mostafa','hassan','ahmed','adil']
    female_names = ['houda','lina','sara','fatima','zineb','nadia','samira',
                    'aisha','loubna','rim','salma','hafsa','meryem','khadija',
                    'nour','widad','imane','soukaina','chaimae','asma','hana',
                    'yasmine','layla','siham','najat','boutaina','manal','hajar','ghita']

    df = df.reset_index(drop=True)
    for i in range(len(df)):
        first_name = str(df.loc[i, 'full_name']).split()[0].lower()
        if first_name in male_names:
            df.loc[i, 'gender'] = 'M'
        elif first_name in female_names:
            df.loc[i, 'gender'] = 'F'

    df['gender'] = df['gender'].fillna(df['gender'].mode()[0])

    # Step 8 : Impute missing values
    df['age'] = df.groupby('grade_level')['age'].transform(
        lambda x: x.fillna(x.median()))

    for col in ['math_score', 'french_score', 'study_hours_per_day']:
        df[col] = df.groupby('grade_level')[col].transform(
            lambda x: x.fillna(x.median()))

    df['attendance_pct'] = df.groupby('school_id')['attendance_pct'].transform(
        lambda x: x.fillna(x.median()))

    df['parent_education'] = df['parent_education'].fillna(
        df['parent_education'].mode()[0])

    df['scholarship'] = df.groupby('parent_education')['scholarship'].transform(
        lambda x: x.fillna(x.mode()[0]))

    # Step 9 : Recompute average_score
    df['average_score'] = (
        df['math_score'] + df['science_score'] +
        df['french_score'] + df['arabic_score'] +
        df['philosophy_score']
    ) / 5
    df['average_score'] = df['average_score'].round(2)

    # Step 10 : Impute enrollment_date with mode
    df['enrollment_date'] = df['enrollment_date'].fillna(
        df['enrollment_date'].mode()[0])

    log(f"✅ Students cleaned : {df.shape}")
    return df


def clean_silver():
    from bronze_ingest import ingest_bronze

    students, schools, regions = ingest_bronze()

    # Clean students
    students_clean = clean_students(students)

    # Schools and regions are already clean
    log("Schools and regions are already clean — no changes needed")

    # Save to silver
    os.makedirs(SILVER_DIR, exist_ok=True)
    students_clean.to_csv(os.path.join(SILVER_DIR, "students_silver.csv"), index=False)
    schools.to_csv(os.path.join(SILVER_DIR, "schools_silver.csv"), index=False)
    regions.to_csv(os.path.join(SILVER_DIR, "regional_stats_silver.csv"), index=False)

    log("✅ Silver layer saved")
    return students_clean, schools, regions


if __name__ == "__main__":
    clean_silver()