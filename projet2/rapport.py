rapport = """
# RAPPORT — PROJET 2 : Analyse Big Data des ventes dans le commerce en détail

---

## 1. Prétraitement des données

Le dataset `retailsale.csv` contient **109 443 lignes** et **10 colonnes** portant sur les
produits, magasins, ventes, prix, promotions, stocks et la dimension temporelle.

### Traitements effectués
- Chargement via Apache Spark avec inférence de schéma
- Suppression de `promo_type_2` : 2 valeurs mais sans variabilité utile, aucun apport analytique
- Traitement des NaN de `promo_bin_1` (89% manquants) : remplacement par "Aucune"
- Suppression de la ligne avec NaN dans price, stock, sales et promo_type_1 (1 ligne)
- Conversion de la colonne `date` au format DateType (M/d/yyyy)
- Vérification et recast des types : sales (int), stock (int), price (float)
- Création de nouvelles variables :
  - `revenu_calcule` = sales × price
  - `annee`, `mois`, `semaine` extraits de la date
  - `en_promotion` : indicateur binaire (0 = pas de promo, 1 = en promo, basé sur promo_bin_1)
- Résultat final : **109 442 lignes** et **0 valeur manquante**

---

## 2. Analyse exploratoire

### Statistiques globales
| Variable | Moyenne | Std | Min | Max |
|---|---|---|---|---|
| sales | 0.46 | 2.22 | 0 | 161 |
| revenu_calcule | 1.57 | 7.39 | 0 | 796.95 |
| stock | 16.01 | 40.79 | 0 | 2892 |
| price | 8.92 | 10.87 | 0.25 | 219.90 |

La grande majorité des lignes présente **0 vente** (médiane = 0).
Les ventes positives concernent une minorité de combinaisons produit-magasin-date,
ce qui est typique d'un dataset retail à grande dimension.

### Top produits par volume de ventes
| Produit | Total ventes | Total revenu |
|---|---|---|
| P0438 | 7 194 | 1 798.50 |
| P0103 | 3 394 | 9 025.00 |
| P0051 | 2 850 | 1 995.00 |
| P0590 | 2 479 | 1 214.50 |
| P0364 | 1 627 | 1 627.00 |

### Top magasins par volume de ventes
| Magasin | Total ventes | Total revenu |
|---|---|---|
| S0085 | 2 893 | 10 479.44 |
| S0038 | 2 234 | 4 283.69 |
| S0026 | 2 040 | 7 704.23 |
| S0020 | 2 037 | 7 557.44 |
| S0095 | 1 762 | 9 943.93 |

### Impact des promotions
| Statut | Nb lignes | Ventes moyennes | Revenu total |
|---|---|---|---|
| Sans promotion | 97 596 | 0.462 | 143 054.22 |
| Avec promotion | 11 846 | 0.484 | 29 313.72 |

Les articles en promotion ont des ventes légèrement supérieures (+4.8%).

### Corrélations entre variables
| Paire | Corrélation | Interprétation |
|---|---|---|
| sales ↔ stock | **+0.4472** | Plus de stock → plus de ventes |
| sales ↔ price | -0.1067 | Prix élevé → légèrement moins de ventes |
| price ↔ stock | -0.1124 | Produits chers ont moins de stock |
| sales ↔ en_promotion | +0.0030 | Promotion : faible effet direct |

---

## 3. Visualisation des données

11 graphiques produits dans le dossier `graphiques/` :

| Graphique | Description |
|---|---|
| 01_ventes_par_produit | Top 15 produits par volume de ventes |
| 02_revenu_par_produit | Top 15 produits par revenu total |
| 03_ventes_par_magasin | Top 15 magasins par volume de ventes |
| 04_evolution_ventes | Évolution mensuelle des ventes |
| 05_evolution_revenu | Évolution mensuelle des revenus |
| 06_revenu_cumule | Revenus cumulés dans le temps |
| 07_impact_promotions | Ventes et revenus avec/sans promotion |
| 08_prix_vs_ventes | Relation prix → volume de ventes moyen |
| 09_distributions | Distribution des ventes, stocks et prix |
| 10_correlations | Matrice de corrélations (heatmap) |
| 11_reel_vs_predit | Valeurs réelles vs prédites (modèle) |

---

## 4. Modélisation — Régression linéaire (Spark MLlib)

### Modèle choisi : Régression Linéaire
**Justification :** La variable cible `sales` est continue et numérique.
La régression linéaire est interprétable, rapide à entraîner sur 100 000+ lignes
avec Spark MLlib, et permet d'identifier directement le poids de chaque variable
explicative sur les ventes.

### Variables explicatives utilisées
- `price` : prix du produit
- `stock` : niveau de stock disponible
- `en_promotion` : indicateur binaire de promotion

### Résultats du modèle
| Métrique | Valeur | Interprétation |
|---|---|---|
| **RMSE** | 1.8564 | Erreur moyenne de ~1.86 unité de vente |
| **MAE** | 0.6802 | Erreur absolue moyenne de ~0.68 unité |
| **R²** | 0.1872 | Le modèle explique ~19% de la variance des ventes |

Le R² de 0.19 indique que le prix, le stock et la promotion expliquent une partie
limitée des ventes. D'autres facteurs (saisonnalité, type de produit, localisation
du magasin) jouent un rôle important non capturé par ces trois variables seules.

---

## 5. Interprétation et recommandations

### Facteurs clés influençant les ventes
1. **Le stock** est le facteur le plus corrélé aux ventes (+0.45). Un manque de stock
   réduit directement les ventes réalisables.
2. **Le prix** a un effet négatif modéré (-0.11). Les produits moins chers vendent plus en volume.
3. **Les promotions** ont un effet direct faible (+0.003) mais génèrent 29 313 FCFA de revenu
   sur seulement 11 846 lignes, contre 143 054 FCFA sur 97 596 lignes sans promo.

### Recommandations — Gestion des stocks
- Maintenir un stock suffisant pour les produits à forte rotation (P0438, P0103, P0051).
- Les produits à 0 vente répétées sur plusieurs périodes doivent être réapprovisionnés
  uniquement en cas de promotion planifiée.

### Recommandations — Stratégie de promotion
- Concentrer les promotions sur les produits à fort potentiel de volume.
- Le faible impact direct des promotions sur les ventes moyennes suggère de cibler
  les promotions sur les périodes de faible activité pour stimuler la demande.

### Recommandations — Politique de prix
- La corrélation négative prix-ventes confirme la sensibilité au prix des clients.
- Les produits à prix élevé (ex. P0103 : prix moyen 2.66, revenu 9 025) génèrent
  plus de revenu par unité malgré un volume moindre.
- Stratégie recommandée : produits d'entrée de gamme à prix bas pour le volume,
  et produits premium ciblés pour maximiser le revenu.
"""

with open("rapport_projet2.md", "w", encoding="utf-8") as f:
    f.write(rapport)

print("Rapport sauvegardé dans 'rapport_projet2.md'")
