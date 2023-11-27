import json
import os
from colorama import init, Fore, Style
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Initialize Colorama for colored output
init(autoreset=True)

USER_DATA_FILE = "users.json"

# Constants for categorization
FOOD_KEYWORDS = ["restaurant", "cafe", "supermarket", "grocery", "pizza", "diner"]
FUEL_KEYWORDS = ["gas", "fuel", "petrol", "service station"]
BILLS_KEYWORDS = ["bill", "utility", "electricity", "water", "internet", "phone"]
TRAVEL_KEYWORDS = ["airline", "travel", "uber", "taxi", "bus", "train", "hotel"]

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

def load_users():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as file:
            return json.load(file)
    else:
        return {"admin": {"first_name": "Admin", "last_name": "User", "phone": "0000000000", "email": "admin",
                          "password": "admin", "expenses": []}}

def save_users_data(users):
    with open(USER_DATA_FILE, 'w') as file:
        json.dump(users, file, indent=4)

def nlp_preprocess(text):
    tokens = word_tokenize(text)
    tokens = [word.lower() for word in tokens]
    tokens = [word for word in tokens if word not in stopwords.words('english')]
    return " ".join(tokens)

def categorize_transaction(description):
    processed_text = nlp_preprocess(description)

    if any(keyword in processed_text for keyword in FOOD_KEYWORDS):
        return "Food"
    elif any(keyword in processed_text for keyword in FUEL_KEYWORDS):
        return "Fuel"
    elif any(keyword in processed_text for keyword in BILLS_KEYWORDS):
        return "Bills"
    elif any(keyword in processed_text for keyword in TRAVEL_KEYWORDS):
        return "Travel"
    else:
        return "Other"

def add_expense(username, users):
    print("\nExample Transaction Description: 'Grocery shopping at Walmart'")
    date = input("Enter the date (YYYY-MM-DD): ")
    description = input("Enter the transaction description: ")
    amount = float(input("Enter the amount: "))
    category = categorize_transaction(description)
    expense = {"date": date, "description": description, "amount": amount, "category": category}
    users[username]["expenses"].append(expense)
    save_users_data(users)
    print("Expense added successfully.")

def view_expenses_by_date(username, users):
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

def view_user_info(username, users):
    print("\nYour Information:")
    for key, value in users[username].items():
        if key != "expenses":
            print(f"{key}: {value}")

def modify_user_info(username, users, is_admin=False):
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
            save_users_data(users)
            print_success(f"{info_to_modify} updated successfully.")
            if not is_admin:
                break  # If a regular user changes their email, log them out
        else:
            print_error("Invalid information type. Please try again.")

def select_user_for_admin(users):
    print("\nAvailable Users:")
    for username in users:
        if username != "admin":  # Exclude the admin account
            print(f"- {username}")
    print("Type 'back' to return to the previous menu.")

    selected_user = input("Enter the username of the user: ")
    if selected_user.lower() == 'back':
        return None
    elif selected_user in users and selected_user != "admin":
        return selected_user
    else:
        print_error("Invalid username or 'back' command selected.")
        return None

def delete_user_account(username, users):
    confirm = input("Are you sure you want to delete your account? (yes/no): ").lower()
    if confirm == 'yes':
        del users[username]
        save_users_data(users)
        print("Account deleted successfully.")


def register_user(users):
    while True:
        first_name = input("Enter the first name (or type 'back' to return): ")
        if first_name.lower() == 'back':
            return

        last_name = input("Enter the last name: ")
        phone = input("Enter the phone number: ")
        email = input("Enter the email address: ")
        if email.lower() == 'back':
            return

        if email in users:
            print_error("A user with this email already exists. Please try again with a new one.")
            continue

        password = input("Create a password: ")
        if password.lower() == 'back':
            return

        users[email] = {"first_name": first_name, "last_name": last_name, "phone": phone, "email": email, "password": password, "expenses": []}
        save_users_data(users)
        print_success("User registered successfully.")
        return

def delete_user(users):
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
        save_users_data(users)
        print_success("User deleted successfully.")
    else:
        print_error("Invalid username or 'back' command selected.")