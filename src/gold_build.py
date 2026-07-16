import pandas as pd
import os
from utils import SILVER_DIR, GOLD_DIR, log

def build_gold():
    log("Building gold layer...")

    # Load silver data
    students = pd.read_csv(os.path.join(SILVER_DIR, "students_silver.csv"))
    schools  = pd.read_csv(os.path.join(SILVER_DIR, "schools_silver.csv"))
    regions  = pd.read_csv(os.path.join(SILVER_DIR, "regional_stats_silver.csv"))

    # Join all 3 sources
    df = students.merge(schools, on='school_id', how='left')
    df = df.merge(regions, on='region', how='left')
    log(f"Gold master shape : {df.shape}")

    # Risk score
    df['risk_score'] = (
        (1 - (df['average_score'] / 20)) * 0.5 +
        (1 - (df['attendance_pct'] / 100)) * 0.3 +
        (1 - (df['study_hours_per_day'] / 7)) * 0.2
    ).round(2)

    def classify_risk(score):
        if score >= 0.6:
            return 'Risque élevé'
        elif score >= 0.4:
            return 'Risque modéré'
        else:
            return 'Risque faible'

    df['risk_level'] = df['risk_score'].apply(classify_risk)

    # Create gold folder
    os.makedirs(GOLD_DIR, exist_ok=True)

    # Save gold master
    df.to_csv(os.path.join(GOLD_DIR, "gold_master.csv"), index=False)

    # KPI 1 : Global
    total = len(df)
    admis   = len(df[df['status'] == 'Admis'])
    ajourne = len(df[df['status'] == 'Ajourné'])
    recale  = len(df[df['status'] == 'Recalé'])
    kpi_global = pd.DataFrame({
        'status': ['Admis', 'Ajourné', 'Recalé'],
        'nombre_eleves': [admis, ajourne, recale],
        'taux_pct': [round(admis/total*100, 2),
                     round(ajourne/total*100, 2),
                     round(recale/total*100, 2)]
    })

    # KPI 2 : Par région
    total_region = df.groupby('region')['status'].count()
    admis_region = df[df['status'] == 'Admis'].groupby('region')['status'].count()
    kpi_region = pd.DataFrame({
        'total': total_region,
        'admis': admis_region,
        'taux_%': round(admis_region / total_region * 100, 2)
    }).sort_values('taux_%', ascending=False)

    # KPI 3 : Par type et milieu
    total_type  = df.groupby('school_type')['status'].count()
    admis_type  = df[df['status'] == 'Admis'].groupby('school_type')['status'].count()
    kpi_type    = pd.DataFrame({'total': total_type, 'admis': admis_type,
                                'taux_%': round(admis_type / total_type * 100, 2)})

    total_milieu = df.groupby('milieu')['status'].count()
    admis_milieu = df[df['status'] == 'Admis'].groupby('milieu')['status'].count()
    kpi_milieu   = pd.DataFrame({'total': total_milieu, 'admis': admis_milieu,
                                 'taux_%': round(admis_milieu / total_milieu * 100, 2)})

    # KPI 4 : Par niveau, genre, internet
    total_level   = df.groupby('grade_level')['status'].count()
    admis_level   = df[df['status'] == 'Admis'].groupby('grade_level')['status'].count()
    kpi_level     = pd.DataFrame({'total': total_level, 'admis': admis_level,
                                  'taux_%': round(admis_level / total_level * 100, 2)})

    total_gender  = df.groupby('gender')['status'].count()
    admis_gender  = df[df['status'] == 'Admis'].groupby('gender')['status'].count()
    kpi_gender    = pd.DataFrame({'total': total_gender, 'admis': admis_gender,
                                  'taux_%': round(admis_gender / total_gender * 100, 2)})

    total_internet = df.groupby('internet_access')['status'].count()
    admis_internet = df[df['status'] == 'Admis'].groupby('internet_access')['status'].count()
    kpi_internet   = pd.DataFrame({'total': total_internet, 'admis': admis_internet,
                                   'taux_%': round(admis_internet / total_internet * 100, 2)})

    # KPI 5 : Engagement
    kpi_engagement = df.groupby('status')[['attendance_pct',
                                           'study_hours_per_day',
                                           'average_score']].mean().round(2)

    # KPI 6 : Risk
    kpi_risk = df.groupby('risk_level').agg(
        nombre_eleves        = ('student_id', 'count'),
        moyenne_score        = ('average_score', 'mean'),
        moyenne_assiduite    = ('attendance_pct', 'mean'),
        moyenne_heures_etude = ('study_hours_per_day', 'mean')
    ).round(2)

    # Save all KPIs
    kpi_global.to_csv(os.path.join(GOLD_DIR, "kpi_global.csv"), index=False)
    kpi_region.to_csv(os.path.join(GOLD_DIR, "kpi_region.csv"))
    kpi_type.to_csv(os.path.join(GOLD_DIR, "kpi_type.csv"))
    kpi_milieu.to_csv(os.path.join(GOLD_DIR, "kpi_milieu.csv"))
    kpi_level.to_csv(os.path.join(GOLD_DIR, "kpi_level.csv"))
    kpi_gender.to_csv(os.path.join(GOLD_DIR, "kpi_gender.csv"))
    kpi_internet.to_csv(os.path.join(GOLD_DIR, "kpi_internet.csv"))
    kpi_engagement.to_csv(os.path.join(GOLD_DIR, "kpi_engagement.csv"))
    kpi_risk.to_csv(os.path.join(GOLD_DIR, "kpi_risk.csv"))

    # Power BI export
    df.to_csv(os.path.join(GOLD_DIR, "powerbi_dataset.csv"), index=False)

    log("✅ Gold layer complete")
    return df


if __name__ == "__main__":
    build_gold()