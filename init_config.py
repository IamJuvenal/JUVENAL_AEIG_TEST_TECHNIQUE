# init_config.py

import json
from datetime import datetime, timedelta


def demander_periode():
    while True:
        print("\nChoisissez une période de temps : (Saisissez un chiffre)")
        print("1. Dernières 24h")
        print("2. Dernières 48h")
        print("3. Dernières 72h")
        print("4. Cette semaine")
        print("5. Ce mois")
        print("6. Ce trimestre")
        print("7. Cette année")
        print("8. Période personnalisée (format : YYYY-MM-DD HH:MM)")

        choix = input("→ ").strip()
        now = datetime.now()

        if choix == "1":
            return now - timedelta(hours=24), now
        elif choix == "2":
            return now - timedelta(hours=48), now
        elif choix == "3":
            return now - timedelta(hours=72), now
        elif choix == "4":
            return now - timedelta(days=7), now
        elif choix == "5":
            return now - timedelta(days=30), now
        elif choix == "6":
            return now - timedelta(days=90), now
        elif choix == "7":
            return now - timedelta(days=365), now
        elif choix == "8":
            try:
                print("Date de début (YYYY-MM-DD HH:MM) :")
                début = datetime.strptime(input("→ ").strip(), "%Y-%m-%d %H:%M")
                print("Date de fin (YYYY-MM-DD HH:MM) :")
                fin = datetime.strptime(input("→ ").strip(), "%Y-%m-%d %H:%M")
                return début, fin
            except ValueError:
                print("Format invalide. Recommencez.")
        else:
            print("Choix invalide. Recommencez.")


def demander_types_de_contenus():
    mapping = {"1": "articles", "2": "posts", "3": "tweets"}

    while True:
        print("\nQuels types de contenus souhaitez-vous collecter ?")
        print("1. Articles")
        print("2. Posts")
        print("3. Tweets")
        print("Vous pouvez en sélectionner plusieurs (ex : 1,2,3)")

        choix = input("→ ").strip()
        selection = [mapping[c] for c in choix.split(",") if c.strip() in mapping]

        if not selection:
            print("Aucun type valide sélectionné. Veuillez choisir au moins un type.")
        else:
            break

    repartition = {}
    total = 0

    # Contenus sélectionnés : demander les % à l'utilisateur
    for c in mapping.values():
        if c in selection:
            try:
                pourcent = int(input(f"Pourcentage pour {c} : ").strip())
                repartition[c] = pourcent
                total += pourcent
            except ValueError:
                print(f"Entrée invalide pour {c}. On met 0%.")
                repartition[c] = 0
        else:
            repartition[c] = 0  # Non choisi = 0%

    # Ajustement automatique si total ≠ 100
    if total != 100:
        print("Les pourcentages donnés ne font pas 100%. Ajustement automatique...")

        sélectionnés = [k for k in selection]
        restant = 100
        repartition_corrigée = {}

        for i, k in enumerate(sélectionnés):
            if i == len(sélectionnés) - 1:
                repartition_corrigée[k] = restant
            else:
                part = (
                    round(100 * repartition[k] / total)
                    if total
                    else 100 // len(sélectionnés)
                )
                repartition_corrigée[k] = part
                restant -= part

        # Remet à 0 les types non sélectionnés
        for k in mapping.values():
            repartition[k] = repartition_corrigée.get(k, 0)

    return repartition


def demander_sources_articles():
    print(
        "\nSouhaitez-vous spécifier les sources à utiliser pour la collecte d’articles ?"
    )
    print("1. GNews")
    print("2. NewsAPI")
    print("3. Les deux (par défaut)")
    print("Appuyez sur Entrée sans rien taper pour sélectionner toutes les sources.")

    choix = input("→ ").strip()
    mapping = {"1": ["GNews"], "2": ["NewsAPI"], "3": ["GNews", "NewsAPI"]}

    return mapping.get(choix, ["GNews", "NewsAPI"])


