from flask import Flask, request, jsonify
import mysql.connector
from flask_jwt_extended import JWTManager, create_access_token, jwt_required

app = Flask(__name__)

#pip install flask mysql-connector-python flask_jwt_extended

# MySQL Config
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'flask_jwt_demo'
}

# JWT Config
app.config['JWT_SECRET_KEY'] = 'super-secret-key'
jwt = JWTManager(app)

# Register User
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username, password = data['username'], data['password']

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", 
                   (username, password))
    conn.commit()
    conn.close()

    return jsonify({"message": "User registered successfully!"}), 201

# Login and get JWT
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username, password = data['username'], data['password']

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", 
                   (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        token = create_access_token(identity=username)
        return jsonify({"token": token})
    return jsonify({"error": "Invalid username or password"}), 401

# Protected Route
@app.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    return jsonify({"message": "Welcome! You accessed a protected route."})

if __name__ == '__main__':
    app.run(debug=True)
