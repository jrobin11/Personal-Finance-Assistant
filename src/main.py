import nltk
from colorama import Fore, Style

from user_actions import user_profile_actions
from admin_actions import admin_actions
from utils import print_heading, print_success, print_error, load_users, register_user

# Download necessary NLTK data
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)


def login(users):
    while True:
        username = input("Enter your username (email) or type 'back' to return: ")
        if username.lower() == 'back':
            return None

        if username not in users:
            print_error("Username does not exist. Please try again.")
            continue

        password = input("Enter your password: ")
        if password.lower() == 'back':
            return None

        if users[username]["password"] == password:
            return username
        else:
            print_error("Invalid password. Please try again.")


def main():
    users = load_users()
    print_heading("Welcome to the Personal Finance Assistant")

    while True:
        user_type = input(
            "\nAre you a " + Fore.CYAN + "New" + Style.RESET_ALL + ", " + Fore.CYAN + "Existing" + Style.RESET_ALL + " user, or " + Fore.CYAN + "Admin" + Style.RESET_ALL + "? (New/Existing/Admin/Quit): ").strip().lower()
        if user_type == "new":
            if not register_user(users):
                continue
        elif user_type == "existing":
            username = login(users)
            if username:
                user_profile_actions(username, users)
        elif user_type == "admin":
            admin_username = input("Enter admin username: ")
            if admin_username.lower() == 'back':
                continue
            admin_password = input("Enter admin password: ")
            if admin_password.lower() == 'back':
                continue
            if admin_username in users and users[admin_username]["password"] == admin_password:
                admin_actions(users)
            else:
                print_error("Invalid admin credentials.")
        elif user_type == "quit":
            print_success("Exiting program.")
            break
        else:
            print_error("Invalid option. Please enter 'New', 'Existing', 'Admin', or 'Quit'.\n")


if __name__ == "__main__":
    main()
