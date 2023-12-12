import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from utils import load_users, save_users_data
import style_utils
# Import necessary functions from utils or other modules


def admin_dashboard(root):
    admin_window = tk.Toplevel(root)
    admin_window.title("Admin Dashboard")
    admin_window.configure(bg=style_utils.BG_COLOR)
    admin_window.geometry("400x300")

    # Configure grid layout
    admin_window.grid_columnconfigure(0, weight=1)

    # Place the buttons at different rows
    ttk.Button(admin_window, text="Create User", command=lambda: create_user_gui(root), style="TButton").grid(row=0, column=0, padx=20, pady=10, sticky="ew")
    ttk.Button(admin_window, text="Delete User", command=lambda: delete_user_gui(root), style="TButton").grid(row=1, column=0, padx=20, pady=10, sticky="ew")
    ttk.Button(admin_window, text="View Users", command=lambda: view_users_gui(root), style="TButton").grid(row=2, column=0, padx=20, pady=10, sticky="ew")
    ttk.Button(admin_window, text="Modify User", command=lambda: modify_user_gui(root), style="TButton").grid(row=3, column=0, padx=20, pady=10, sticky="ew")
    ttk.Button(admin_window, text="Logout", command=admin_window.destroy, style="TButton").grid(row=4, column=0, padx=20, pady=10, sticky="ew")


# Implement the functions called by each button
def create_user_gui(root):
    create_user_window = tk.Toplevel(root)
    create_user_window.title("Create New User")

    # Entry fields for user information
    labels = ["First Name", "Last Name", "Phone", "Email", "Password"]
    entries = {}

    for i, label in enumerate(labels):
        tk.Label(create_user_window, text=label).grid(row=i, column=0)
        entry = tk.Entry(create_user_window)
        entry.grid(row=i, column=1)
        entries[label] = entry

    # Submit Button
    tk.Button(create_user_window, text="Create User",
              command=lambda: submit_new_user(entries, create_user_window)).grid(row=len(labels), columnspan=2)

def submit_new_user(entries, window):
    # Extracting the data from the entries
    user_data = {label: entry.get() for label, entry in entries.items()}
    
    # Validate the data
    if not all(user_data.values()):
        messagebox.showerror("Error", "All fields are required.", parent=window)
        return

    users = load_users()

    # Check if the email already exists
    if user_data["Email"] in users:
        messagebox.showerror("Error", "A user with this email already exists.", parent=window)
        return

    # Adding the new user
    new_user = {
        "first_name": user_data["First Name"],
        "last_name": user_data["Last Name"],
        "phone": user_data["Phone"],
        "email": user_data["Email"],
        "password": user_data["Password"],
        "expenses": []
    }

    users[user_data["Email"]] = new_user
    save_users_data(users)

    messagebox.showinfo("Success", "User created successfully.", parent=window)
    window.destroy()

def delete_user_gui(root):
    delete_user_window = tk.Toplevel(root)
    delete_user_window.title("Delete User")

    # Load users
    users = load_users()

    # Create a dropdown to select a user
    tk.Label(delete_user_window, text="Select User:").grid(row=0, column=0)
    selected_user = tk.StringVar()
    user_dropdown = ttk.Combobox(delete_user_window, textvariable=selected_user)
    user_dropdown['values'] = [email for email in users.keys() if email != 'admin']  # Exclude admin
    user_dropdown.grid(row=0, column=1)

    # Delete Button
    tk.Button(delete_user_window, text="Delete User",
              command=lambda: confirm_and_delete_user(selected_user.get(), users, delete_user_window)).grid(row=1, columnspan=2)

def confirm_and_delete_user(email, users, window):
    if not email:
        messagebox.showerror("Error", "No user selected.", parent=window)
        return

    confirm = messagebox.askyesno("Confirm", f"Are you sure you want to delete the user {email}?", parent=window)
    if confirm:
        if email in users:
            del users[email]
            save_users_data(users)
            messagebox.showinfo("Success", f"User {email} deleted successfully.", parent=window)
            window.destroy()
        else:
            messagebox.showerror("Error", "User not found.", parent=window)

def view_users_gui(root):
    users_window = tk.Toplevel(root)
    users_window.title("View Users")

    # Text widget to display users
    users_text = tk.Text(users_window, height=15, width=50)
    users_text.pack()

    # Load users and display them
    users = load_users()
    for email, user_info in users.items():
        user_details = f"Email: {email}\n"
        for key, value in user_info.items():
            if key != "password":  # Optionally exclude password for security
                user_details += f"  {key.capitalize()}: {value}\n"
        user_details += "\n"
        users_text.insert(tk.END, user_details)

    # Disable editing of the text widget
    users_text.config(state=tk.DISABLED)

def modify_user_gui(root):
    modify_user_window = tk.Toplevel(root)
    modify_user_window.title("Modify User Information")

    # Load users
    users = load_users()

    # Create a dropdown to select a user
    tk.Label(modify_user_window, text="Select User:").grid(row=0, column=0)
    selected_user = tk.StringVar()
    user_dropdown = ttk.Combobox(modify_user_window, textvariable=selected_user, state="readonly")
    user_dropdown['values'] = list(users.keys())
    user_dropdown.grid(row=0, column=1)

    # Entry fields for user information
    labels = ["First Name", "Last Name", "Phone", "Email"]
    entries = {label: tk.Entry(modify_user_window) for label in labels}
    for i, (label, entry) in enumerate(entries.items(), start=1):
        tk.Label(modify_user_window, text=label).grid(row=i, column=0)
        entry.grid(row=i, column=1)

    # Update Button
    tk.Button(modify_user_window, text="Update User",
              command=lambda: submit_modified_user(selected_user.get(), entries, users, modify_user_window)).grid(row=len(labels) + 1, columnspan=2)

def submit_modified_user(email, entries, users, window):
    if email not in users:
        messagebox.showerror("Error", "User not found.", parent=window)
        return

    # Extracting the data from the entries
    user_data = {label: entry.get() for label, entry in entries.items()}
    
    # Validate the data
    if not all(user_data.values()):
        messagebox.showerror("Error", "All fields are required.", parent=window)
        return

    # Updating the user's information
    users[email].update({
        "first_name": user_data["First Name"],
        "last_name": user_data["Last Name"],
        "phone": user_data["Phone"],
        "email": user_data["Email"]  # Handle email change carefully
    })

    save_users_data(users)

    messagebox.showinfo("Success", f"User {email} updated successfully.", parent=window)
    window.destroy()

