import csv
import os
from backend.add_dish_service import get_all_dishes

FOOD_FILE = "data/food2.csv"

def get_ingredients(dish_name):
    dish_name = dish_name.lower()
    if not os.path.exists(FOOD_FILE):
        return []

    with open(FOOD_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["RecipeName"].lower() == dish_name:
                return [i.strip() for i in row["Ingredients"].split(",")]
    return []

def get_recipe(dish_name):
    dish_name = dish_name.lower()
    if not os.path.exists(FOOD_FILE):
        return "Recipe not found"

    with open(FOOD_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["RecipeName"].lower() == dish_name:
                return row["Procedure"]
    return "Recipe not found"

def get_similar_dishes(dish_name):
    dish_name = dish_name.lower()
    results = []
    if not os.path.exists(FOOD_FILE):
        return results

    with open(FOOD_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if dish_name in row["RecipeName"].lower() and row["RecipeName"].lower() != dish_name:
                results.append(row["RecipeName"])
    return results

def recommend_similar(dish_name):
    target_ingredients = set(get_ingredients(dish_name))
    recommendations = []

    for other_dish in get_all_dishes():
        if other_dish.lower() == dish_name.lower():
            continue
        other_ingredients = set(get_ingredients(other_dish))
        score = len(target_ingredients & other_ingredients)
        if score > 0:
            recommendations.append((other_dish, score))

    recommendations.sort(key=lambda x: x[1], reverse=True)
    return [dish for dish, _ in recommendations][:5]
