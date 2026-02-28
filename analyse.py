import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import numpy as np
import warnings
warnings.filterwarnings("ignore")

matplotlib.rcParams["figure.dpi"] = 120
sns.set_theme(style="whitegrid", palette="Set2")

df = pd.read_csv("donnees_nettoyees.csv")

activites = df["activite"].value_counts().head(15)
plt.figure(figsize=(10, 5))
activites.plot(kind="barh", color=sns.color_palette("Set2", len(activites)))
plt.title("Types d'activités des répondants")
plt.xlabel("Nombre de répondants")
plt.tight_layout()
plt.savefig("graphiques/01_activites.png")
plt.close()

plt.figure(figsize=(5, 5))
df["utilise_emballage"].value_counts().plot(kind="pie", autopct="%1.1f%%", startangle=90)
plt.title("Utilisez-vous des emballages alimentaires jetables ?")
plt.ylabel("")
plt.tight_layout()
plt.savefig("graphiques/02_utilisation_emballage.png")
plt.close()

ordre_quantite = ["1-10", "10-30", "30-50", "50-100", "100+"]
quantites = df["quantite_par_jour"].value_counts().reindex(ordre_quantite).dropna()
plt.figure(figsize=(7, 4))
quantites.plot(kind="bar", color=sns.color_palette("Set2", len(quantites)))
plt.title("Quantité d'emballages utilisée par jour")
plt.xlabel("Tranche")
plt.ylabel("Nombre de répondants")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("graphiques/03_quantite_par_jour.png")
plt.close()

plt.figure(figsize=(6, 4))
df["preference_type"].value_counts().plot(kind="bar", color=sns.color_palette("Pastel1"))
plt.title("Préférence : jetable ou réutilisable ?")
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig("graphiques/04_preference_type.png")
plt.close()

plt.figure(figsize=(8, 4))
df["nb_compartiments"].value_counts().plot(kind="bar", color=sns.color_palette("Set3"))
plt.title("Nombre de compartiments préférés")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("graphiques/05_nb_compartiments.png")
plt.close()

plt.figure(figsize=(5, 5))
df["fenetre_transparente"].value_counts().plot(kind="pie", autopct="%1.1f%%", startangle=90)
plt.title("Préférence pour fenêtre transparente")
plt.ylabel("")
plt.tight_layout()
plt.savefig("graphiques/06_fenetre_transparente.png")
plt.close()

contenances_1 = df["contenance_1comp"].value_counts().head(10)
plt.figure(figsize=(7, 4))
contenances_1.plot(kind="bar", color=sns.color_palette("Set2"))
plt.title("Contenances préférées (1 compartiment)")
plt.xlabel("Contenance")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("graphiques/07_contenance_1comp.png")
plt.close()

plt.figure(figsize=(8, 4))
df["echantillon_prefere"].value_counts().plot(kind="bar", color=sns.color_palette("Paired"))
plt.title("Échantillon préféré")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("graphiques/08_echantillon_prefere.png")
plt.close()

budget_propre = df["budget_mensuel"].dropna()
plt.figure(figsize=(8, 4))
sns.histplot(budget_propre, bins=15, kde=True, color="steelblue")
plt.title("Distribution du budget mensuel (FCFA)")
plt.xlabel("Budget mensuel (FCFA)")
plt.tight_layout()
plt.savefig("graphiques/09_budget_mensuel.png")
plt.close()

prix_propre = df["prix_centaine_actuel"].dropna()
plt.figure(figsize=(8, 4))
sns.histplot(prix_propre, bins=12, kde=True, color="coral")
plt.title("Prix actuel pour la centaine de plats (FCFA)")
plt.xlabel("Prix (FCFA)")
plt.tight_layout()
plt.savefig("graphiques/10_prix_centaine.png")
plt.close()

plt.figure(figsize=(6, 4))
df["achat_meme_plus_cher"].value_counts().plot(kind="bar", color=sns.color_palette("Set1"))
plt.title("Achèteraient même si légèrement plus cher ?")
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig("graphiques/11_achat_plus_cher.png")
plt.close()

