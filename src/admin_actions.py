from utils import print_menu, select_user_for_admin, view_user_info, modify_user_info, delete_user, register_user, print_warning, print_success, print_error

def admin_actions(users):
    while True:
        admin_options = ["Create User", "Delete User", "View Users", "Modify User", "Logout"]
        print_menu("Admin Options", admin_options)
        action = input("What would you like to do? ").lower()

        if action == "create user":
            register_user(users)
        elif action == "delete user":
            delete_user(users)
        elif action == "view users":
            selected_user = select_user_for_admin(users)
            if selected_user:
                view_user_info(selected_user, users)
            else:
                print_warning("Returning to admin menu.")
        elif action == "modify user":
            selected_user = select_user_for_admin(users)
            if selected_user:
                modify_user_info(selected_user, users, is_admin=True)
            else:
                print_warning("Returning to admin menu.")
        elif action == "logout":
            print_success("Logged out successfully.")
            break
        else:
            print_error("Invalid option.")
