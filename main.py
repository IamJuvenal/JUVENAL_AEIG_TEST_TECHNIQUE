# main.py

import json
from datetime import datetime
from collect.google_news import collect_articles, set_period
from storage.csv_writer import append_to_csv


def load_config():
    """Charge les paramètres depuis le fichier config.json"""
    with open("config.json", "r", encoding="utf-8") as f:
        return json.load(f)


def choisir_periode():
    """Affiche un menu pour que l'utilisateur sélectionne une période de veille"""
    print("\nChoisissez une période de recherche :")
    print("1 - Dernières 24h")
    print("2 - Dernières 48h")
    print("3 - Dernières 72h")
    print("4 - Dernière semaine")
    print("5 - Dernier mois")
    print("6 - Dernier trimestre")
    print("7 - Dernière année")
    print("8 - Définir manuellement la période (format : aaaa-mm-jj hh:mm)")

    choix = input("Entrez le numéro correspondant à votre choix : ")

    periodes = {
        "1": "1d",
        "2": "2d",
        "3": "3d",
        "4": "7d",
        "5": "30d",
        "6": "90d",
        "7": "365d"
    }

    if choix in periodes:
        return {"period": periodes[choix]}
    elif choix == "8":
        debut = input("Date de début (aaaa-mm-jj hh:mm) : ")
        fin = input("Date de fin   (aaaa-mm-jj hh:mm) : ")
        try:
            start = datetime.strptime(debut, "%Y-%m-%d %H:%M")
            end = datetime.strptime(fin, "%Y-%m-%d %H:%M")
            return {"custom": True, "start_date": start, "end_date": end}
        except ValueError:
            print("Format invalide. Format attendu : aaaa-mm-jj hh:mm")
            print("Reprise avec la période par défaut (7 jours).")
            return {"period": "7d"}
    else:
        print("Choix invalide. Période par défaut appliquée (7 jours).")
        return {"period": "7d"}


def lancer_pipeline_de_veille():
    """Exécute le pipeline de veille : chargement config, collecte, sauvegarde CSV"""
    config = load_config()
    sujets = config["topics"]
    csv_file = config.get("csv_file", "veille_resultats.csv")
    all_results = []

    # Choix de la période
    periode = choisir_periode()
    set_period(periode)

    # Collecte pour chaque sujet
    for sujet in sujets:
        print(f"Collecte pour le sujet : {sujet}")
        articles = collect_articles(sujet)
        all_results.extend(articles)

    # Sauvegarde des résultats
    append_to_csv(all_results, csv_file)
    print("Veille terminée.")


if __name__ == "__main__":
    lancer_pipeline_de_veille()
