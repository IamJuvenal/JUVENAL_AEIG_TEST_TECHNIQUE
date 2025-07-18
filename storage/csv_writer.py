import csv
import os

# Structure homogène commune à tous les contenus collectés
FIELDNAMES = [
    "id",
    "titre",
    "description",
    "contenu",
    "url",
    "image_url",
    "date_publication",
    "source_nom",
    "source_url",
    "type_contenu",
]


def append_to_csv(data, filename):
    """
    Ajoute des lignes au fichier CSV dans une structure homogène.
    Si le fichier n'existe pas, il est créé avec l'en-tête.
    """
    if not data:
        print("Aucune donnée à sauvegarder.")
        return

    # Vérifie si le fichier existe déjà
    file_exists = os.path.isfile(filename)

    with open(filename, mode="a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)

        # Écrit l'en-tête si le fichier est vide/nouveau
        if not file_exists:
            writer.writeheader()

        for row in data:
            # Assure une correspondance exacte des champs attendus
            ligne = {champ: row.get(champ, "") for champ in FIELDNAMES}
            writer.writerow(ligne)
