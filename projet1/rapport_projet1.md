
# RAPPORT — PROJET 1 : Analyse d'une enquête de marché pour la vente de plats jetables

---

## 1. Préparation des données

Le fichier enquête.xlsx contient **123 répondants** et **29 variables** portant sur les
activités, l'utilisation actuelle des emballages, les préférences produit et la sensibilité au prix.

### Traitements effectués
- Renommage des colonnes en noms courts et explicites
- Suppression de la colonne non pertinente (URL photos)
- Conversion des montants textuels en valeurs numériques :
  - Gestion des formats "5000f", "10.000f", "5000 à 10000f", "20 ou 35 milles le mois"
  - Les plages (ex. "5000 à 10000") ont été remplacées par leur milieu (7500)
  - Les mentions "milles" ont été multipliées par 1000
- Remplacement des valeurs manquantes numériques par la médiane de la colonne
- Remplacement des NaN textuels par "Non précisé" ou "Aucune"
- Harmonisation des réponses : fréquences de livraison, quantités journalières
- Résultat final : **0 valeur manquante** dans le dataset nettoyé

---

## 2. Analyse exploratoire

### a) Types d'activités
Les répondants sont majoritairement des **restaurateurs** vendant des mets africains et européens.
Les fast-foods et snacks représentent une part significative du panel.

### b) Utilisation actuelle des plats jetables
- **100%** des répondants utilisent déjà des emballages alimentaires jetables.
- **48.0%** utilisent entre 1 et 10 emballages par jour.
- **38.2%** en utilisent entre 10 et 30 par jour.
- **13.8%** en utilisent entre 30 et 50 par jour.

### c) Préférences produit
- **Compartiments** : la combinaison la plus demandée est *"1 seul compartiment, 2 compartiments, 3 compartiments"*.
- **Contenance** : la contenance préférée pour 1 compartiment est **850ML**.
- **Design** : **78.9%** préfèrent un emballage avec fenêtre transparente.
- **Matériau** : le matériau le plus demandé est **Carton**.

### d) Sensibilité au prix
- Prix médian actuellement payé pour la centaine : **3500 FCFA**
- Budget mensuel médian : **7000 FCFA**
- **36.6%** accepteraient de payer un peu plus cher que leur prix actuel.
- **58.5%** seraient "peut-être" prêts à payer plus.

---

## 3. Visualisation des résultats

17 graphiques ont été produits (dossier `graphiques/`) couvrant :
- Les types d'activités et l'utilisation des emballages
- Les préférences en compartiments, contenance et design
- La distribution des budgets et des prix actuels
- La relation entre le prix payé et la probabilité d'achat
- Les principaux critères de choix
- La segmentation et le profil des segments

### Relation prix → intention d'achat
Les répondants qui paient actuellement moins de 2 500 FCFA la centaine montrent
une intention d'achat plus forte, ce qui suggère qu'un prix d'entrée compétitif
autour de **2 500 à 3 500 FCFA** maximiserait l'adoption initiale.

---

## 4. Analyse avancée

### a) Profils de clients identifiés

**Segment B — Client moyen (54 répondants, 43.9%)**
- Budget mensuel moyen : ~11 889 FCFA
- Prix centaine moyen actuel : ~8 694 FCFA
- 53.7% d'intention d'achat positive
- Préfèrent majoritairement les emballages jetables

**Segment C — Petit client (69 répondants, 56.1%)**
- Budget mensuel moyen : ~5 152 FCFA
- Prix centaine moyen actuel : ~3 761 FCFA
- Plus sensibles au prix, moins enclins à payer plus cher

### b) Caractéristiques des produits les plus demandés
Parmi les répondants ayant une intention d'achat positive :
- Compartiments : *"2 compartiments, 3 compartiments"*
- Contenance préférée : **850ML**
- Matériau préféré : **Carton**
- Fréquence de livraison : **Hebdomadairement**

### c) Segmentation — Méthode utilisée
**Méthode : segmentation par règles métier**

La segmentation a été réalisée à partir de trois critères :
1. **Quantité journalière** utilisée (proxy du volume d'achat)
2. **Budget mensuel** disponible
3. **Disposition à payer plus cher** que le prix actuel

Cette méthode a été choisie car elle est directement interprétable, cohérente avec les données
d'enquête disponibles, et ne nécessite pas de normalisation complexe des variables. Elle produit
des segments actionnables du point de vue commercial.

---

## 5. Recommandations stratégiques

### Produit
- Proposer en priorité des emballages **multi-compartiments (1 à 3 compartiments)**,
  en **carton ou bioplastique**, avec **fenêtre transparente**.
- La contenance cible est **850 ML** pour 1 compartiment, **800 ML** pour 2 compartiments.
- Prévoir une gamme **papier carton dur** (plébiscitée par les acheteurs potentiels).

### Politique de prix
- Le prix de référence actuel est de **3500 FCFA la centaine**.
- Positionner le produit entre **3 000 et 4 000 FCFA la centaine** pour rester compétitif
  tout en dégageant une marge.
- Le budget mensuel médian de **7000 FCFA** confirme qu'un prix trop élevé
  exclurait une majorité des répondants.
- Les 36.6% prêts à payer plus constituent le segment prioritaire à cibler
  pour une gamme premium.

### Approvisionnement
- Privilégier la **distribution locale** (56.1% des répondants le préfèrent).
- Cadence de livraison **hebdomadaire** recommandée (fréquence la plus souhaitée).
- Proposer des commandes en ligne en complément pour les clients plus connectés.
