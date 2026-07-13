# Notes — Audit Qualité des Données Brutes (Bronze Layer)

**Date :** 2026-07-01
**Sources analysées :** students.csv, schools.csv, regional_stats.csv
**Notebook de référence :** notebooks/01_quality_exploration.ipynb

---

## 1. Vue d'ensemble

| Dataset            | Lignes | Colonnes | Doublons (lignes) | IDs dupliqués  | Valeurs manquantes |
| ------------------ | ------ | -------- | ----------------- | --------------- | ------------------ |
| students.csv       | 1 030  | 19       | 6                 | 30 (student_id) | Oui (9 colonnes)   |
| schools.csv        | 137    | 11       | 0                 | 0               | Non                |
| regional_stats.csv | 8      | 9        | 0                 | 0               | Non                |

→ **Seul students.csv présente des problèmes de qualité.**

---

## 2. Valeurs Manquantes — students.csv

| Colonne             | Valeurs manquantes | %     |
| ------------------- | ------------------ | ----- |
| math_score          | 75                 | 7.28% |
| scholarship         | 75                 | 7.28% |
| parent_education    | 74                 | 7.18% |
| attendance_pct      | 72                 | 6.99% |
| study_hours_per_day | 72                 | 6.99% |
| french_score        | 70                 | 6.80% |
| gender              | 65                 | 6.31% |
| age                 | 7                  | 0.68% |
| average_score       | 5                  | 0.49% |

---

## 3. Doublons — students.csv

- **6 lignes entièrement dupliquées** → suppression directe
- **30 student_id dupliqués** → IDs identiques avec données potentiellement différentes → à inspecter, conserver la première occurrence

---

## 4. Valeurs Non-Numériques Cachées

Colonnes stockées en `object` au lieu de `float/int` à cause de valeurs textuelles :

| Colonne        | Valeurs détectées                                         | Action              |
| -------------- | ----------------------------------------------------------- | ------------------- |
| age            | `'seize'`, `'dix-sept'`                                 | Convertir en 16, 17 |
| age            | `'nr'`, `'inconnu'`                                     | Remplacer par NaN   |
| math_score     | `'non noté'`, `'absent'`, `'?'`, `'--'`, `'n.a'` | Remplacer par NaN   |
| attendance_pct | `'nr'`, `'n.a.'`, `'—'`, `'inconnu'`               | Remplacer par NaN   |
| average_score  | `'erreur'`, `'--'`, `'n.a.'`                          | Remplacer par NaN   |

---

## 5. Valeurs Aberrantes (Outliers)

Plages métier définies pour le système éducatif marocain :

| Colonne             | Plage valide     | Problèmes détectés                | Action            |
| ------------------- | ---------------- | ------------------------------------ | ----------------- |
| age                 | 10 ≤ age ≤ 25  | min=0, max=200, 3 valeurs > 25       | Hors plage → NaN |
| math_score          | 0 ≤ score ≤ 20 | 4 valeurs négatives, 8 valeurs > 20 | Hors plage → NaN |
| attendance_pct      | 0 ≤ pct ≤ 100  | 1 valeur négative, 6 valeurs > 100  | Hors plage → NaN |
| study_hours_per_day | 0 ≤ h ≤ 16     | 1 valeur négative, 7 valeurs > 16   | Hors plage → NaN |
| average_score       | 0 ≤ score ≤ 20 | Aucun outlier détecté              | Aucune action     |

---

## 6. Catégories Incohérentes — students.csv

### gender

| Valeurs brutes                                | Valeur normalisée |
| --------------------------------------------- | ------------------ |
| Masculin, MASCULIN, masculin, Homme, homme, M | Masculin           |
| Féminin, FEMININ, feminin, F                 | Féminin           |

### grade_level

| Valeurs brutes                 | Valeur normalisée             |
| ------------------------------ | ------------------------------ |
| 2ème Bac, 2ème bac, 2eme BAC | 2ème Bac                      |
| 1ère Bac, 1ere bac, 1 Bac*    | 1ère Bac                      |
| Tronc Commun, tronc commun, TC | Tronc Commun                   |
| 3ème Collège                 | 3ème Collège (déjà propre) |

*⚠️ `1 Bac` supposé être `1ère Bac` — à confirmer

### status

| Valeurs brutes              | Valeur normalisée |
| --------------------------- | ------------------ |
| Admis, ADMIS, admis, Reçu  | Admis              |
| Ajourné, ajourné, AJOURNE | Ajourné           |
| Recalé, recalé            | Recalé            |

