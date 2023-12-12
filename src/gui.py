import tkinter as tk
from tkinter import ttk
import style_utils
import user_actions
import admin_actions
from tkinter import messagebox
from utils import load_users, save_users_data

# Function definitions for button commands
def on_new_user():
    new_user_window = tk.Toplevel(root)
    new_user_window.title("Register New User")

    # Form fields
    tk.Label(new_user_window, text="First Name").grid(row=0, column=0)
    first_name_entry = tk.Entry(new_user_window)
    first_name_entry.grid(row=0, column=1)

    tk.Label(new_user_window, text="Last Name").grid(row=1, column=0)
    last_name_entry = tk.Entry(new_user_window)
    last_name_entry.grid(row=1, column=1)

    tk.Label(new_user_window, text="Phone").grid(row=2, column=0)
    phone_entry = tk.Entry(new_user_window)
    phone_entry.grid(row=2, column=1)

    tk.Label(new_user_window, text="Email").grid(row=3, column=0)
    email_entry = tk.Entry(new_user_window)
    email_entry.grid(row=3, column=1)

    tk.Label(new_user_window, text="Password").grid(row=4, column=0)
    password_entry = tk.Entry(new_user_window, show="*")
    password_entry.grid(row=4, column=1)

    # Submit button
    tk.Button(new_user_window, text="Register", command=lambda: register_user(
        first_name_entry.get(),
        last_name_entry.get(),
        phone_entry.get(),
        email_entry.get(),
        password_entry.get(),
        new_user_window
    )).grid(row=5, column=0, columnspan=2)

def on_existing_user():
    login_window = tk.Toplevel(root)
    login_window.title("Login")

    # Email Entry
    tk.Label(login_window, text="Email:").grid(row=0, column=0)
    email_entry = tk.Entry(login_window)
    email_entry.grid(row=0, column=1)

    # Password Entry
    tk.Label(login_window, text="Password:").grid(row=1, column=0)
    password_entry = tk.Entry(login_window, show="*")
    password_entry.grid(row=1, column=1)

    # Login Button
    tk.Button(login_window, text="Login", command=lambda: login_user(email_entry.get(), password_entry.get(), login_window)).grid(row=2, column=0, columnspan=2)

def on_admin_login(admin_window):
    # Admin login credentials (for simplicity, hardcoded here)
    ADMIN_USERNAME = "admin"
    ADMIN_PASSWORD = "admin"

    username_entry = tk.Entry(admin_window)
    password_entry = tk.Entry(admin_window, show="*")

    def verify_admin_login():
        if username_entry.get() == ADMIN_USERNAME and password_entry.get() == ADMIN_PASSWORD:
            messagebox.showinfo("Login Successful", "Admin login successful.")
            admin_window.destroy()
            admin_actions.admin_dashboard(root)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    tk.Label(admin_window, text="Admin Username:").pack()
    username_entry.pack()
    tk.Label(admin_window, text="Admin Password:").pack()
    password_entry.pack()
    tk.Button(admin_window, text="Login", command=verify_admin_login).pack()

def on_admin():
    admin_login_window = tk.Toplevel(root)
    admin_login_window.title("Admin Login")
    on_admin_login(admin_login_window)


# Setup main window
def setup_main_window():
    root = tk.Tk()
    root.title("Personal Finance Assistant")
    root.configure(bg=style_utils.BG_COLOR)
    root.geometry("500x300")  # Adjust the size as needed
    

    # Grid layout for better alignment
    root.grid_columnconfigure(0, weight=1)

    style_utils.configure_styles()

    ttk.Label(root, text="Personal Finance Assistant", style="Header.TLabel").grid(row=0, column=0, pady=20, sticky="ew")
    
    ttk.Button(root, text="New Here?", command=on_new_user, style="TButton").grid(row=1, column=0, padx=20, pady=10, sticky="ew")
    ttk.Button(root, text="Login", command=on_existing_user, style="TButton").grid(row=2, column=0, padx=20, pady=10, sticky="ew")
    ttk.Button(root, text="Admin Login", command=on_admin, style="TButton").grid(row=3, column=0, padx=20, pady=10, sticky="ew")
    ttk.Button(root, text="Quit", command=root.destroy, style="TButton").grid(row=4, column=0, padx=20, pady=10, sticky="ew")

    return root

    

# Function to handle user registration
def register_user(first_name, last_name, phone, email, password, window):
    # Check if any field is empty
    if not all([first_name, last_name, email, password]):
        messagebox.showerror("Error", "All fields are required")
        return

    # Load existing users
    users = load_users()

    # Check if email already exists
    if email in users:
        messagebox.showerror("Error", "Email already exists")
        return

    # Add new user to users dictionary
    users[email] = {
        "first_name": first_name,
        "last_name": last_name,
        "phone": phone,
        "email": email,
        "password": password,
        "expenses": []
    }

    # Save users data
    save_users_data(users)

    # Confirmation message
    messagebox.showinfo("Success", "User registered successfully")
    window.destroy()

def login_user(email, password, login_window):
    users = load_users()
    if email in users and users[email]["password"] == password:
        messagebox.showinfo("Login Successful", "You are now logged in.")
        login_window.destroy()  # Close the login window
        open_user_dashboard(email)  # Open the user dashboard
    else:
        messagebox.showerror("Login Failed", "Invalid email or password")

def open_user_dashboard(username):
    dashboard = tk.Toplevel(root)
    dashboard.title("User Dashboard - " + username)

    tk.Button(dashboard, text="Add Expense", command=lambda: user_actions.add_expense_gui(dashboard, username)).pack()
    tk.Button(dashboard, text="View Expenses", command=lambda: user_actions.view_expenses_gui(dashboard, username)).pack()
    tk.Button(dashboard, text="View Info", command=lambda: user_actions.view_info_gui(dashboard, username)).pack()
    tk.Button(dashboard, text="Modify Info", command=lambda: user_actions.modify_info_gui(dashboard, username)).pack()
    tk.Button(dashboard, text="Show Insights", command=lambda: user_actions.show_insights_gui(dashboard, username)).pack()
    tk.Button(dashboard, text="Delete Account", command=lambda: user_actions.delete_account_gui(dashboard, username)).pack()
    tk.Button(dashboard, text="Logout", command=dashboard.destroy).pack()

if __name__ == "__main__":
    root = setup_main_window()
    root.mainloop()
