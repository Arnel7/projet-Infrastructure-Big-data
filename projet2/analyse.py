import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml import Pipeline

spark = SparkSession.builder \
    .appName("RetailSale_Analyse") \
    .config("spark.driver.memory", "4g") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

sns.set_theme(style="whitegrid", palette="Set2")
plt.rcParams["figure.dpi"] = 120

df = spark.read.parquet("donnees_nettoyees.parquet")

print(f"Lignes chargées : {df.count()}")

# 1. STATISTIQUES DESCRIPTIVES

print("\n=== Stats globales ===")
df.select("sales", "revenu_calcule", "stock", "price").describe().show()

print("=== Stats par produit (top 10 ventes) ===")
df.groupBy("product_id").agg(
    F.sum("sales").alias("total_ventes"),
    F.sum("revenu_calcule").alias("total_revenu"),
    F.avg("price").alias("prix_moyen")
).orderBy(F.desc("total_ventes")).show(10)

print("=== Stats par magasin (top 10) ===")
df.groupBy("store_id").agg(
    F.sum("sales").alias("total_ventes"),
    F.sum("revenu_calcule").alias("total_revenu")
).orderBy(F.desc("total_ventes")).show(10)

print("=== Impact promotions ===")
df.groupBy("en_promotion").agg(
    F.count("*").alias("nb_lignes"),
    F.avg("sales").alias("ventes_moyennes"),
    F.sum("revenu_calcule").alias("revenu_total")
).orderBy("en_promotion").show()

# 2. VENTES PAR PRODUIT

top_produits = df.groupBy("product_id").agg(
    F.sum("sales").alias("total_ventes"),
    F.sum("revenu_calcule").alias("total_revenu")
).orderBy(F.desc("total_ventes")).limit(15).toPandas()

plt.figure(figsize=(12, 5))
plt.bar(top_produits["product_id"], top_produits["total_ventes"], color=sns.color_palette("Set2", 15))
plt.title("Top 15 produits par volume de ventes")
plt.xlabel("Produit")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("graphiques/01_ventes_par_produit.png")
plt.close()

plt.figure(figsize=(12, 5))
plt.bar(top_produits["product_id"], top_produits["total_revenu"], color=sns.color_palette("Set3", 15))
plt.title("Top 15 produits par revenu total")
plt.xlabel("Produit")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("graphiques/02_revenu_par_produit.png")
plt.close()

# 3. VENTES PAR MAGASIN

top_magasins = df.groupBy("store_id").agg(
    F.sum("sales").alias("total_ventes"),
    F.sum("revenu_calcule").alias("total_revenu")
).orderBy(F.desc("total_ventes")).limit(15).toPandas()

plt.figure(figsize=(12, 5))
plt.bar(top_magasins["store_id"], top_magasins["total_ventes"], color=sns.color_palette("Paired", 15))
plt.title("Top 15 magasins par volume de ventes")
plt.xlabel("Magasin")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("graphiques/03_ventes_par_magasin.png")
plt.close()

# 4. ÉVOLUTION TEMPORELLE

evolution = df.groupBy("annee", "mois").agg(
    F.sum("sales").alias("total_ventes"),
    F.sum("revenu_calcule").alias("total_revenu")
).orderBy("annee", "mois").toPandas()

evolution["periode"] = evolution["annee"].astype(str) + "-" + evolution["mois"].astype(str).str.zfill(2)

plt.figure(figsize=(14, 5))
plt.plot(evolution["periode"], evolution["total_ventes"], marker="o", color="steelblue")
plt.title("Évolution mensuelle des ventes")
plt.xlabel("Période")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("graphiques/04_evolution_ventes.png")
plt.close()

plt.figure(figsize=(14, 5))
plt.plot(evolution["periode"], evolution["total_revenu"], marker="o", color="coral")
plt.title("Évolution mensuelle des revenus")
plt.xlabel("Période")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("graphiques/05_evolution_revenu.png")
plt.close()

# 5. REVENUS CUMULÉS

evolution["revenu_cumule"] = evolution["total_revenu"].cumsum()
plt.figure(figsize=(14, 5))
plt.fill_between(evolution["periode"], evolution["revenu_cumule"], alpha=0.4, color="teal")
plt.plot(evolution["periode"], evolution["revenu_cumule"], color="teal")
plt.title("Revenus cumulés dans le temps")
plt.xlabel("Période")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("graphiques/06_revenu_cumule.png")
plt.close()

# 6. IMPACT DES PROMOTIONS

promo = df.groupBy("en_promotion").agg(
    F.avg("sales").alias("ventes_moyennes"),
    F.sum("revenu_calcule").alias("revenu_total")
).toPandas()

promo["label"] = promo["en_promotion"].map({0: "Sans promo", 1: "Avec promo"})

