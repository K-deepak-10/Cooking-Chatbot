from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from backend.search_service import find_similar_dishes, get_ingredients, get_recipe, get_similar_dishes
from backend.add_dish_service import add_new_dish
from backend.auth_service import register_user, login_user
from backend.favorite_service import add_favorite, get_favorites
from backend.ranking_service import recommend_similar

app = Flask(__name__)
app.secret_key = "super-secret-key"  # Replace in production

# ==================================================
# ENTRY POINT
# ==================================================
@app.route("/", methods=["GET"])
def root():
    """Public landing. Logged-in users see their dashboard."""
    user = session.get("user")
    return render_template("index.html", user=session.get("user"))

# ==================================================
# LOGIN
# ==================================================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        result = login_user(username, password)
        if result["status"] == "success":
            session["user"] = username
            return jsonify({"status": "success", "redirect": "/app"})
        return jsonify(result)
    return render_template("login.html")

# ==================================================
# REGISTER
# ==================================================
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        return jsonify(register_user(username, password))
    return render_template("register.html")

# ==================================================
# LOGOUT
# ==================================================
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ==================================================
# MAIN APP (LOGIN REQUIRED)
# ==================================================
@app.route("/app")
def app_page():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("index.html", user=session["user"])

# ==================================================
# SEARCH (PUBLIC)
# ==================================================
@app.route("/search", methods=["POST"])
def search():
    dish = request.form.get("dish", "").strip()
    results = find_similar_dishes(dish)
    return jsonify([d.title() for d in results])

# ==================================================
# DETAILS (PUBLIC)
# ==================================================
@app.route("/details", methods=["POST"])
def details():
    dish = request.form.get("dish", "").lower()
    option = request.form.get("option")

    if option == "ingredients":
        return jsonify(get_ingredients(dish))
    elif option == "recipe":
        return jsonify(get_recipe(dish))
    elif option == "similar":
        return jsonify(get_similar_dishes(dish))
    elif option == "smart":
        return jsonify(recommend_similar(dish))

    else:
        return jsonify([])

# ==================================================
# ADD DISH (LOGIN REQUIRED)
# ==================================================
@app.route("/add_dish", methods=["POST"])
def add_dish():
    if "user" not in session:
        return jsonify({"status": "unauthorized", "message": "Please login"})

    name = request.form.get("name")
    ingredients = request.form.get("ingredients")
    recipe = request.form.get("recipe")

    if not name or not ingredients or not recipe:
        return jsonify({"status": "error", "message": "All fields are required"})

    return jsonify(add_new_dish(name, ingredients, recipe))

# ==================================================
# FAVORITES
# ==================================================
@app.route("/favorite", methods=["POST"])
def favorite():
    if "user" not in session:
        return jsonify({"status": "unauthorized"})

    dish = request.form.get("dish")
    add_favorite(session["user"], dish)
    return jsonify({"status": "saved"})

@app.route("/favorites")
def favorites():
    if "user" not in session:
        return jsonify([])
    try:
        favs = get_favorites(session["user"])
    except KeyError:
        favs = []
    return jsonify(favs)

# ==================================================
# EXIT (optional)
# ==================================================
@app.route("/exit", methods=["POST"])
def exit_app():
    session.clear()
    return jsonify({"status": "ok"})

# ==================================================
# RUN
# ==================================================
if __name__ == "__main__":
    app.run(debug=True)
