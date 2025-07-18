# storage/csv_writer.py

import csv
import os

def append_to_csv(data_list, filename):
    """Ajoute une liste de dictionnaires dans un fichier CSV."""

    file_exists = os.path.isfile(filename)

    with open(filename, mode="a", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["date", "type", "sujet", "titre", "source", "lien", "résumé"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        for row in data_list:
            writer.writerow(row)
