import tkinter as tk
from tkinter import ttk
import style_utils
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from matplotlib.figure import Figure
from constants import CATEGORY_KEYWORDS
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import simpledialog, messagebox
from utils import load_users, save_users_data, add_expense, view_expenses_by_date, modify_user_info

nltk.download('punkt')
nltk.download('stopwords')

def add_expense_gui(parent, username):
    # Create a new window for adding an expense
    add_expense_window = tk.Toplevel(parent)
    style_utils.configure_styles()
    add_expense_window.title("Add Expense")

    # Date Entry
    tk.Label(add_expense_window, text="Date (YYYY-MM-DD):").grid(row=0, column=0)
    date_entry = tk.Entry(add_expense_window)
    date_entry.grid(row=0, column=1)

    # Description Entry
    tk.Label(add_expense_window, text="Description:").grid(row=1, column=0)
    description_entry = tk.Entry(add_expense_window)
    description_entry.grid(row=1, column=1)

    # Amount Entry
    tk.Label(add_expense_window, text="Amount:").grid(row=2, column=0)
    amount_entry = tk.Entry(add_expense_window)
    amount_entry.grid(row=2, column=1)

    # Submit Button
    tk.Button(add_expense_window, text="Add Expense", 
              command=lambda: submit_expense(username, date_entry.get(), description_entry.get(), amount_entry.get(), add_expense_window)).grid(row=4, column=0, columnspan=2)

def categorize_expense(description):
    # Tokenize and lower case the description
    tokens = word_tokenize(description.lower())
    filtered_words = [word for word in tokens if word not in stopwords.words('english')]

    # Check against keywords from constants.py
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword in filtered_words for keyword in keywords):
            return category
    return "Other"

def submit_expense(username, date, description, amount, window):
    try:
        amount = float(amount)  # Convert amount to float
    except ValueError:
        messagebox.showerror("Invalid Input", "Amount must be a number.", parent=window)
        return

    # Automatic categorization
    category = categorize_expense(description)

    # Load existing users data
    users = load_users()

    # Add the expense
    expense = {"date": date, "description": description, "amount": amount, "category": category}
    users[username]["expenses"].append(expense)

    # Save the updated users data
    save_users_data(users)

    messagebox.showinfo("Success", "Expense added successfully.", parent=window)
    window.destroy()  # Close the add expense window



def view_expenses_gui(parent, username):
    users = load_users()
    expenses = view_expenses_by_date(username, users)

    # Create a new window to display expenses
    expenses_window = tk.Toplevel(parent)
    style_utils.configure_styles()
    expenses_window.title(f"Expenses for {username}")

    # Text widget to display expenses
    expenses_text = tk.Text(expenses_window, height=15, width=50)
    expenses_text.pack()

    # Populate the text widget with expenses
    for date, expenses_list in expenses.items():
        expenses_text.insert(tk.END, f"Date: {date}\n")
        for expense in expenses_list:
            expense_details = f"  Description: {expense['description']}, Amount: ${expense['amount']}, Category: {expense['category']}\n"
            expenses_text.insert(tk.END, expense_details)
        expenses_text.insert(tk.END, "\n")

    # Disable editing of the text widget
    expenses_text.config(state=tk.DISABLED)


def view_info_gui(parent, username):
    users = load_users()
    user_info = users.get(username, {})
    info_str = "\n".join([f"{key}: {value}" for key, value in user_info.items() if key != 'expenses'])
    messagebox.showinfo("User Info", info_str, parent=parent)
    style_utils.configure_styles()

def modify_info_gui(parent, username):
    # Load the user's current information
    users = load_users()
    user_info = users.get(username, {})

    # Create a new window for modifying user information
    modify_info_window = tk.Toplevel(parent)
    style_utils.configure_styles()
    modify_info_window.title("Modify User Information")

    # First Name Entry
    tk.Label(modify_info_window, text="First Name:").grid(row=0, column=0)
    first_name_entry = tk.Entry(modify_info_window)
    first_name_entry.insert(0, user_info.get("first_name", ""))
    first_name_entry.grid(row=0, column=1)

    # Last Name Entry
    tk.Label(modify_info_window, text="Last Name:").grid(row=1, column=0)
    last_name_entry = tk.Entry(modify_info_window)
    last_name_entry.insert(0, user_info.get("last_name", ""))
    last_name_entry.grid(row=1, column=1)

    # Phone Entry
    tk.Label(modify_info_window, text="Phone:").grid(row=2, column=0)
    phone_entry = tk.Entry(modify_info_window)
    phone_entry.insert(0, user_info.get("phone", ""))
    phone_entry.grid(row=2, column=1)

    # Email Entry (email is typically not changeable, but you can include it if it makes sense for your application)
    tk.Label(modify_info_window, text="Email:").grid(row=3, column=0)
    email_entry = tk.Entry(modify_info_window)
    email_entry.insert(0, user_info.get("email", ""))
    email_entry.grid(row=3, column=1)

    # Submit Button
    tk.Button(modify_info_window, text="Update Info", 
              command=lambda: submit_modified_info(username, first_name_entry.get(), last_name_entry.get(), phone_entry.get(), email_entry.get(), modify_info_window)).grid(row=4, column=0, columnspan=2)

