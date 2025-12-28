import pandas as pd

df = pd.read_csv("data/food2.csv", encoding="latin-1", on_bad_lines="skip")
df["name_clean"] = df["RecipeName"].str.lower().str.strip()
df["ingredients_clean"] = df["Ingredients"].str.lower().str.split(",").apply(lambda x: [i.strip() for i in x])
