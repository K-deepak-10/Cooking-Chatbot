🍽️ Cooking Chatbot – Flask Application

A web-based Cooking Chatbot built using Flask, CSV-based storage, and JavaScript, allowing users to search dishes, view ingredients and recipes, get smart recommendations, and manage favorites.
The application supports guest users with limited access and logged-in users with advanced features.

🚀 Features
🔓 Public (No Login Required)

🔍 Live dish search (prefix, contains, fuzzy match)

🧂 View ingredients

📖 View recipe procedure

🔁 Similar dishes

🧠 Smart recommendations

🧪 Ingredient-based ranking

🔐 Logged-in Users

❤️ Save favorite dishes

📂 View saved favorites

➕ Add new dishes

👤 User session management

🧱 Tech Stack

Backend: Flask (Python)

Frontend: HTML, Bootstrap 5, Vanilla JavaScript

Data Storage:

food2.csv – dishes data

users.csv – registered users

favorites.csv – user favorites

Search Engine: RapidFuzz

Deployment: Railway

📁 Project Structure
cooking_chatbot/
│
├── app.py
├── backend/
│   ├── search_service.py
│   ├── recipe_service.py
│   ├── ranking_service.py
│   ├── recommendation_service.py
│   ├── auth_service.py
│   ├── favorite_service.py
│   └── data_loader.py
│
├── data/
│   ├── food2.csv
│   ├── users.csv
│   └── favorites.csv
│
├── static/
│   ├── css/style.css
│   └── js/script.js
│
├── templates/
│   ├── index.html
│   ├── login.html
│   └── register.html
│
└── README.md