plt.figure(figsize=(5, 5))
df["intention_achat"].value_counts().plot(
    kind="pie", autopct="%1.1f%%", startangle=90,
    colors=sns.color_palette("Set2")
)
plt.title("Intention d'achat")
plt.ylabel("")
plt.tight_layout()
plt.savefig("graphiques/12_intention_achat.png")
plt.close()

plt.figure(figsize=(7, 4))
df["frequence_livraison"].value_counts().plot(kind="bar", color=sns.color_palette("tab10"))
plt.title("Fréquence de livraison souhaitée")
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig("graphiques/13_frequence_livraison.png")
plt.close()

plt.figure(figsize=(7, 4))
df["mode_approvisionnement"].value_counts().plot(kind="bar", color=sns.color_palette("pastel"))
plt.title("Mode d'approvisionnement préféré")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("graphiques/14_mode_approvisionnement.png")
plt.close()

tous_materiaux = df["materiaux"].dropna().str.split(",").explode().str.strip()
plt.figure(figsize=(8, 4))
tous_materiaux.value_counts().plot(kind="bar", color=sns.color_palette("Set2"))
plt.title("Matériaux d'emballage préférés")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("graphiques/15_materiaux.png")
plt.close()

tranches_prix = [0, 2500, 5000, 8000, 15000, 100000]
etiquettes_prix = ["<2500", "2500-5000", "5000-8000", "8000-15000", ">15000"]
df["tranche_prix"] = pd.cut(df["prix_centaine_actuel"], bins=tranches_prix, labels=etiquettes_prix)

prob_achat = df.groupby("tranche_prix", observed=True).apply(
    lambda x: round((x["intention_achat"] == "Oui").sum() / len(x) * 100, 1)
).reset_index()
prob_achat.columns = ["tranche_prix", "pct_intention_oui"]

plt.figure(figsize=(8, 4))
plt.bar(prob_achat["tranche_prix"].astype(str), prob_achat["pct_intention_oui"],
        color=sns.color_palette("coolwarm", len(prob_achat)))
plt.title("Probabilité d'achat selon le prix actuel payé (centaine de plats)")
plt.xlabel("Prix actuel (FCFA)")
plt.ylabel("% d'intention d'achat positive")
plt.ylim(0, 100)
for i, val in enumerate(prob_achat["pct_intention_oui"]):
    plt.text(i, val + 1, f"{val}%", ha="center", fontsize=9)
plt.tight_layout()
plt.savefig("graphiques/18_prix_vs_intention_achat.png")
plt.close()

tous_criteres = pd.concat([
    df["caracteristique_1"],
    df["caracteristique_2"],
    df["autres_criteres"]
]).dropna().str.strip()
tous_criteres = tous_criteres[tous_criteres.str.lower() != "ras"]
tous_criteres = tous_criteres[tous_criteres.str.lower() != "non"]

plt.figure(figsize=(9, 5))
tous_criteres.value_counts().head(12).sort_values().plot(kind="barh", color=sns.color_palette("Set2", 12))
plt.title("Principaux critères de choix des emballages")
plt.xlabel("Nombre de mentions")
plt.tight_layout()
plt.savefig("graphiques/19_criteres_choix.png")
plt.close()

acheteurs = df[df["intention_achat"] == "Oui"]

print("\n=== Produits les plus demandés (acheteurs potentiels) ===")
print("Compartiments:")
print(acheteurs["nb_compartiments"].value_counts().head(5).to_string())
print("\nContenance 1 compartiment:")
print(acheteurs["contenance_1comp"].value_counts().head(5).to_string())
print("\nMatériaux:")
print(acheteurs["materiaux"].str.split(",").explode().str.strip().value_counts().head(5).to_string())
print("\nFenêtre transparente:")
print(acheteurs["fenetre_transparente"].value_counts().to_string())
print("\nFréquence livraison:")
print(acheteurs["frequence_livraison"].value_counts().to_string())

fig, axes = plt.subplots(1, 3, figsize=(15, 5))
acheteurs["nb_compartiments"].value_counts().head(5).plot(kind="bar", ax=axes[0], color=sns.color_palette("Set2"))
axes[0].set_title("Compartiments (acheteurs)")
axes[0].tick_params(axis="x", rotation=30)

