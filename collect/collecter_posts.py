import requests
import json
import uuid
from datetime import datetime
from init_config import demander_reddit_credentials, sauvegarder_config
from utils import valider_reddit_credentials
from storage.csv_writer import append_to_csv


def charger_config():
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ Fichier config.json introuvable.")
        exit(1)


def obtenir_token_reddit(creds):
    auth = requests.auth.HTTPBasicAuth(creds["client_id"], creds["client_secret"])
    data = {
        "grant_type": "password",
        "username": creds["username"],
        "password": creds["password"],
    }
    headers = {"User-Agent": creds["user_agent"]}

    try:
        res = requests.post(
            "https://www.reddit.com/api/v1/access_token",
            auth=auth,
            data=data,
            headers=headers,
        )

        if res.status_code == 200 and "access_token" in res.json():
            return res.json()["access_token"]
        else:
            print("❌ Erreur d'authentification Reddit :", res.json())
            return None
    except Exception as e:
        print("❌ Exception lors de l’authentification Reddit :", str(e))
        return None


def rechercher_posts(token, sujet, max_results):
    headers = {"Authorization": f"bearer {token}", "User-Agent": "veille-auto-script"}
    url = f"https://oauth.reddit.com/search?q={sujet}&limit={max_results}&sort=new"

    try:
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        posts = res.json()["data"]["children"]
        return posts
    except Exception as e:
        print("❌ Erreur lors de la recherche Reddit :", str(e))
        return []


def transformer_posts(posts):
    transformés = []
    for post in posts:
        data = post["data"]
        transformés.append(
            {
                "id": data.get("id", str(uuid.uuid4())),
                "titre": data.get("title", ""),
                "description": "",
                "contenu": data.get("selftext", ""),
                "url": f"https://www.reddit.com{data.get('permalink', '')}",
                "image_url": (
                    data.get("url_overridden_by_dest", "")
                    if data.get("post_hint") == "image"
                    else ""
                ),
                "date_publication": (
                    datetime.utcfromtimestamp(data.get("created_utc")).isoformat()
                    if data.get("created_utc")
                    else ""
                ),
                "source_nom": "Reddit",
                "source_url": "https://www.reddit.com",
                "type_contenu": "post",
            }
        )
    return transformés


def collecter_posts():
    config = charger_config()
    reddit_creds = config.get("reddit_credentials", {})

    if not valider_reddit_credentials(reddit_creds):
        print("❌ Identifiants Reddit incomplets.")
        reddit_creds = demander_reddit_credentials()
        config["reddit_credentials"] = reddit_creds
        sauvegarder_config(config)

    access_token = obtenir_token_reddit(reddit_creds)

    if not access_token:
        print("🔁 Tentative avec de nouveaux identifiants Reddit...")
        reddit_creds = demander_reddit_credentials()
        config["reddit_credentials"] = reddit_creds
        sauvegarder_config(config)
        access_token = obtenir_token_reddit(reddit_creds)

    if not access_token:
        print("🚫 Impossible d’obtenir un token Reddit. Abandon.")
        return

    print("✅ Authentification Reddit réussie. Prêt à collecter les posts.")

    sujets = config["topics"]
    max_results = config.get("max_results", 10)

    tous_les_posts = []

    for sujet in sujets:
        brut = rechercher_posts(access_token, sujet, max_results)
        nettoyés = transformer_posts(brut)
        tous_les_posts.extend(nettoyés)

    if tous_les_posts:
        append_to_csv(tous_les_posts, "veille_resultats.csv")
        print(f"✅ {len(tous_les_posts)} posts ajoutés à veille_resultats.csv")
    else:
        print("⚠️ Aucun post Reddit trouvé.")


if __name__ == "__main__":
    collecter_posts()
