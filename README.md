# JUVENAL_AEIG_TEST_TECHNIQUE
# 🛰️ Système de Veille Automatique

Ce dépôt contient un projet de veille automatisée permettant de collecter, structurer et stocker des contenus web (articles, posts, tweets) selon plusieurs critères définis par l’utilisateur.

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
│   ├── articles.py
│   ├── posts.py
│   └── tweets.py
├── storage/                 # Fonctions d’enregistrement et de vérification
│   └── sauvegarde.py
├── main.py                  # Script principal (appelle l’assistant et lance la collecte)
├── config.json              # Fichier de configuration généré automatiquement
├── veille_resultats.csv     # Fichier de sortie contenant les résultats
└── README.md                # Ce fichier
```

## 💻 Utilisation

Lancez simplement le fichier `main.py` :

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

## 📦 Dépendances

Le projet utilise principalement :

* `random`, `json`, `datetime`
* (à venir) des connecteurs d’API externes comme GNews, Reddit, X.com…

## 📌 Avertissement

Ce projet a été réalisé dans le cadre d’un test technique pour AIEG. Il peut intégrer des données simulées pour l’instant, en attendant l’intégration complète d’APIs réelles.

---

© 2025 — Développé par Juvenal KPODJADAN