def demander_nombre_de_resultats():
    while True:
        try:
            print("\nCombien de résultats souhaitez-vous collecter au total ?")
            nb = int(input("→ ").strip())
            if nb > 0:
                return nb
            else:
                print("Le nombre doit être supérieur à zéro.")
        except ValueError:
            print("Entrée invalide. Veuillez entrer un nombre entier.")


def demander_zones_geographiques():
    ZONES_LIBELLES = {
        "1": ("Afrique", "AFR"),
        "2": ("Afrique de l’Ouest", "AFO"),
        "3": ("Afrique du Nord", "AFN"),
        "4": ("Afrique de l’Est", "AFE"),
        "5": ("Afrique Centrale", "AFC"),
        "6": ("Afrique Australe", "AFS"),
        "7": ("Nigéria", "NG"),
        "8": ("Afrique du Sud", "ZA"),
        "9": ("Égypte", "EG"),
        "10": ("Algérie", "DZ"),
        "11": ("Bénin", "BJ"),
        "12": ("Europe", "EU"),
        "13": ("Europe de l’Ouest", "EO"),
        "14": ("Europe du Nord", "EN"),
        "15": ("Europe du Sud", "ES"),
        "16": ("Europe de l’Est", "EE"),
        "17": ("France", "FR"),
        "18": ("Allemagne", "DE"),
        "19": ("Italie", "IT"),
        "20": ("Espagne", "ES"),
        "21": ("Royaume-Uni", "GB"),
        "22": ("Asie", "AS"),
        "23": ("Asie de l’Est", "AEO"),
        "24": ("Asie du Nord", "AEN"),
        "25": ("Asie du Sud", "AES"),
        "26": ("Asie Centrale", "AEC"),
        "27": ("Chine", "CN"),
        "28": ("Inde", "IN"),
        "29": ("Japon", "JP"),
        "30": ("Indonésie", "ID"),
        "31": ("Corée du Sud", "KR"),
        "32": ("Amériques", "AM"),
        "33": ("Amérique du Nord", "NA"),
        "34": ("Amérique Centrale", "CA"),
        "35": ("Caraïbes et Amérique du Sud", "CS"),
        "36": ("États-Unis", "US"),
        "37": ("Canada", "CA"),
        "38": ("Mexique", "MX"),
        "39": ("Brésil", "BR"),
        "40": ("Argentine", "AR"),
        "41": ("Océanie", "OC"),
        "42": ("Océanie du Nord", "ON"),
        "43": ("Océanie du Sud", "OCS"),
        "44": ("Australie", "AU"),
        "45": ("Nouvelle-Zélande", "NZ"),
        "46": ("Papouasie-Nouvelle-Guinée", "PG"),
        "47": ("Fidji", "FJ"),
        "48": ("Nouvelle-Calédonie", "NC"),
        "49": ("Antarctique", "ANT"),
    }

    while True:
        print("\nZones géographiques disponibles :")
        for num, (nom, _) in ZONES_LIBELLES.items():
            print(f"{num}. {nom}")

        print("\nChoisissez un ou plusieurs numéros séparés par des virgules.")
        print(
            "Vous pouvez aussi ajouter des codes ISO de pays non présents dans la liste."
        )
        print("Exemple : 7,9,BJ pour Nigéria, Égypte et Bénin.")
        print(
            "La liste complète des codes ISO des pays est disponible sur https://www.iban.com/country-codes et dans le fichier README du projet."
        )

        saisie = input("→ ").strip()
        choix = [x.strip().upper() for x in saisie.split(",") if x.strip()]
        codes_mixte = set()
        erreurs = []

        for item in choix:
            if item in ZONES_LIBELLES:
                codes_mixte.add(ZONES_LIBELLES[item][1])
            elif len(item) == 2 and item.isalpha():
                codes_mixte.add(item)
            else:
                erreurs.append(item)

        if erreurs:
            print(
                f"Entrées invalides détectées : {', '.join(erreurs)}. Veuillez réessayer."
            )
        elif not codes_mixte:
            print("Vous devez sélectionner au moins une zone ou un code ISO.")
        else:
            return list(codes_mixte)


