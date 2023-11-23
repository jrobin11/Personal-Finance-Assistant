import pandas as pd
import json
import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Download necessary NLTK data
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

# File to store user data
USER_DATA_FILE = "users.json"


# Function to load users data
def load_users():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as file:
            return json.load(file)
    else:
        return {"admin": {"first_name": "Admin", "last_name": "User", "phone": "0000000000", "email": "admin",
                          "password": "admin", "expenses": []}}


# Function to save users data
def save_users_data():
    with open(USER_DATA_FILE, 'w') as file:
        json.dump(users, file, indent=4)


# Initialize users data
users = load_users()


# Basic NLP preprocessing
def nlp_preprocess(text):
    tokens = word_tokenize(text)
    tokens = [word.lower() for word in tokens]
    tokens = [word for word in tokens if word not in stopwords.words('english')]
    return " ".join(tokens)


def categorize_transaction(description):
    processed_text = nlp_preprocess(description)
    food_keywords = ["restaurant", "cafe", "supermarket", "grocery", "pizza", "diner"]
    fuel_keywords = ["gas", "fuel", "petrol", "service station"]
    bills_keywords = ["bill", "utility", "electricity", "water", "internet", "phone"]
    travel_keywords = ["airline", "travel", "uber", "taxi", "bus", "train", "hotel"]
    if any(keyword in processed_text for keyword in food_keywords):
        return "Food"
    elif any(keyword in processed_text for keyword in fuel_keywords):
        return "Fuel"
    elif any(keyword in processed_text for keyword in bills_keywords):
        return "Bills"
    elif any(keyword in processed_text for keyword in travel_keywords):
        return "Travel"
    else:
        return "Other"


def register_user():
    first_name = input("Enter your first name: ")
    last_name = input("Enter your last name: ")
    phone = input("Enter your phone number: ")
    email = input("Enter your email address: ")
    password = input("Create a password: ")
    username = email  # Using email as the username for simplicity
    if username in users:
        print("A user with this email already exists.")
        return
    users[username] = {"first_name": first_name, "last_name": last_name, "phone": phone, "email": email,
                       "password": password, "expenses": []}
    print("User registered successfully.")


def login():
    username = input("Enter your username (email): ")
    password = input("Enter your password: ")
    user = users.get(username)
    if user and user["password"] == password:
        return username
    else:
        print("Invalid username or password.")
        return None


def add_expense(username):
    date = input("Enter the date (YYYY-MM-DD): ")
    description = input("Enter the transaction description: ")
    amount = float(input("Enter the amount: "))
    category = categorize_transaction(description)
    expense = {"date": date, "description": description, "amount": amount, "category": category}
    users[username]["expenses"].append(expense)
    save_users_data()
    print("Expense added successfully.")


def display_expenses(username):
    expenses = users[username]["expenses"]
    if expenses:
        df = pd.DataFrame(expenses)
        print(df)
    else:
        print("No expenses to display.")


def user_actions(username):
    while True:
        print("\nOptions: Add Expense, View Expenses, Quit")
        action = input("What would you like to do? ").lower()
        if action == "add expense":
            add_expense(username)
        elif action == "view expenses":
            display_expenses(username)
        elif action == "quit":
            break
        else:
            print("Invalid option.")


def admin_actions():
    while True:
        print("\nAdmin Options: Create User, Delete User, View Users, Modify User, Quit")
        action = input("What would you like to do? ").lower()

        if action == "create user":
            register_user()
        elif action == "delete user":
            username = input("Enter the username of the user to delete: ")
            if username in users and username != "admin":
                del users[username]
                save_users_data()
                print("User deleted successfully.")
            else:
                print("Invalid username or cannot delete admin.")
        elif action == "view users":
            for username, user_info in users.items():
                print(f"Username: {username}, Full Name: {user_info['first_name']} {user_info['last_name']}")
        elif action == "modify user":
            modify_user()
            save_users_data()
        elif action == "quit":
            break
        else:
            print("Invalid option.")


def modify_user():
    username = input("Enter the username of the user to modify: ")
    if username in users and username != "admin":
        print("Modifying User:", username)
        users[username]['first_name'] = input("Enter new first name: ")
        users[username]['last_name'] = input("Enter new last name: ")
        users[username]['phone'] = input("Enter new phone number: ")
        users[username]['email'] = input("Enter new email address: ")
        users[username]['password'] = input("Enter new password: ")
        save_users_data()
        print("User details updated successfully.")
    else:
        print("Invalid username or cannot modify admin.")


def main():
    print("Welcome to the Personal Finance Assistant\n")
    while True:
        user_type = input("Are you a new or existing user? (New/Existing/Quit): ").strip().lower()
        if user_type == "new":
            register_user()
        elif user_type == "existing":
            username = login()
            if username:
                if username == "admin":
                    admin_actions()
                else:
                    user_actions(username)
        elif user_type == "quit":
            print("Exiting program.")
            break
        else:
            print("Invalid option. Please enter 'New', 'Existing', or 'Quit'.\n")


if __name__ == "__main__":
    main()
