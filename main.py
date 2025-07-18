from init_config import initialiser_config
from collect.collecter_articles import collecter_articles
from collect.collecter_posts import collecter_posts
from storage.csv_writer import append_to_csv
import json
import os


def charger_resultats_temporaires(nom_fichier):
    try:
        with open(nom_fichier, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"⚠️  Aucun fichier {nom_fichier} trouvé.")
        return []


def lancer_pipeline_de_veille():
    # Étape 1 : configuration utilisateur
    initialiser_config()

    # Étape 2 : lecture de la configuration
    with open("config.json", "r", encoding="utf-8") as f:
        config = json.load(f)

    # Étape 3 : collecte
    if config["content_types"].get("articles", 0) > 0:
        collecter_articles()

    if config["content_types"].get("posts", 0) > 0:
        collecter_posts()

    # Étape 4 : chargement des résultats et écriture CSV
    tous_resultats = []

    if config["content_types"].get("articles", 0) > 0:
        articles = charger_resultats_temporaires("articles_collectes.json")
        tous_resultats.extend(articles)
        print(f"✅ {len(articles)} articles ajoutés.")

    if config["content_types"].get("posts", 0) > 0:
        posts = charger_resultats_temporaires("posts_collectes.json")
        tous_resultats.extend(posts)
        print(f"✅ {len(posts)} posts ajoutés.")

    if tous_resultats:
        append_to_csv(tous_resultats, "veille_resultats.csv")
        print("✅ Résultats sauvegardés dans veille_resultats.csv")
    else:
        print("❌ Aucun contenu à sauvegarder.")


if __name__ == "__main__":
    lancer_pipeline_de_veille()