def convertir_zones_en_pays(codes_mixte):
    """
    Convertit une liste de codes mélangés (codes ISO alpha-2 pour les pays et codes alpha-3 personnalisés pour les zones)
    en une liste de codes ISO alpha-2 de pays uniquement, sans doublons.

    Args:
        codes_mixte (list): Liste de codes (par ex. ['AO', 'FR', 'BJ'])

    Returns:
        list: Liste dédoublonnée de codes ISO alpha-2 correspondant aux pays uniquement.
    """

    ZONES_TO_PAYS = {
        "AFR": [  # Afrique
            "DZ",
            "AO",
            "BJ",
            "BW",
            "BF",
            "BI",
            "CM",
            "CV",
            "CF",
            "TD",
            "KM",
            "CD",
            "CG",
            "CI",
            "DJ",
            "EG",
            "GQ",
            "ER",
            "ET",
            "GA",
            "GM",
            "GH",
            "GN",
            "GW",
            "KE",
            "LS",
            "LR",
            "LY",
            "MG",
            "MW",
            "ML",
            "MR",
            "MU",
            "YT",
            "MA",
            "MZ",
            "NA",
            "NE",
            "NG",
            "RE",
            "RW",
            "SH",
            "ST",
            "SN",
            "SC",
            "SL",
            "SO",
            "ZA",
            "SS",
            "SD",
            "SZ",
            "TZ",
            "TG",
            "TN",
            "UG",
            "EH",
            "ZM",
            "ZW",
        ],
        "AFO": [  # Afrique de l’Ouest
            "BJ",
            "BF",
            "CV",
            "CI",
            "GM",
            "GH",
            "GN",
            "GW",
            "LR",
            "ML",
            "MR",
            "NE",
            "NG",
            "SN",
            "SL",
            "TG",
        ],
        "AFN": ["DZ", "EG", "LY", "MA", "MR", "SD", "TN", "EH"],  # Afrique du Nord
        "AFE": [  # Afrique de l’Est
            "BI",
            "KM",
            "DJ",
            "ER",
            "ET",
            "KE",
            "MG",
            "MW",
            "MU",
            "RE",
            "RW",
            "SC",
            "SO",
            "SS",
            "TZ",
            "UG",
            "YT",
            "ZM",
            "ZW",
        ],
        "AFC": [  # Afrique Centrale
            "AO",
            "CM",
            "CF",
            "TD",
            "CG",
            "CD",
            "GQ",
            "GA",
            "ST",
        ],
        "AFS": ["BW", "LS", "NA", "ZA", "SZ"],  # Afrique Australe
        "EU": [  # Europe
            "FR",
            "DE",
            "IT",
            "ES",
            "GB",
            "PT",
            "NL",
            "BE",
            "CH",
            "AT",
            "SE",
            "NO",
            "FI",
            "DK",
            "IE",
            "PL",
            "CZ",
            "SK",
            "HU",
            "RO",
            "BG",
            "GR",
            "HR",
            "SI",
            "EE",
            "LV",
            "LT",
            "LU",
            "MT",
            "CY",
            "IS",
            "LI",
            "MD",
            "UA",
            "BY",
            "AL",
            "MK",
            "RS",
            "BA",
            "ME",
            "XK",
        ],
        "EO": ["FR", "BE", "NL", "CH", "LU", "MC"],  # Europe de l’Ouest
        "EN": ["SE", "NO", "FI", "DK", "IS", "EE", "LV", "LT", "IE"],  # Europe du Nord
        "ES": ["IT", "ES", "PT", "GR", "MT", "CY", "SM", "VA", "AD"],  # Europe du Sud
        "EE": [  # Europe de l’Est
            "PL",
            "CZ",
            "SK",
            "HU",
            "RO",
            "BG",
            "UA",
            "BY",
            "MD",
            "RU",
        ],
        "AS": [  # Asie
            "CN",
            "IN",
            "ID",
            "JP",
            "KR",
            "PK",
            "BD",
            "PH",
            "TH",
            "VN",
            "IR",
            "IQ",
            "SA",
            "SY",
            "YE",
            "AE",
            "IL",
            "JO",
            "OM",
            "KW",
            "QA",
            "BH",
            "LB",
            "AF",
            "KZ",
            "UZ",
            "TM",
            "TJ",
            "KG",
            "GE",
            "AM",
            "AZ",
            "LK",
            "MM",
            "NP",
            "BT",
            "MN",
            "KH",
            "LA",
            "SG",
            "MY",
            "TL",
            "BN",
            "PS",
        ],
        "AEO": ["CN", "JP", "KR", "MN", "TW", "HK", "MO", "KP"],  # Asie de l'Est
        "AEN": ["RU", "GE", "AM", "AZ"],  # Asie du Nord
        "AES": ["IN", "PK", "BD", "LK", "NP", "BT", "MV", "AF"],  # Asie du Sud
        "AEC": ["KZ", "UZ", "TM", "TJ", "KG"],  # Asie Centrale
        "AM": [  # Amériques
            "US",
            "CA",
            "MX",
            "BR",
            "AR",
            "CO",
            "CL",
            "PE",
            "VE",
            "EC",
            "BO",
            "PY",
            "UY",
            "GY",
            "SR",
            "GF",
            "CR",
            "PA",
            "GT",
            "HN",
            "SV",
            "NI",
            "CU",
            "DO",
            "HT",
            "JM",
            "TT",
            "BS",
            "BB",
            "BZ",
        ],
        "NA": ["US", "CA", "MX"],  # Amérique du Nord
        "CA": ["GT", "HN", "SV", "NI", "CR", "PA", "BZ"],  # Amérique Centrale
        "CS": [  # Caraïbes et Amérique du Sud
            "CU",
            "DO",
            "HT",
            "JM",
            "TT",
            "BS",
            "BB",
            "BR",
            "AR",
            "CO",
            "CL",
            "PE",
            "VE",
            "EC",
            "BO",
            "PY",
            "UY",
            "GY",
            "SR",
            "GF",
        ],
        "OC": [  # Océanie
            "AU",
            "NZ",
            "PG",
            "FJ",
            "NC",
            "VU",
            "SB",
            "WS",
            "TO",
            "TV",
            "KI",
            "FM",
            "MH",
            "PW",
            "NR",
        ],
        "ON": [  # Océanie du Nord
            "FM",
            "MH",
            "PW",
            "NR",
            "KI",  # États fédérés de Micronésie, Îles Marshall, Palaos, Nauru, Kiribati
        ],
        "OS": [  # Océanie du Sud
            "AU",
            "NZ",
            "PG",
            "FJ",
            "NC",
            "VU",
            "SB",
            "WS",
            "TO",
            "TV",
        ],
        "ANT": [  # Antarctique (aucun pays souverain, mais codes territoriaux possibles)
            # On inclut seulement "AQ" qui est le code ISO 3166-1 alpha-2 pour l’Antarctique
            "AQ"
        ],
    }

    # Pour l'exécution de cette fonction, on suppose que ZONES_TO_PAYS est déjà disponible

    pays_uniques = set()

    for code in codes_mixte:
        if code in ZONES_TO_PAYS:
            pays_uniques.update(
                ZONES_TO_PAYS[code]
            )  # on ajoute tous les pays de la zone
        elif len(code) == 2 and code.isalpha():
            pays_uniques.add(code)  # on ajoute directement le pays s'il est valide
        else:
            print(f"Avertissement : Code inconnu ou invalide ignoré → {code}")

    return sorted(pays_uniques)


