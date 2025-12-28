import pandas as pd
from rapidfuzz import process, fuzz

# ---------------- LOAD DATA ----------------
try:
    df = pd.read_csv("data/food2.csv", encoding="latin-1", on_bad_lines="skip")
except FileNotFoundError:
    df = pd.DataFrame(columns=["RecipeName", "Ingredients", "Procedure"])

# Clean dish names for search
df["name_clean"] = df["RecipeName"].str.lower().str.strip()
dish_list = df["name_clean"].dropna().unique().tolist()

# ---------------- SEARCH FUNCTION ----------------
def find_similar_dishes(query, limit=10):
    if not query:
        return []

    query = query.lower().strip()
    
    # 1️⃣ Prefix matches
    prefix_matches = [d for d in dish_list if d.startswith(query)]
    
    # 2️⃣ Word-level contains
    word_matches = [d for d in dish_list if query in d.split()]
    
    # 3️⃣ Loose contains
    contains_matches = [d for d in dish_list if query in d and d not in prefix_matches]
    
    # 4️⃣ Fuzzy fallback
    fuzzy_matches = process.extract(query, dish_list, scorer=fuzz.partial_ratio, limit=limit)
    fuzzy_filtered = [m[0] for m in fuzzy_matches if m[1] >= 50]

    # Merge all results, deduplicate
    combined = prefix_matches + word_matches + contains_matches + fuzzy_filtered
    unique_results = list(dict.fromkeys(combined))

    return unique_results[:limit]

# ---------------- GET INGREDIENTS ----------------
def get_ingredients(dish_name):
    dish_name = dish_name.lower().strip()
    row = df[df["name_clean"] == dish_name]
    if row.empty:
        return []
    return [i.strip() for i in row.iloc[0]["Ingredients"].split(",")]

# ---------------- GET RECIPE ----------------
def get_recipe(dish_name):
    dish_name = dish_name.lower().strip()
    row = df[df["name_clean"] == dish_name]
    if row.empty:
        return "Recipe not found"
    return row.iloc[0]["Procedure"]

# ---------------- GET SIMILAR DISHES ----------------
def get_similar_dishes(dish_name, limit=5):
    dish_name = dish_name.lower().strip()
    return [d for d in find_similar_dishes(dish_name, limit=limit) if d != dish_name]
