import random
import json
import requests
from init_config import obtenir_cle_api
from storage.csv_writer import append_to_csv


def charger_config():
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Erreur : config.json introuvable. Lancez init_config.py d'abord.")
        exit(1)


def charger_cles_api():
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("api_keys", {})
    except FileNotFoundError:
        return {}


def fetch_from_gnews(query, lang, country, start_date, end_date, max_results, api_key):
    url = "https://gnews.io/api/v4/search"
    params = {
        "q": query,
        "lang": lang,
        "country": country.lower(),
        "from": start_date,
        "to": end_date,
        "max": max_results,
        "token": api_key,
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()
        if "articles" in data:
            return data["articles"]
        elif "errors" in data or "message" in data:
            raise ValueError(f"Erreur GNews: {data.get('message', 'clé API invalide')}")
        else:
            return []
    except Exception as e:
        print(f"Erreur lors de la requête GNews : {e}")
        return None


def fetch_from_newsapi(
    query, lang, country, start_date, end_date, max_results, api_key
):
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "language": lang,
        "from": start_date,
        "to": end_date,
        "pageSize": max_results,
        "apiKey": api_key,
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()
        if "articles" in data:
            return data["articles"]
        elif "code" in data and data["code"] == "apiKeyInvalid":
            raise ValueError("Clé NewsAPI invalide")
        else:
            return []
    except Exception as e:
        print(f"Erreur lors de la requête NewsAPI : {e}")
        return None


def normaliser_article(article, source_name, type_contenu="article"):
    return {
        "id": article.get("source", {}).get("id") or "",
        "titre": article.get("title") or "",
        "description": article.get("description") or "",
        "contenu": article.get("content") or "",
        "url": article.get("url") or "",
        "image_url": article.get("image") or article.get("urlToImage") or "",
        "date_publication": article.get("publishedAt") or "",
        "source_nom": article.get("source", {}).get("name") or source_name,
        "source_url": article.get("source", {}).get("url") or "",
        "type_contenu": type_contenu,
    }


def collecter_articles():
    config = charger_config()
    cles_api = charger_cles_api()
    articles_final = []

    sources = config["content_types"].get("sources_articles", ["GNews", "NewsAPI"])
    sujets = config["topics"]
    langues = config["language"]
    pays = config["locations"]
    start_date = config["start_date"]
    end_date = config["end_date"]
    max_results = config["max_results"]
    nb_par_source = max_results // len(sources)

    for source in sources:
        cle = cles_api.get(source)
        if not cle:
            cle = obtenir_cle_api(source)
            if not cle:
                continue
            cles_api[source] = cle  # MAJ immédiate

        for sujet in sujets:
            lang = random.choice(langues)
            country = random.choice(pays)

            if source == "GNews":
                resultats = fetch_from_gnews(
                    sujet, lang, country, start_date, end_date, nb_par_source, cle
                )
                if resultats is None:
                    cle = obtenir_cle_api("GNews")
                    if not cle:
                        continue
                    cles_api["GNews"] = cle
                    resultats = fetch_from_gnews(
                        sujet, lang, country, start_date, end_date, nb_par_source, cle
                    )

            elif source == "NewsAPI":
                resultats = fetch_from_newsapi(
                    sujet, lang, country, start_date, end_date, nb_par_source, cle
                )
                if resultats is None:
                    cle = obtenir_cle_api("NewsAPI")
                    if not cle:
                        continue
                    cles_api["NewsAPI"] = cle
                    resultats = fetch_from_newsapi(
                        sujet, lang, country, start_date, end_date, nb_par_source, cle
                    )

            if resultats:
                articles_final.extend(
                    [
                        normaliser_article(article, source_name=source)
                        for article in resultats
                    ]
                )

    if articles_final:
        append_to_csv(articles_final, "veille_resultats.csv")
        print(f"✅ {len(articles_final)} articles ajoutés à veille_resultats.csv")


if __name__ == "__main__":
    collecter_articles()