def submit_modified_info(username, first_name, last_name, phone, email, window):
    users = load_users()

    # Here you can add checks, e.g., if the email is already taken by another user
    # ...

    # Update user's information
    users[username]["first_name"] = first_name
    users[username]["last_name"] = last_name
    users[username]["phone"] = phone
    users[username]["email"] = email  # Only update if email change is allowed

    save_users_data(users)

    messagebox.showinfo("Success", "User information updated successfully.", parent=window)
    window.destroy()  # Close the modify info window


def show_insights_gui(parent, username):
    users = load_users()
    expenses = users.get(username, {}).get("expenses", [])
    style_utils.configure_styles()
    # Calculate the total expenses per category
    category_totals = {}
    for expense in expenses:
        category = expense['category']
        amount = expense['amount']
        category_totals[category] = category_totals.get(category, 0) + amount

    # Create a new window for showing insights
    insights_window = tk.Toplevel(parent)
    insights_window.title("Spending Insights")

    # Create a pie chart if there are expenses
    if category_totals:
        fig = Figure(figsize=(6, 6), dpi=100)
        ax = fig.add_subplot(111)

        categories = list(category_totals.keys())
        amounts = list(category_totals.values())
        ax.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140)
        ax.set_title('Expenses by Category')

        # Adding the pie chart to the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=insights_window)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack()

        # Add suggestions
        suggestions = analyze_expenses_for_suggestions(category_totals)
        tk.Label(insights_window, text="Suggestions to Improve Spending Habits:", font=('Helvetica', 12, 'bold')).pack()
        tk.Label(insights_window, text=suggestions).pack()
    else:
        tk.Label(insights_window, text="No expenses recorded.").pack()

def analyze_expenses_for_suggestions(category_totals):
    suggestions = []

    # Basic comparison checks
    if category_totals.get("Food", 0) > category_totals.get("Savings", 0):
        suggestions.append("You're spending more on food than savings. Consider allocating more budget to savings.")

    if category_totals.get("Entertainment", 0) > category_totals.get("Education", 0):
        suggestions.append("Entertainment expenses exceed educational. Consider investing more in education and learning.")

    # Check for high spending on non-essentials
    luxury_categories = ["Entertainment", "Shopping", "Travel"]
    essential_categories = ["Groceries", "Bills", "Health", "Transportation"]
    luxury_spending = sum(category_totals.get(cat, 0) for cat in luxury_categories)
    essential_spending = sum(category_totals.get(cat, 0) for cat in essential_categories)

    if luxury_spending > essential_spending:
        suggestions.append("Your spending on luxuries exceeds essentials. Reviewing your budget priorities might be beneficial.")

    # High spending on fuel and transportation
    if category_totals.get("Fuel", 0) > category_totals.get("Transportation", 0) * 0.3:
        suggestions.append("Fuel costs are a significant part of your transportation budget. Consider more fuel-efficient travel options.")

    # Check if health expenses are unusually low - might indicate underinvestment in health
    if category_totals.get("Health", 0) < category_totals.get("Entertainment", 0) * 0.5:
        suggestions.append("Health-related expenses are relatively low. Ensure you're not neglecting medical needs or health insurance.")

    # High childcare expenses might indicate a need for budget reevaluation
    if category_totals.get("Child Care", 0) > sum(category_totals.values()) * 0.2:
        suggestions.append("Child care is a large part of your expenses. Exploring more cost-effective childcare options could be beneficial.")

    # High utility bills could indicate energy inefficiency
    if category_totals.get("Bills", 0) > sum(category_totals.values()) * 0.15:
        suggestions.append("Your utility bills are a significant part of your expenses. Consider ways to reduce energy and water usage.")

    # Add more checks as needed

    # Combine all suggestions or return a default message if no specific advice
    return " \n".join(suggestions) if suggestions else "Your spending habits are on track!"

def delete_user_account(username, users):
    """
    Deletes a user account from the users dictionary.
    
    :param username: The username of the account to be deleted.
    :param users: The dictionary containing user data.
    """
    if username in users:
        del users[username]
    else:
        raise ValueError("User not found")

def delete_account_gui(parent, username):
    """
    Opens a confirmation dialog and deletes the user account if confirmed.
    
    :param parent: The parent Tkinter widget (typically the user's dashboard window).
    :param username: The username of the account to be deleted.
    """
    users = load_users()
    confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete your account?", parent=parent)
    if confirm:
        try:
            delete_user_account(username, users)
            save_users_data(users)
            messagebox.showinfo("Deleted", "Your account has been deleted.", parent=parent)
            parent.destroy()  # Close the dashboard window
        except ValueError as e:
            messagebox.showerror("Error", str(e), parent=parent)


