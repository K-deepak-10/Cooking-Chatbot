from backend.data_loader import df

def ingredient_match_score(dish_ingredients, query_ingredients):
    score = 0
    for q in query_ingredients:
        if q in dish_ingredients:
            score += 1
    return score

def rank_by_ingredients(query_ingredients):
    results = []
    for _, row in df.iterrows():
        score = ingredient_match_score(
            row["ingredients_clean"],
            query_ingredients
        )
        if score > 0:
            results.append((row["RecipeName"], score))
    results.sort(key=lambda x: x[1], reverse=True)
    return results[:10]

def recommend_similar(dish_name):
    # find the row of the given dish
    row = df[df["name_clean"] == dish_name.lower().strip()]
    if row.empty:
        return []

    ingredients = row.iloc[0]["ingredients_clean"]
    similar = rank_by_ingredients(ingredients)
    # remove the dish itself from results
    similar = [d[0] for d in similar if d[0].lower() != dish_name.lower().strip()]
    return similar[:5]