def demander_langues():
    langues_disponibles = {
        "1": ("Français", "fr"),
        "2": ("Anglais", "en"),
        "3": ("Espagnol", "es"),
        "4": ("Allemand", "de"),
        "5": ("Portugais", "pt"),
        "6": ("Arabe", "ar"),
        "7": ("Chinois", "zh"),
        "8": ("Russe", "ru"),
        "9": ("Autre (saisir un code ISO)"),
    }

    print("\nDans quelles langues souhaitez-vous collecter les résultats ?")
    for key, val in langues_disponibles.items():
        if key == "9":
            print(f"{key}. {val}")
        else:
            print(f"{key}. {val[0]} ({val[1]})")

    print("Vous pouvez sélectionner plusieurs langues (ex: 1,2,5)")
    print(
        "La liste complète des codes ISO est ici : https://cloud.google.com/translate/docs/languages"
    )

    choix = input("→ ").strip()
    codes = []
    for item in choix.split(","):
        code = item.strip()
        if code in langues_disponibles and code != "9":
            codes.append(langues_disponibles[code][1])
        elif code == "9":
            code_perso = input("Code ISO personnalisé (ex: it, nl) : ").strip().lower()
            if len(code_perso) == 2 and code_perso.isalpha():
                codes.append(code_perso)
            else:
                print("Code ISO invalide.")
        else:
            print(f"Choix invalide : {code}")

    if not codes:
        print("Aucune langue valide saisie. Réessayons.")
        return demander_langues()
    return codes