acheteurs["contenance_1comp"].value_counts().head(6).plot(kind="bar", ax=axes[1], color=sns.color_palette("Set3"))
axes[1].set_title("Contenance préférée (acheteurs)")
axes[1].tick_params(axis="x", rotation=30)

acheteurs["materiaux"].str.split(",").explode().str.strip().value_counts().head(5).plot(
    kind="bar", ax=axes[2], color=sns.color_palette("Paired"))
axes[2].set_title("Matériaux préférés (acheteurs)")
axes[2].tick_params(axis="x", rotation=30)
plt.tight_layout()
plt.savefig("graphiques/20_produits_plus_demandes.png")
plt.close()

def attribuer_segment(ligne):
    score_quantite = 0
    if ligne["quantite_par_jour"] in ["50-100", "100+"]:
        score_quantite = 2
    elif ligne["quantite_par_jour"] in ["10-30", "30-50"]:
        score_quantite = 1

    score_budget = 0
    if pd.notna(ligne["budget_mensuel"]):
        if ligne["budget_mensuel"] >= 20000:
            score_budget = 2
        elif ligne["budget_mensuel"] >= 8000:
            score_budget = 1

    score_prix = 1 if str(ligne["achat_meme_plus_cher"]).strip() == "Oui" else 0
    score_total = score_quantite + score_budget + score_prix

    if score_total >= 4:
        return "A - Gros client"
    elif score_total >= 2:
        return "B - Client moyen"
    else:
        return "C - Petit client"

df["segment"] = df.apply(attribuer_segment, axis=1)

plt.figure(figsize=(6, 4))
df["segment"].value_counts().plot(kind="bar", color=["#2ecc71", "#3498db", "#e74c3c"])
plt.title("Répartition des segments clients")
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig("graphiques/16_segmentation.png")
plt.close()

profil = df.groupby("segment").agg(
    nombre=("segment", "count"),
    budget_moyen=("budget_mensuel", "mean"),
    prix_moyen_centaine=("prix_centaine_actuel", "mean"),
    pct_intention_oui=("intention_achat", lambda x: round((x == "Oui").sum() / len(x) * 100, 1)),
    pct_prefere_jetable=("preference_type", lambda x: round((x == "Jetable").sum() / len(x) * 100, 1)),
).round(0)

print("\n=== Profil des segments clients ===")
print(profil.to_string())

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
profil["budget_moyen"].plot(kind="bar", ax=axes[0], color=["#2ecc71", "#3498db", "#e74c3c"])
axes[0].set_title("Budget mensuel moyen par segment (FCFA)")
axes[0].set_xticklabels(profil.index, rotation=15)

profil["pct_intention_oui"].plot(kind="bar", ax=axes[1], color=["#2ecc71", "#3498db", "#e74c3c"])
axes[1].set_title("% d'intention d'achat positive par segment")
axes[1].set_ylabel("%")
axes[1].set_xticklabels(profil.index, rotation=15)
plt.tight_layout()
plt.savefig("graphiques/17_profil_segments.png")
plt.close()

print("\n=== SYNTHÈSE DE L'ENQUÊTE ===")
print(f"Répondants totaux : {len(df)}")
print(f"Utilisent déjà des emballages jetables : {(df['utilise_emballage'] == 'Oui').sum()} ({(df['utilise_emballage'] == 'Oui').mean()*100:.1f}%)")
print(f"Intention d'achat positive (Oui) : {(df['intention_achat'] == 'Oui').sum()} ({(df['intention_achat'] == 'Oui').mean()*100:.1f}%)")
print(f"Budget mensuel médian : {df['budget_mensuel'].median():.0f} FCFA")
print(f"Prix centaine médian actuel : {df['prix_centaine_actuel'].median():.0f} FCFA")
print(f"Fréquence livraison la plus souhaitée : {df['frequence_livraison'].value_counts().idxmax()}")
print(f"Mode approvisionnement préféré : {df['mode_approvisionnement'].value_counts().idxmax()}")

df.to_csv("donnees_segmentees.csv", index=False)
print("\nTous les graphiques sont dans 'graphiques/'")
print("Données finales dans 'donnees_segmentees.csv'")
