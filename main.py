import pandas as pd
import json
import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

from colorama import init, Fore, Style

# Initialize Colorama for colored output
init(autoreset=True)

# Download necessary NLTK data
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

# File to store user data
USER_DATA_FILE = "users.json"

def print_heading(text):
    print(Fore.CYAN + Style.BRIGHT + text + Style.RESET_ALL)

def print_success(text):
    print(Fore.GREEN + text + Style.RESET_ALL)

def print_error(text):
    print(Fore.RED + text + Style.RESET_ALL)

def print_warning(text):
    print(Fore.YELLOW + text + Style.RESET_ALL)

def print_menu(title, options):
    print(Style.BRIGHT + Fore.BLUE + f"\n{title}" + Style.RESET_ALL)
    for option in options:
        print(Fore.YELLOW + f"- {option}" + Style.RESET_ALL)

def format_expense(expense):
    return Fore.GREEN + f"- {expense['description']} (${expense['amount']}), Category: {expense['category']}" + Style.RESET_ALL

def main():
    print_heading("Welcome to the Personal Finance Assistant")
    while True:
        user_type = input("\nAre you a " + Fore.CYAN + "New" + Style.RESET_ALL + ", " + Fore.CYAN + "Existing" + Style.RESET_ALL + " user, or " + Fore.CYAN + "Admin" + Style.RESET_ALL + "? (New/Existing/Admin/Quit): ").strip().lower()
        if user_type == "new":
            if not register_user():
                continue
        elif user_type == "existing":
            username = login()
            if username:
                user_profile_actions(username)
        elif user_type == "admin":
            admin_username = input("Enter admin username: ")
            if admin_username.lower() == 'back':
                continue
            admin_password = input("Enter admin password: ")
            if admin_password.lower() == 'back':
                continue
            if admin_username in users and users[admin_username]["password"] == admin_password:
                admin_actions()
            else:
                print_error("Invalid admin credentials.")
        elif user_type == "quit":
            print_success("Exiting program.")
            break
        else:
            print_error("Invalid option. Please enter 'New', 'Existing', 'Admin', or 'Quit'.\n")

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
    while True:
        first_name = input("Enter your first name (or type 'back' to return): ")
        if first_name.lower() == 'back':
            return False

        last_name = input("Enter your last name: ")
        phone = input("Enter your phone number: ")

        email = input("Enter your email address: ")
        if email.lower() == 'back':
            return False

        if email in users:
            print("A user with this email already exists. Please try again with a new one.")
            continue

        password = input("Create a password: ")
        if password.lower() == 'back':
            return False

        users[email] = {"first_name": first_name, "last_name": last_name, "phone": phone, "email": email,
                        "password": password, "expenses": []}
        save_users_data()
        print("User registered successfully.")
        return True
def login():
    while True:
        username = input("Enter your username (email) or type 'back' to return: ")
        if username.lower() == 'back':
            return None

        password = input("Enter your password: ")
        if password.lower() == 'back':
            return None

        user = users.get(username)
        if user and user["password"] == password:
            return username
        else:
            print("Invalid username or password.")

def delete_user():
    print("\nAvailable Users to Delete:")
    for username in users:
        if username != "admin":  # Exclude the admin account
            print(f"- {username}")
    print("Type 'back' to return to the previous menu.")
    selected_user = input("Enter the username of the user to delete: ")

    if selected_user.lower() == 'back':
        return
    elif selected_user in users and selected_user != "admin":
        del users[selected_user]
        save_users_data()
        print("User deleted successfully.")
    else:
        print("Invalid username or 'back' command selected.")

def user_profile_actions(username):
    while True:
        user_options = ["Add Expense", "View Expenses", "View Info", "Modify Info", "Delete Account", "Logout"]
        print_menu("User Options", user_options)
        action = input("What would you like to do? ").lower()

        if action == "add expense":
            add_expense(username)
        elif action == "view expenses":
            view_expenses_by_date(username)
        elif action == "view info":
            view_user_info(username)
        elif action == "modify info":
            modify_user_info(username)
        elif action == "delete account":
            delete_user_account(username)
            break  # Exit after account deletion
        elif action == "logout":
            print("Logged out successfully.")
            break
        else:
            print("Invalid option. Please try again.")