def demander_sujets():
    print("\nEntrez les sujets à surveiller, séparés par des virgules.")
    print("Exemples : cybersécurité, intelligence artificielle, climat, éducation")

    saisie = input("→ ").strip()
    sujets = [s.strip() for s in saisie.split(",") if s.strip()]

    if not sujets:
        print("Aucun sujet saisi. Veuillez en entrer au moins un.")
        return demander_sujets()

    return sujets


def sauvegarder_config(config, fichier="config.json"):
    with open(fichier, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)


def obtenir_cle_api(source):
    """
    Demande à l'utilisateur une nouvelle clé API pour la source donnée
    et la met à jour dans config.json.
    """
    print(f"\nLa clé API pour {source} est manquante ou invalide.")
    nouvelle_cle = input(
        f"Veuillez entrer une nouvelle clé API pour {source} : "
    ).strip()

    if not nouvelle_cle:
        print("Aucune clé saisie. Abandon.")
        return None

    try:
        with open("config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
    except FileNotFoundError:
        config = {}

    if "api_keys" not in config:
        config["api_keys"] = {}

    config["api_keys"][source] = nouvelle_cle

    with open("config.json", "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)

    print(f"Nouvelle clé enregistrée pour {source}.")
    return nouvelle_cle


def demander_reddit_credentials():
    print("\n⚠️  Reddit credentials requis pour collecter des posts.")
    creds = {}
    creds["client_id"] = input("Client ID : ").strip()
    creds["client_secret"] = input("Client Secret : ").strip()
    creds["username"] = input("Nom d'utilisateur Reddit : ").strip()
    creds["password"] = input("Mot de passe Reddit : ").strip()
    creds["user_agent"] = input(
        "User Agent (ex: script Python de veille Reddit) : "
    ).strip()
    return creds


def initialiser_config():
    config = {}

    # Collecte des paramètres
    config["start_date"], config["end_date"] = [
        d.strftime("%Y-%m-%d %H:%M") for d in demander_periode()
    ]
    config["content_types"] = demander_types_de_contenus()

    if config["content_types"].get("articles", 0) > 0:
        config["content_types"]["sources_articles"] = demander_sources_articles()

    config["max_results"] = demander_nombre_de_resultats()

    codes_mixte = demander_zones_geographiques()
    config["locations"] = convertir_zones_en_pays(codes_mixte)  # ✅ conversion ici

    config["language"] = demander_langues()
    config["topics"] = demander_sujets()

    from utils import (
        valider_reddit_credentials,
    )  # à placer tout en haut si ta fonction est ailleurs

    if config["content_types"].get("posts", 0) > 0:
        try:
            with open("config.json", "r", encoding="utf-8") as f:
                ancienne_config = json.load(f)
                reddit_creds = ancienne_config.get("reddit_credentials", {})
        except FileNotFoundError:
            reddit_creds = {}

        if not valider_reddit_credentials(reddit_creds):
            reddit_creds = demander_reddit_credentials()

        config["reddit_credentials"] = reddit_creds

    # Sauvegarde des anciennes clés API si présentes
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            ancienne_config = json.load(f)
            if "api_keys" in ancienne_config:
                config["api_keys"] = ancienne_config["api_keys"]
    except FileNotFoundError:
        pass

    # Sauvegarde
    sauvegarder_config(config)
    print("\nConfiguration enregistrée avec succès dans config.json.")


if __name__ == "__main__":
    initialiser_config()
