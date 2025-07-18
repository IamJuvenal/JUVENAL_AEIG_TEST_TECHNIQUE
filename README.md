# JUVENAL_AEIG_TEST_TECHNIQUE
# 🛰️ Système de Veille Automatique

Ce dépôt contient un projet de veille automatisée permettant de collecter, structurer et stocker des contenus web (articles, posts, tweets -à venir-) selon plusieurs critères définis par l’utilisateur.

## 🚀 Fonctionnalités principales

* Assistant de configuration interactif (langue, zone géographique, thématiques, période…)
* Répartition des types de contenus à collecter (% d’articles, de posts, de tweets)
* Normalisation automatique des codes de pays à partir de zones géographiques
* Collecte aléatoire et équilibrée à partir des paramètres utilisateur
* Stockage des résultats dans un fichier CSV (`veille_resultats.csv`)

## 🔧 Structure du projet

```bash
├── init_config.py           # Assistant interactif de configuration
├── collect/                 # Fonctions de collecte par type de contenu
│   ├── __init__.py
│   ├── collecter_articles.py
│   ├── collecter_posts.py
│   └── collecter_tweets.py
├── storage/                 # Fonctions d’enregistrement et de vérification
│   └── sauvegarde.py
├── main.py                  # Script principal (appelle l’assistant et lance la collecte)
├── config.json              # Fichier de configuration généré automatiquement
├── veille_resultats.csv     # Fichier de sortie contenant les résultats
└── utils.py                # permettant de valider ses identifiants pour l'accès à l'API de Reddit
└── README.md                # Ce fichier
```


## 📦 Dépendances

Tout le projet etant en ligne de commande et s'éxécutant sous python, quelques dépendances non natives pourraient etre necessaire à installer via pip

Il s'agit de : 

requests

datetime

uuid

json

csv


## 💻 Utilisation

Après l'installation des dépendances
Lancez simplement le fichier `main.py` avec le code suivant. :

```bash
python main.py
```

Cela ouvre un assistant interactif qui vous guide pas à pas dans le choix :

* de la période de veille,
* des types de contenus à collecter,
* des zones géographiques,
* des langues,
* des sujets d’intérêt.

Une fois la configuration terminée, le système lance la collecte et sauvegarde les résultats dans un fichier CSV (`veille_resultats.csv`).


## 📌 Avertissement

Le système est prévu pour s'adapter progressivement à d'autres sources (tweets, blogs, etc.)

Un module d’export automatique vers Google Sheets est en cours d’implémentation.

Les clés API (GNews, NewsAPI, Reddit, etc.) sont demandées lors de la configuration si non encore enregistrées. Pour la scalabilité du projet, ils sont saisis par l'utilisateur au début de l'exécution de la requete. Voici mes clés personnelles pour tester le projet. Privilégier les petites tailles de requetes : 2-4 pour pouvoir tester plusieurs fois avant épuisement.

🔑 1. Identifiants Reddit (pour collecter les posts)
{
  "client_id": "oIVxnERY3jl5kQVxkWJkjw",
  "client_secret": "yu84Rhn3fGjpNzrzlz4ZtwXI8Nl79Q",
  "username": "AsparagusRare9203",
  "password": "Aa@12345678",
  "user_agent": "veille-auto-script/0.1 by AsparagusRare9203"
}

🌐 2. Clé API GNews (pour collecter des articles)
{
  "GNews": "1efc5b20b66ddb9ceda93df72117cce1"
}

🌐 3. Clé API NewsAPI (autre source d’articles)
{
  "NewsAPI": "2b92ea76285e428a99c8ebe7dba3e9c3"
}



Limite du projet

Pour le moment, les informations sont stockées en locale. Nous continuons de developper la solution pour que les infos soient envoyées vers airtable. Nous pourrions faire un nouveau push sur votre demande qui contiendra cette fonctionnalité.
---

© 2025 — Développé par Juvenal KPODJADAN
