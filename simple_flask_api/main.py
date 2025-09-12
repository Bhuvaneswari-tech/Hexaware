from flask import Flask, request, jsonify
import mysql.connector
from flask_jwt_extended import JWTManager, create_access_token, jwt_required

app = Flask(__name__)

# MySQL Config
db_config = {
    'host': 'localhost',
    'user': 'root',       # change to your MySQL username
    'password': 'root',   # change to your MySQL password
    'database': 'flask_jwt_demo'  # make sure this DB exists
}

# JWT Config
app.config['JWT_SECRET_KEY'] = 'super-secret-key'
jwt = JWTManager(app)

# ✅ Helper function for DB connection
def get_db_connection():
    return mysql.connector.connect(**db_config)

# ---------------- AUTH ----------------
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username, password = data['username'], data['password']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "User registered successfully!"}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username, password = data['username'], data['password']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user:
        token = create_access_token(identity=username)
        return jsonify({"token": token})
    return jsonify({"error": "Invalid username or password"}), 401


@app.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    return jsonify({"message": "Welcome! You accessed a protected route."})


# ---------------- STUDENT CRUD ----------------
@app.route("/students", methods=["POST"])
@jwt_required()
def add_student():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO students (name, age, grade) VALUES (%s, %s, %s)",
                   (data["name"], data["age"], data["grade"]))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Student added successfully!"})

@app.route("/students", methods=["GET"])
@jwt_required()
def list_students():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(students)


# ---------------- MAIN ----------------
if __name__ == '__main__':
    app.run(debug=True)
