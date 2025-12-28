import csv
import os

USER_FILE = "data/users.csv"

def register_user(username, password):
    username = username.strip()
    password = password.strip()

    if not os.path.exists(USER_FILE):
        with open(USER_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["username", "password"])
            writer.writeheader()

    # Check if username exists
    with open(USER_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["username"] == username:
                return {"status": "error", "message": "Username already exists"}

    # Register new user
    with open(USER_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["username", "password"])
        writer.writerow({"username": username, "password": password})

    return {"status": "success", "message": "User registered successfully"}

def login_user(username, password):
    username = username.strip()
    password = password.strip()

    if not os.path.exists(USER_FILE):
        return {"status": "error", "message": "User not found"}

    with open(USER_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("username") == username and row.get("password") == password:
                return {"status": "success"}
    return {"status": "error", "message": "Invalid username or password"}
