from flask import Flask, request, jsonify, render_template, redirect, url_for
import json, os

app = Flask(__name__)

DB_FILE = "db.json"

# -----------------------
# Helper Functions
# -----------------------

# Load JSON data
def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {"users": []}

# Save JSON data
def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

# -----------------------
# API ROUTES
# -----------------------

# Get all users (API)
@app.route('/api/users', methods=['GET'])
def get_users():
    data = load_data()
    return jsonify(data["users"])

# Add new user (API - POST)
@app.route('/api/users', methods=['POST'])
def add_user():
    data = load_data()
    new_user = request.get_json()

    # Auto-increment ID
    if data["users"]:
        new_user["id"] = max(u["id"] for u in data["users"]) + 1
    else:
        new_user["id"] = 1

    data["users"].append(new_user)
    save_data(data)

    return jsonify({"msg": "User added successfully", "user": new_user}), 201

# Update user by ID (API - PUT)
@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = load_data()
    users = data["users"]
    user = next((u for u in users if u["id"] == user_id), None)

    if not user:
        return jsonify({"error": "User not found"}), 404

    update_data = request.get_json()
    user["name"] = update_data.get("name", user["name"])
    user["email"] = update_data.get("email", user["email"])

    save_data(data)
    return jsonify({"msg": "User updated successfully", "user": user})

# Delete user by ID (API - DELETE)
@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    data = load_data()
    users = data["users"]
    user = next((u for u in users if u["id"] == user_id), None)

    if not user:
        return jsonify({"error": "User not found"}), 404

    users.remove(user)
    save_data(data)

    return jsonify({"message": f"User {user_id} deleted successfully!"})

# -----------------------
# HTML ROUTES
# -----------------------

# Add User Form
@app.route('/add-user', methods=['GET', 'POST'])
def add_user_form():
    data = load_data()

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        new_id = max([u["id"] for u in data["users"]], default=0) + 1
        new_user = {"id": new_id, "name": name, "email": email}

        data["users"].append(new_user)
        save_data(data)

        return redirect(url_for('add_user_form'))

    # Pass users to template
    return render_template("add_user.html", users=data["users"])


# Update User Form
@app.route('/update-user', methods=['GET', 'POST'])
def update_user_form():
    if request.method == 'POST':
        user_id = int(request.form['id'])
        name = request.form['name']
        email = request.form['email']

        data = load_data()
        users = data["users"]
        user = next((u for u in users if u["id"] == user_id), None)

        if user:
            user["name"] = name
            user["email"] = email
            save_data(data)
            return redirect(url_for('update_user_form'))
        else:
            return "User not found", 404

    return render_template("update_user.html")

# List Users Page
@app.route('/users')
def users_page():
    data = load_data()
    return render_template("users.html", users=data["users"])

# -----------------------
# Main Runner
# -----------------------
if __name__ == '__main__':
    app.run(debug=True)
