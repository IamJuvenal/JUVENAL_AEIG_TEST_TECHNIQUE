# collect/google_news.py

import subprocess
import sys

# Vérifie si la bibliothèque gnews est installée, sinon l’installe
try:
    from gnews import GNews
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "gnews"])
    from gnews import GNews

from datetime import datetime

google_news = GNews(language="fr", country="FR", max_results=10)


def collect_articles(subject):
    results = google_news.get_news(subject)
    articles = []

    for item in results:
        raw_date = item.get("published date")

        # Gère différents formats de date
        if isinstance(raw_date, datetime):
            date_formatted = raw_date.strftime("%Y-%m-%d")
        elif isinstance(raw_date, str):
            date_formatted = raw_date[:10]
        else:
            date_formatted = datetime.now().strftime("%Y-%m-%d")

        articles.append(
            {
                "date": date_formatted,
                "type": "article",
                "sujet": subject,
                "titre": item.get("title", ""),
                "source": item.get("publisher", {}).get("title", ""),
                "lien": item.get("url", ""),
                "résumé": item.get("description", ""),
            }
        )

    return articles
