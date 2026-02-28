# Projet Big Data — Infrastructure Big Data

## Structure du dépôt

```
projet-Infrastructure-Big-data/
├── projet1/        ← Analyse d'une enquête de marché
└── projet2/        ← Analyse big data des ventes retail (à venir)
```

---

## Projet 1 — Analyse d'une enquête de marché pour la vente de plats jetables

### Contexte
Une entreprise locale souhaite lancer une activité de vente de plats jetables.
Une enquête de terrain a été réalisée auprès de 123 répondants.

### Fichiers
| Fichier | Description |
|---|---|
| `nettoyage.py` | Chargement, nettoyage et harmonisation des données |
| `analyse.py` | Analyse exploratoire, visualisations et segmentation |
| `rapport_projet1.md` | Rapport complet avec synthèse et recommandations |
| `donnees_nettoyees.csv` | Données après prétraitement |
| `donnees_segmentees.csv` | Données avec segments clients |
| `graphiques/` | 20 visualisations générées |

### Lancer le projet
```bash
pip install -r requirements.txt
python nettoyage.py
python analyse.py
```

---

## Projet 2 — Analyse big data des ventes dans le commerce en détail

### Contexte
Analyse de données de ventes en commerce de détail (109 443 lignes, 10 colonnes)
avec Apache Spark (PySpark) sur serveur distant Ubuntu.

### Fichiers
| Fichier | Description |
|---|---|
| `nettoyage.py` | Chargement CSV, nettoyage et feature engineering avec Spark |
| `analyse.py` | Analyse exploratoire, visualisations et modélisation MLlib |
| `rapport_projet2.md` | Rapport complet avec synthèse et recommandations |
| `donnees_nettoyees.parquet` | Données après prétraitement Spark |
| `graphiques/` | 11 visualisations générées |

### Lancer le projet
```bash
pip install -r requirements.txt
python nettoyage.py      # génère donnees_nettoyees.parquet
python analyse.py        # génère les graphiques et le rapport
```

---

## Présentation
Le fichier `rapport_final.tex` compile l'ensemble des deux projets en une présentation Beamer.
```bash
pdflatex rapport_final.tex
```