### internet_access

| Valeurs brutes     | Valeur normalisée |
| ------------------ | ------------------ |
| Oui, oui, OUI, yes | Oui                |
| Non, non, NON, no  | Non                |

### parent_education

Aucun problème de cohérence — 4 valeurs propres : `Aucun`, `Primaire`, `Secondaire`, `Supérieur`

### scholarship

Aucun problème de cohérence — 2 valeurs propres : `Oui`, `Non`

---

## 7. Formats de Dates — enrollment_date

| Format                    | Nombre de valeurs |
| ------------------------- | ----------------- |
| YYYY-MM-DD (standard ISO) | 850               |
| DD/MM/YYYY                | 73                |
| DD Month YYYY             | 34                |
| Autre / Inconnu           | 73                |

→ Action : tout standardiser en YYYY-MM-DD dans la couche silver.

---

## 8. Intégrité des Jointures

| Jointure                                | Résultat                   |
| --------------------------------------- | --------------------------- |
| students.school_id → schools.school_id | ✅ Aucun school_id orphelin |
| schools.region → regional_stats.region | ✅ Aucune région manquante |

---

## 9. Décisions de Nettoyage (à implémenter en Silver)

### Doublons

- 6 lignes entièrement dupliquées → suppression directe
- 30 student_id dupliqués → conservation de la première occurrence

### Normalisation des catégories

| Colonne         | Règle appliquée                                                                       |
| --------------- | --------------------------------------------------------------------------------------- |
| gender          | Toutes les variantes (Masculin, homme, M...) → M / F, inféré par prénom si manquant |
| grade_level     | Variantes (2eme BAC, TC...) → 4 valeurs standards                                      |
| status          | Variantes (ADMIS, Reçu...) → Admis / Ajourné / Recalé                               |
| internet_access | (yes, oui, OUI...) → Oui / Non                                                         |

### Valeurs non-numériques

| Colonne        | Valeurs remplacées par NaN                               |
| -------------- | --------------------------------------------------------- |
| age            | 'nr', 'inconnu' → NaN / 'seize' → 16 / 'dix-sept' → 17 |
| math_score     | 'non noté', 'absent', '?', '--', 'n.a' → NaN            |
| attendance_pct | 'nr', 'n.a.', '—', 'inconnu' → NaN                      |
| average_score  | 'erreur', '--', 'n.a.' → NaN                             |

### Cohérence métier

### Imputation des valeurs manquantes

### Outliers

| Colonne             | Plage valide     | Action                                               |
| ------------------- | ---------------- | ---------------------------------------------------- |
| age                 | 14 ≤ age ≤ 19  | Hors plage → NaN puis réimputation par grade_level |
| math_score          | 0 ≤ score ≤ 20 | Hors plage → NaN                                    |
| attendance_pct      | 0 ≤ pct ≤ 100  | Hors plage → NaN                                    |
| study_hours_per_day | 0 ≤ h ≤ 16     | Hors plage → NaN                                    |

| Colonne             | Méthode                                                     | Justification                                                  |
| ------------------- | ------------------------------------------------------------ | -------------------------------------------------------------- |
| gender              | Inférence par prénom (dictionnaire marocain) + mode global | Précision contextuelle                                        |
| age                 | Médiane par grade_level                                     | L'âge varie selon le niveau scolaire                          |
| math_score          | Médiane par grade_level                                     | Les notes varient selon le niveau                              |
| french_score        | Médiane par grade_level                                     | Les notes varient selon le niveau                              |
| attendance_pct      | Médiane par school_id                                       | L'assiduité dépend de l'établissement                       |
| study_hours_per_day | Médiane par grade_level                                     | Les heures d'étude varient selon le niveau                    |
| parent_education    | Mode global (Aucun)                                          | Variable catégorielle, pas de groupe logique                  |
| scholarship         | Mode par groupe parent_education                             | La bourse dépend du niveau socio-économique                  |
| average_score       | Moyenne des 5 matières                                      | Calcul direct, pas d'estimation                                |
| enrollment_date     | Mode global                                                  | Dates non parsables remplacées par la date la plus fréquente |

### Standardisation des dates

- enrollment_date : 3 formats détectés (YYYY-MM-DD, DD/MM/YYYY, DD Month YYYY) → tout standardisé en YYYY-MM-DD
