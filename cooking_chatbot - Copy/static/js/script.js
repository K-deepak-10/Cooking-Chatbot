// ================= LIVE DISH SEARCH =================
const dishInput = document.getElementById("dish");
if (dishInput) {
    dishInput.addEventListener("keyup", function () {
        const dish = this.value.trim();

        if (dish.length < 1) {
            document.getElementById("suggestions").innerHTML = "";
            return;
        }

        fetch("/search", {
            method: "POST",
            body: new URLSearchParams({ dish })
        })
        .then(res => res.json())
        .then(data => {
            const select = document.getElementById("suggestions");
            select.innerHTML = "";

            data.forEach(d => {
                const opt = document.createElement("option");
                opt.value = d;
                opt.text = d;
                select.appendChild(opt);
            });
        });
    });
}

// ================= GET DETAILS =================
function getDetails(option) {
    const dish = document.getElementById("suggestions").value;
    if (!dish) { alert("Select a dish first"); return; }

    fetch("/details", {
        method: "POST",
        body: new URLSearchParams({ dish, option })
    })
    .then(res => res.json())
    .then(data => {
        const output = document.getElementById("output");

        if (Array.isArray(data)) {
            output.innerHTML = data.map(d => `<span class="ingredient-chip">${d}</span>`).join(" ");
        } else {
            output.innerText = data;
        }
    });
}

// ================= INGREDIENT SEARCH =================
function ingredientSearch() {
    const ingredients = document.getElementById("ingredientInput").value.trim();
    if (!ingredients) { alert("Enter ingredients"); return; }

    fetch("/ingredient-search", {
        method: "POST",
        body: new URLSearchParams({ ingredients })
    })
    .then(res => res.json())
    .then(data => {
        const output = document.getElementById("output");
        output.innerHTML = data.map(d => `🍽️ ${d[0]} (score: ${d[1]})`).join("<br>");
    });
}

// ================= RESET =================
function resetDish() {
    document.getElementById("dish").value = "";
    document.getElementById("suggestions").innerHTML = "";
    document.getElementById("output").innerText = "";
}

// ================= EXIT =================
function exitApp() {
    fetch("/exit", { method: "POST" }).then(() => {
        alert("👋 Thanks for using Cooking Chatbot!");
        location.reload();
    });
}

// ================= ADD DISH =================
function toggleAddDish() {
    document.getElementById("addDishSection").classList.toggle("d-none");
}

function addDish() {
    const name = document.getElementById("newDishName").value.trim();
    const ingredients = document.getElementById("newIngredients").value.trim();
    const recipe = document.getElementById("newRecipe").value.trim();

    if (!name || !ingredients || !recipe) {
        showAddStatus("All fields are required", "danger");
        return;
    }

    fetch("/add_dish", {
        method: "POST",
        body: new URLSearchParams({ name, ingredients, recipe })
    })
    .then(res => res.json())
    .then(data => {
        showAddStatus(data.message, data.status === "success" ? "success" : "danger");

        if (data.status === "success") {
            document.getElementById("newDishName").value = "";
            document.getElementById("newIngredients").value = "";
            document.getElementById("newRecipe").value = "";

            setTimeout(toggleAddDish, 1500);
            refreshSearchSuggestions(name);
        }
    });
}

function refreshSearchSuggestions(newDish) {
    fetch("/search", {
        method: "POST",
        body: new URLSearchParams({ dish: "" }) // get all dishes
    })
    .then(res => res.json())
    .then(dishes => {
        const select = document.getElementById("suggestions");
        select.innerHTML = "";
        dishes.forEach(d => {
            const opt = document.createElement("option");
            opt.value = d;
            opt.text = d;
            select.appendChild(opt);
        });

        select.value = newDish;
        document.getElementById("output").innerHTML = `🍽️ New dish "${newDish}" added!`;
    });
}

function showAddStatus(message, type) {
    const status = document.getElementById("addStatus");
    status.className = `alert alert-${type}`;
    status.innerText = message;
    status.classList.remove("d-none");
}

// ================= FAVORITES =================
function saveFavorite() {
    const dish = document.getElementById("suggestions").value;
    if (!dish) { alert("Select a dish first"); return; }

    fetch("/favorite", {
        method: "POST",
        body: new URLSearchParams({ dish })
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === "unauthorized") {
            alert("Please login to save favorites");
            window.location.href = "/login";
        } else {
            alert("❤️ Dish added to favorites");
            loadFavorites(); // reload immediately
        }
    });
}

function toggleFavorites() {
    const panel = document.getElementById("favoritesPanel");
    panel.classList.toggle("d-none");
    if (!panel.classList.contains("d-none")) {
        loadFavorites();
    }
}

function loadFavorites() {
    fetch("/favorites")
        .then(res => res.json())
        .then(data => {
            const list = document.getElementById("favoritesList");
            list.innerHTML = "";

            if (data.length === 0) {
                list.innerHTML = "<li class='list-group-item'>No favorites yet 💔</li>";
                return;
            }

            data.forEach(dish => {
                const li = document.createElement("li");
                li.className = "list-group-item";
                li.innerText = "🍽 " + dish;
                list.appendChild(li);
            });
        });
}

// ================= REGISTER =================
function registerUser() {
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();

    if (!username || !password) {
        alert("Please enter username and password");
        return;
    }

    fetch("/register", {
        method: "POST",
        body: new URLSearchParams({ username, password })
    })
    .then(res => res.json())
    .then(data => {
        alert(data.message);
        if (data.status === "success") {
            window.location.href = "/login";
        }
    });
}
