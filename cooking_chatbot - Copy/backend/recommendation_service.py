from backend.data_loader import df

def recommend_similar(dish):
    base = df[df["name_clean"] == dish].iloc[0]
    base_ingredients = base["ingredients_clean"]

    recommendations = []

    for _, row in df.iterrows():
        if row["name_clean"] != dish:
            common = len(
                set(base_ingredients.split(","))
                & set(row["ingredients_clean"].split(","))
            )
            if common >= 2:
                recommendations.append((row["RecipeName"], common))

    recommendations.sort(key=lambda x: x[1], reverse=True)
    return recommendations[:8]
