import csv
import os

FAV_FILE = "data/favorites.csv"

def add_favorite(username, dish):
    dish = dish.strip()
    file_exists = os.path.exists(FAV_FILE) and os.path.getsize(FAV_FILE) > 0

    with open(FAV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["username", "dish"])
        if not file_exists:
            writer.writeheader()
        writer.writerow({"username": username, "dish": dish})

def get_favorites(username):
    if not os.path.exists(FAV_FILE):
        return []
    favorites = []
    with open(FAV_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if "username" in row and "dish" in row and row["username"] == username:
                favorites.append(row["dish"])
    return favorites

