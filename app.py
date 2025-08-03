from flask import Flask, request, jsonify
import sqlite3
import json
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = conn.cursor()

@app.route('/')
def home():
    return "User Management System"


@app.route('/users', methods=['GET'])
def get_all_users():
    try:
        cursor.execute("SELECT id, name, email FROM users")
        users = cursor.fetchall()

        user_list = [
            {"id": row[0], "name": row[1], "email": row[2]}
            for row in users
        ]

        return jsonify(user_list), 200

    except Exception as e:
        return jsonify({
            "error": "Failed to fetch users",
            "details": str(e)
        }), 500

# @app.route('/users', methods=['GET'])
# def get_all_users():
#     cursor.execute("SELECT * FROM users")
#     users = cursor.fetchall()
#     return str(users)


@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        cursor.execute("SELECT id, name, email FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()

        if user:
            return jsonify({
                "id": user[0],
                "name": user[1],
                "email": user[2]
            }), 200
        else:
            return jsonify({"error": "User not found"}), 404

    except Exception as e:
        return jsonify({
            "error": "Failed to retrieve user",
            "details": str(e)
        }), 500


# @app.route('/user/<user_id>', methods=['GET'])
# def get_user(user_id):
#     query = f"SELECT * FROM users WHERE id = '{user_id}'"
#     cursor.execute(query)
#     user = cursor.fetchone()
    
#     if user:
#         return str(user)
#     else:
#         return "User not found"


from flask import Flask, request, jsonify
import sqlite3

# ... your app and db setup stays the same

@app.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json(force=True)
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()

        # Basic validation
        if not name or not email or not password:
            return jsonify({"error": "Name, email, and password are required."}), 400

        # Optional: check for email format (basic check)
        if '@' not in email or '.' not in email:
            return jsonify({"error": "Invalid email format."}), 422

        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            (name, email, password)
        )
        conn.commit()

        return jsonify({"message": "User created successfully!"}), 201

    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


# @app.route('/users', methods=['POST'])
# def create_user():
#     data = request.get_json()
#     name = data.get('name')
#     email = data.get('email')
#     password = data.get('password')

#     if not name or not email or not password:
#         return jsonify({"error": "Missing required fields"}), 400

#     hashed_pw = generate_password_hash(password)
#     cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, hashed_pw))
#     conn.commit()

#     return jsonify({"message": "User created successfully"}), 201


# @app.route('/users', methods=['POST'])
# def create_user():
#     data = request.get_data()
#     data = json.loads(data)
    
#     name = data['name']
#     email = data['email']
#     password = data['password']
    
#     cursor.execute(f"INSERT INTO users (name, email, password) VALUES ('{name}', '{email}', '{password}')")
#     conn.commit()
    
#     print("User created successfully!")
#     return "User created"


@app.route('/user/<user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')

        if not name or not email:
            return jsonify({"error": "Both name and email are required"}), 400

        cursor.execute(
            "UPDATE users SET name = ?, email = ? WHERE id = ?",
            (name, email, user_id)
        )
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "User not found"}), 404

        return jsonify({"message": "User updated successfully"}), 200

    except Exception as e:
        return jsonify({
            "error": "Failed to update user",
            "details": str(e)
        }), 500

# @app.route('/user/<user_id>', methods=['PUT'])
# def update_user(user_id):
#     data = request.get_data()
#     data = json.loads(data)
    
#     name = data.get('name')
#     email = data.get('email')
    
#     if name and email:
#         cursor.execute(f"UPDATE users SET name = '{name}', email = '{email}' WHERE id = '{user_id}'")
#         conn.commit()
#         return "User updated"
#     else:
#         return "Invalid data"


@app.route('/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "User not found"}), 404

        return jsonify({"message": f"User {user_id} deleted successfully"}), 200

    except Exception as e:
        return jsonify({
            "error": "Failed to delete user",
            "details": str(e)
        }), 500

# @app.route('/user/<user_id>', methods=['DELETE'])
# def delete_user(user_id):
#     cursor.execute(f"DELETE FROM users WHERE id = '{user_id}'")
#     conn.commit()
    
#     print(f"User {user_id} deleted")
#     return "User deleted"

@app.route('/search', methods=['GET'])
def search_users():
    name = request.args.get('name')

    if not name:
        return jsonify({"error": "Missing 'name' query parameter"}), 400

    try:
        cursor.execute("SELECT id, name, email FROM users WHERE name LIKE ?", (f"%{name}%",))
        users = cursor.fetchall()

        if not users:
            return jsonify({"message": "No users found"}), 404

        results = [
            {"id": user[0], "name": user[1], "email": user[2]}
            for user in users
        ]

        return jsonify({"results": results}), 200

    except Exception as e:
        return jsonify({"error": "Failed to search users", "details": str(e)}), 500

# @app.route('/search', methods=['GET'])
# def search_users():
#     name = request.args.get('name')
    
#     if not name:
#         return "Please provide a name to search"
    
#     cursor.execute(f"SELECT * FROM users WHERE name LIKE '%{name}%'")
#     users = cursor.fetchall()
#     return str(users)


@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json(force=True)
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()

        # Validation
        if not email or not password:
            return jsonify({"error": "Email and password are required."}), 400

        cursor.execute(
            "SELECT * FROM users WHERE email = ? AND password = ?",
            (email, password)
        )
        user = cursor.fetchone()

        if user:
            return jsonify({
                "status": "success",
                "user_id": user[0],
                "message": "Login successful"
            }), 200
        else:
            return jsonify({
                "status": "failed",
                "message": "Invalid email or password"
            }), 401

    except Exception as e:
        return jsonify({
            "error": "Internal server error",
            "details": str(e)
        }), 500

# @app.route('/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     email = data.get('email')
#     password = data.get('password')

#     if not email or not password:
#         return jsonify({"error": "Missing email or password"}), 400

#     cursor.execute("SELECT id, password FROM users WHERE email = ?", (email,))
#     user = cursor.fetchone()

#     if user and check_password_hash(user[1], password):
#         return jsonify({"status": "success", "user_id": user[0]})
#     else:
#         return jsonify({"status": "failed"}), 401


# @app.route('/login', methods=['POST'])
# def login():
#     data = json.loads(request.get_data())
#     email = data['email']
#     password = data['password']
    
#     cursor.execute(f"SELECT * FROM users WHERE email = '{email}' AND password = '{password}'")
#     user = cursor.fetchone()
    
#     if user:
#         return jsonify({"status": "success", "user_id": user[0]})
#     else:
#         return jsonify({"status": "failed"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5009, debug=True)