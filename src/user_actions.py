from utils import print_menu, add_expense, view_expenses_by_date, view_user_info, modify_user_info, delete_user_account

def user_profile_actions(username, users):
    while True:
        user_options = ["Add Expense", "View Expenses", "View Info", "Modify Info", "Delete Account", "Logout"]
        print_menu("User Options", user_options)
        action = input("What would you like to do? ").lower()

        if action == "add expense":
            add_expense(username, users)
        elif action == "view expenses":
            view_expenses_by_date(username, users)
        elif action == "view info":
            view_user_info(username, users)
        elif action == "modify info":
            modify_user_info(username, users)
        elif action == "delete account":
            delete_user_account(username, users)
            break  # Exit after account deletion
        elif action == "logout":
            print("Logged out successfully.")
            break
        else:
            print("Invalid option. Please try again.")