def view_expenses_by_date(username):
    if not users[username]["expenses"]:
        print_warning("No expenses recorded.")
        return

    expenses_by_date = {}
    for expense in users[username]["expenses"]:
        expenses_by_date.setdefault(expense['date'], []).append(expense)

    for date, expenses in sorted(expenses_by_date.items()):
        print(Style.BRIGHT + Fore.BLUE + f"\nExpenses for {date}:" + Style.RESET_ALL)
        for expense in expenses:
            print(format_expense(expense))


def view_user_info(username):
    print("\nYour Information:")
    for key, value in users[username].items():
        if key != "expenses":
            print(f"{key}: {value}")

def modify_user_info(username, is_admin=False):
    original_username = username
    while True:
        print(f"\nModifying User: {username}")
        for key, value in users[username].items():
            if key != "expenses":  # Exclude expenses from modification options
                print(f"{key}: {value}")

        info_to_modify = input("\nWhich information do you want to modify? (Type 'back' to return): ").strip()

        if info_to_modify.lower() == 'back':
            print("Returning to previous menu.")
            break
        elif info_to_modify in users[username] and info_to_modify != "expenses":
            new_value = input(f"Enter new value for {info_to_modify}: ")
            if info_to_modify == "email":
                if new_value in users:
                    print_warning("This email is already taken. Please try a different one.")
                    continue
                users[new_value] = users.pop(original_username)
                username = new_value  # Update username in case of further modifications
            users[username][info_to_modify] = new_value
            save_users_data()
            print_success(f"{info_to_modify} updated successfully.")
            if not is_admin:
                break  # If a regular user changes their email, log them out
        else:
            print_error("Invalid information type. Please try again.")

def delete_user_account(username):
    confirm = input("Are you sure you want to delete your account? (yes/no): ").lower()
    if confirm == 'yes':
        del users[username]
        save_users_data()
        print("Account deleted successfully.")
def add_expense(username):
    print("\nExample Transaction Description: 'Grocery shopping at Walmart'")
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
        print_menu("Admin Options", ["Create User", "Delete User", "View Users", "Modify User", "Logout"])
        action = input("What would you like to do? ").lower()

        if action == "create user":
            register_user()
        elif action == "delete user":
            delete_user()
        elif action == "view users":
            selected_user = select_user_for_admin()
            if selected_user:
                view_user_info(selected_user)
            else:
                print_warning("Returning to admin menu.")
        elif action == "modify user":
            selected_user = select_user_for_admin()
            if selected_user:
                modify_user_info(selected_user, is_admin=True)
            else:
                print_warning("Returning to admin menu.")
        elif action == "logout":
            print_success("Logged out successfully.")
            break
        else:
            print_error("Invalid option.")

def select_user_for_admin():
    print("\nAvailable Users:")
    for username in users:
        if username != "admin":  # Exclude the admin account
            print(f"- {username}")
    print("Type 'back' to return to the previous menu.")
    selected_user = input("Enter the username of the user to view: ")

    if selected_user.lower() == 'back':
        return None
    elif selected_user in users and selected_user != "admin":
        return selected_user
    else:
        print("Invalid username or 'back' command selected.")
        return None

def modify_user():
    # List all users for the admin to choose
    print("\nAvailable Users:")
    for username in users:
        if username != "admin":  # Exclude the admin account
            print(f"- {username}")
    print("Type 'back' to return to the previous menu.")
    selected_user = input("Enter the username of the user to modify: ")

    if selected_user.lower() == 'back':
        return
    elif selected_user in users and selected_user != "admin":
        while True:
            # Display user information
            print(f"\nSelected User: {selected_user}")
            for key, value in users[selected_user].items():
                if key != "expenses":  # Exclude expenses from modification options
                    print(f"{key}: {value}")

            print("\nWhich information do you want to modify? (Type 'back' to return)")
            info_to_modify = input("Enter the information type (first_name, last_name, phone, email, password): ").strip()

            if info_to_modify.lower() == 'back':
                break
            elif info_to_modify in users[selected_user] and info_to_modify != "expenses":
                new_value = input(f"Enter new value for {info_to_modify}: ")
                users[selected_user][info_to_modify] = new_value
                save_users_data()
                print(f"{info_to_modify} updated successfully.")
            else:
                print("Invalid information type. Please try again.")
    else:
        print("Invalid username or 'back' command selected.")


if __name__ == "__main__":
    main()
