import pandas as pd
import re

CHEMIN_FICHIER = "../Projet_Big_data_2026_pigier/enquête.xlsx"

donnees_brutes = pd.read_excel(CHEMIN_FICHIER)

nouvelles_colonnes = {
    "Code de l'agent recenseur": "agent",
    "Date du Recencement": "date",
    "Que vendez-vous principalement ?": "activite",
    "Utilisez vous des  emballages alimentaires ( plats à jeter) ?": "utilise_emballage",
    "Combien d' emballages alimentaires  à jeter utilisez-vous en moyenne par jour ?": "quantite_par_jour",
    "Quels sont les principaux objectifs que vous recherchez avec les  emballages alimentaires  utilisés? ": "objectifs",
    "Préférez-vous des emballages alimentaires jetables ou réutilisables pour votre établissement ?": "preference_type",
    "À quelle fréquence aimeriez-vous recevoir des livraisons d'emballages alimentaires (quotidiennement, hebdomadairement, mensuellement, etc.) ?": "frequence_livraison",
    "Quelles caractéristiques spécifiques recherchez-vous dans un emballage alimentaire (par exemple, résistance à la chaleur, étanchéité, facilité d'ouverture, etc.) ? [1]": "caracteristique_1",
    "Quelles caractéristiques spécifiques recherchez-vous dans un emballage alimentaire (par exemple, résistance à la chaleur, étanchéité, facilité d'ouverture, etc.) ? [2]": "caracteristique_2",
    "Quel est votre budget approximatif pour les emballages alimentaires par mois ?": "budget_mensuel",
    "Comment préférez-vous être approvisionné en emballages alimentaires (commande en ligne, distribution locale, etc.) ?": "mode_approvisionnement",
    "Quels types de matériaux d'emballage privilégiez-vous (plastique, carton, bioplastiques, etc.) ?": "materiaux",
    "Avez-vous des besoins spécifiques en termes de tailles d'emballages (petit, moyen, grand, etc.) ?": "taille_emballage",
    " Vous voulez des  emballages alimentaires avec combien de compartilment": "nb_compartiments",
    "Préférez-vous des emballages avec des fenêtres transparentes pour montrer les produits ?": "fenetre_transparente",
    "Pouvez vous nous montrerles emballages que vous avez déjà?": "photo_url",
    "Quelle contenance préférez-vous? [1 Compartiment]": "contenance_1comp",
    "Quelle contenance préférez-vous? [2 Compartiments]": "contenance_2comp",
    "Quelle contenance préférez-vous? [3 Compartiments]": "contenance_3comp",
    "Quelle contenance préférez-vous? [4 Compartiments]": "contenance_4comp",
    "Lequel des echantillons préférez-vous": "echantillon_prefere",
    "Acheteriez vous ces plats si on vous en apporte ?": "intention_achat",
    "A combien vous reviens la centaine des plats que vous utiliser actuellement?": "prix_centaine_actuel",
    "Allez-vous acheter nos  emballages alimentaires   meme si cela coute légèrement plus cher que ce que vous utilisez en ce moment ?": "achat_meme_plus_cher",
    "Y a-t-il des contraintes légales ou normatives concernant les emballages alimentaires que vous devez respecter ?": "contraintes_legales",
    "Quels autres critères sont importants pour vous lors du choix de vos emballages alimentaires ?": "autres_criteres",
    "Avez-vous d'autres commentaires ou besoins spécifiques que vous aimeriez partager avec nous ?": "commentaires",
    "Avez-vous des suggestions pour  l'entreprise qui veut commercialiser les plats jetables?": "suggestions",
}

df = donnees_brutes.rename(columns=nouvelles_colonnes)
df = df.drop(columns=["photo_url"])

def extraire_montant(valeur):
    if pd.isna(valeur):
        return None
    texte = str(valeur).strip().lower()
    if texte in ("ras", "non", "-", ""):
        return None
    contient_mille = "mille" in texte
    texte_propre = (texte
        .replace("milles", "").replace("mille", "")
        .replace("fcfa", "").replace("cfa", "").replace("f", "")
        .replace(".", "").replace(",", "").replace(" ", "")
    )
    nombres = [float(n) for n in re.findall(r'\d+', texte_propre)]
    if not nombres:
        return None
    milieu = (nombres[0] + nombres[1]) / 2 if len(nombres) >= 2 else nombres[0]
    if contient_mille:
        milieu *= 1000
    return milieu

df["budget_mensuel"] = df["budget_mensuel"].apply(extraire_montant)
df["prix_centaine_actuel"] = df["prix_centaine_actuel"].apply(extraire_montant)

df["budget_mensuel"] = df["budget_mensuel"].fillna(df["budget_mensuel"].median())
df["prix_centaine_actuel"] = df["prix_centaine_actuel"].fillna(df["prix_centaine_actuel"].median())

colonnes_texte = df.select_dtypes(include="str").columns
for col in colonnes_texte:
    df[col] = df[col].str.strip()

df["utilise_emballage"] = df["utilise_emballage"].str.capitalize()
df["preference_type"] = df["preference_type"].str.capitalize()
df["fenetre_transparente"] = df["fenetre_transparente"].str.capitalize()
df["achat_meme_plus_cher"] = df["achat_meme_plus_cher"].str.capitalize()

df["intention_achat"] = df["intention_achat"].str.capitalize().replace({
    "Peut être": "Peut-être",
    "Peut  être": "Peut-être",
    "Je ne sais pas": "Peut-être",
})

df["date"] = pd.to_datetime(df["date"], errors="coerce")

def harmoniser_frequence(val):
    if pd.isna(val):
        return None
    v = str(val).strip().lower()
    if "quot" in v:
        return "Quotidiennement"
    if "hebdo" in v or "semain" in v:
        return "Hebdomadairement"
    if "mens" in v or "mois" in v:
        return "Mensuellement"
    if "besoin" in v or "command" in v:
        return "À la demande"
    return val.strip()

df["frequence_livraison"] = df["frequence_livraison"].apply(harmoniser_frequence)

def harmoniser_quantite(val):
    if pd.isna(val):
        return None
    v = str(val).strip().lower()
    if "1 et 10" in v or "1-10" in v or "1-15" in v or "1 et 15" in v:
        return "1-10"
    if "1 et 30" in v or "10 et 30" in v or "15 et 30" in v or "10-30" in v:
        return "10-30"
    if "30 et 50" in v or "31 et 50" in v or "30-50" in v:
        return "30-50"
    if "50 et 100" in v or "51" in v or "50-100" in v:
        return "50-100"
    if "100" in v or "plus de 100" in v:
        return "100+"
    return val.strip()

df["quantite_par_jour"] = df["quantite_par_jour"].apply(harmoniser_quantite)

df = df.drop(columns=["budget_mensuel_num", "prix_centaine_num"], errors="ignore")

for col in ["contenance_1comp", "contenance_2comp", "contenance_3comp", "contenance_4comp"]:
    df[col] = df[col].fillna("Non précisé")

df["suggestions"] = df["suggestions"].fillna("Aucune")

print("=== Valeurs manquantes par colonne ===")
manquantes = df.isnull().sum()
print(manquantes[manquantes > 0])
print(f"\nNombre de répondants : {len(df)}")
print(f"Nombre de colonnes : {len(df.columns)}")

df.to_csv("donnees_nettoyees.csv", index=False)
print("\nFichier 'donnees_nettoyees.csv' sauvegardé.")
