import csv
import os
import pandas as pd

FOOD_FILE = "data/food2.csv"

def add_new_dish(name, ingredients, recipe):
    name = name.strip()
    ingredients = ingredients.strip()
    recipe = recipe.strip()

    if not os.path.exists(FOOD_FILE):
        with open(FOOD_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["RecipeName", "Ingredients", "Procedure"])
            writer.writeheader()

    # Append new dish
    with open(FOOD_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["RecipeName", "Ingredients", "Procedure"])
        writer.writerow({
            "RecipeName": name,
            "Ingredients": ingredients,
            "Procedure": recipe
        })

    # Update search dataframe
    global df, dish_list
    df = pd.read_csv(FOOD_FILE, encoding="latin-1", on_bad_lines="skip")
    df["name_clean"] = df["RecipeName"].str.lower().str.strip()
    dish_list = df["name_clean"].dropna().unique().tolist()

    return {"status": "success", "message": f"Dish '{name}' added successfully!"}
