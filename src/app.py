from flask import Flask, render_template, request, redirect, url_for, jsonify
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.form.to_dict()
    users = load_users()
    success, message = register_user(data, users)
    if success:
        # Assuming you want to go to the dashboard after registration
        return redirect(url_for('dashboard'))
    else:
        return jsonify({"success": False, "message": message}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.form.to_dict()
    users = load_users()
    success, user_info = login_user(data, users)
    if success:
        return redirect(url_for('dashboard'))
    else:
        return jsonify({"success": False, "message": "Invalid credentials"}), 401

@app.route('/dashboard')
def dashboard():
    # Assuming the user is logged in
    return render_template('dashboard.html')  # Render a dashboard template

def load_users():
    with open('users.json', 'r') as file:
        return json.load(file)

def save_users_data(users):
    with open('users.json', 'w') as file:
        json.dump(users, file, indent=4)

def register_user(data, users):
    email = data.get('email')
    if email in users:
        return False, "User already exists."
    users[email] = {
        "first_name": data.get('first_name'),
        "last_name": data.get('last_name'),
        "phone": data.get('phone'),
        "email": email,
        "password": data.get('password'),
        "expenses": []
    }
    save_users_data(users)
    return True, "Registration successful."

def login_user(data, users):
    email = data.get('email')
    password = data.get('password')
    if email in users and users[email]['password'] == password:
        return True, {"first_name": users[email]['first_name']}
    return False, {}

if __name__ == '__main__':
    app.run(debug=True)
