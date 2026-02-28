from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import IntegerType, FloatType, DateType

spark = SparkSession.builder \
    .appName("RetailSale_Nettoyage") \
    .config("spark.driver.memory", "4g") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

df = spark.read.csv("retailsale.csv", header=True, inferSchema=True)

print("=== Schéma ===")
df.printSchema()
print(f"Lignes : {df.count()} | Colonnes : {len(df.columns)}")

print("\n=== NaN par colonne ===")
for col in df.columns:
    n = df.filter(F.col(col).isNull()).count()
    if n > 0:
        print(f"  {col}: {n} NaN")

print("\n=== Valeurs uniques par colonne ===")
for col in df.columns:
    print(f"  {col}: {df.select(col).distinct().count()} uniques")

print("\n=== Statistiques numériques ===")
df.select("sales", "revenue", "stock", "price").describe().show()

df = df.drop("promo_type_2")

df = df.withColumn(
    "promo_bin_1",
    F.when(F.col("promo_bin_1").isNull(), "Aucune").otherwise(F.col("promo_bin_1").cast("string"))
)

df = df.withColumn("date", F.to_date(F.col("date"), "M/d/yyyy"))

df = df.withColumn("sales", F.col("sales").cast(IntegerType()))
df = df.withColumn("stock", F.col("stock").cast(IntegerType()))
df = df.withColumn("price", F.col("price").cast(FloatType()))

df = df.withColumn("revenu_calcule", F.round(F.col("sales") * F.col("price"), 2))

df = df.withColumn("annee", F.year("date"))
df = df.withColumn("mois", F.month("date"))
df = df.withColumn("semaine", F.weekofyear("date"))

df = df.withColumn("en_promotion", F.when(F.col("promo_bin_1") == "Aucune", 0).otherwise(1))

print("\n=== Aperçu données nettoyées ===")
df.show(5, truncate=False)

print("\n=== NaN restants ===")
nan_restants = 0
for col in df.columns:
    n = df.filter(F.col(col).isNull()).count()
    if n > 0:
        print(f"  {col}: {n}")
        nan_restants += n
if nan_restants == 0:
    print("  Aucun NaN")

df = df.dropna(subset=["price", "stock", "sales", "promo_type_1"])
df = df.fillna({"revenue": 0.0, "revenu_calcule": 0.0})

df.write.mode("overwrite").parquet("donnees_nettoyees.parquet")
print("\nFichier 'donnees_nettoyees.parquet' sauvegardé.")

spark.stop()