fig, axes = plt.subplots(1, 2, figsize=(10, 4))
axes[0].bar(promo["label"], promo["ventes_moyennes"], color=["#e74c3c", "#2ecc71"])
axes[0].set_title("Ventes moyennes selon promotion")
axes[1].bar(promo["label"], promo["revenu_total"], color=["#e74c3c", "#2ecc71"])
axes[1].set_title("Revenu total selon promotion")
plt.tight_layout()
plt.savefig("graphiques/07_impact_promotions.png")
plt.close()

# 7. RELATION PRIX → VENTES

prix_ventes = df.groupBy("price").agg(
    F.avg("sales").alias("ventes_moyennes")
).orderBy("price").toPandas()

plt.figure(figsize=(10, 5))
plt.scatter(prix_ventes["price"], prix_ventes["ventes_moyennes"], alpha=0.5, color="steelblue", s=20)
plt.title("Relation prix → volume de ventes moyen")
plt.xlabel("Prix")
plt.ylabel("Ventes moyennes")
plt.tight_layout()
plt.savefig("graphiques/08_prix_vs_ventes.png")
plt.close()

# 8. DISTRIBUTION DES VENTES ET STOCKS

sample = df.filter(F.col("sales") > 0).sample(fraction=0.05, seed=42).select("sales", "stock", "price").toPandas()

fig, axes = plt.subplots(1, 3, figsize=(15, 4))
sns.histplot(sample["sales"], bins=30, kde=True, ax=axes[0], color="steelblue")
axes[0].set_title("Distribution des ventes (>0)")
sns.histplot(sample["stock"], bins=30, kde=True, ax=axes[1], color="coral")
axes[1].set_title("Distribution des stocks")
sns.histplot(sample["price"], bins=30, kde=True, ax=axes[2], color="green")
axes[2].set_title("Distribution des prix")
plt.tight_layout()
plt.savefig("graphiques/09_distributions.png")
plt.close()

# 9. CORRÉLATIONS

corr_pd = sample[["sales", "stock", "price"]].corr()
plt.figure(figsize=(6, 5))
sns.heatmap(corr_pd, annot=True, fmt=".2f", cmap="coolwarm", center=0)
plt.title("Corrélations entre variables numériques")
plt.tight_layout()
plt.savefig("graphiques/10_correlations.png")
plt.close()

print("\n=== Corrélations Spark ===")
for col_a, col_b in [("sales", "price"), ("sales", "stock"), ("price", "stock"), ("sales", "en_promotion")]:
    try:
        r = df.stat.corr(col_a, col_b)
        print(f"  corr({col_a}, {col_b}) = {r:.4f}")
    except Exception:
        print(f"  corr({col_a}, {col_b}) = non calculable (variance nulle)")

# 10. MODÈLE : RÉGRESSION LINÉAIRE (prédiction des ventes)

df_model = df.select("sales", "price", "stock", "en_promotion") \
    .filter(F.col("sales").isNotNull()) \
    .filter(F.col("price").isNotNull())

assembleur = VectorAssembler(
    inputCols=["price", "stock", "en_promotion"],
    outputCol="features"
)

train, test = df_model.randomSplit([0.8, 0.2], seed=42)

modele = LinearRegression(featuresCol="features", labelCol="sales", maxIter=10)

pipeline = Pipeline(stages=[assembleur, modele])
pipeline_entraine = pipeline.fit(train)

predictions = pipeline_entraine.transform(test)

evaluateur_rmse = RegressionEvaluator(labelCol="sales", predictionCol="prediction", metricName="rmse")
evaluateur_mae = RegressionEvaluator(labelCol="sales", predictionCol="prediction", metricName="mae")
evaluateur_r2 = RegressionEvaluator(labelCol="sales", predictionCol="prediction", metricName="r2")

rmse = evaluateur_rmse.evaluate(predictions)
mae = evaluateur_mae.evaluate(predictions)
r2 = evaluateur_r2.evaluate(predictions)

modele_lr = pipeline_entraine.stages[-1]
coefficients = dict(zip(["price", "stock", "en_promotion"], modele_lr.coefficients.toArray()))

print("\n=== Résultats du modèle — Régression linéaire ===")
print(f"  RMSE  : {rmse:.4f}")
print(f"  MAE   : {mae:.4f}")
print(f"  R²    : {r2:.4f}")
print(f"  Coefficients : {coefficients}")

pred_pd = predictions.select("sales", "prediction").limit(200).toPandas()
plt.figure(figsize=(8, 5))
plt.scatter(pred_pd["sales"], pred_pd["prediction"], alpha=0.4, color="purple", s=15)
plt.plot([0, pred_pd["sales"].max()], [0, pred_pd["sales"].max()], "r--")
plt.title("Valeurs réelles vs prédites (régression linéaire)")
plt.xlabel("Ventes réelles")
plt.ylabel("Ventes prédites")
plt.tight_layout()
plt.savefig("graphiques/11_reel_vs_predit.png")
plt.close()

print("\nTous les graphiques dans 'graphiques/'")

spark.stop()
