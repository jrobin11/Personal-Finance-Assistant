import json
import os
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

from constants import FOOD_KEYWORDS, FUEL_KEYWORDS, BILLS_KEYWORDS, TRAVEL_KEYWORDS, \
    ENTERTAINMENT_KEYWORDS, SHOPPING_KEYWORDS, HEALTH_KEYWORDS, EDUCATION_KEYWORDS, \
    HOME_KEYWORDS, TRANSPORTATION_KEYWORDS, CHILD_CARE_KEYWORDS, PET_CARE_KEYWORDS, PERSONAL_CARE_KEYWORDS,\
    SAVINGS_INVESTMENT_KEYWORDS

USER_DATA_FILE = "users.json"

def load_users():
    """ Load users from the JSON file. """
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as file:
            return json.load(file)
    else:
        return {}

def save_users_data(users):
    """ Save the users data to the JSON file. """
    with open(USER_DATA_FILE, 'w') as file:
        json.dump(users, file, indent=4)

def nlp_preprocess(text):
    """ Preprocess text for categorization. """
    compounds = re.findall(r'\b(?:water|electricity|internet|phone)-bill\b', text, re.IGNORECASE)
    tokens = word_tokenize(text)
    tokens = [word.lower() for word in tokens if word.lower() not in stopwords.words('english')]
    tokens.extend(compounds)
    return " ".join(tokens)

def categorize_transaction(description):
    """ Categorize a transaction based on its description. """
    processed_text = nlp_preprocess(description)
    bill_compounds = {"water-bill", "electricity-bill", "internet-bill", "phone-bill"}
    
    for compound in bill_compounds:
        if compound in processed_text:
            return "Bills"
    if any(keyword in processed_text for keyword in FOOD_KEYWORDS):
        return "Food"
    elif any(keyword in processed_text for keyword in FUEL_KEYWORDS):
        return "Fuel"
    elif any(keyword in processed_text for keyword in BILLS_KEYWORDS):
        return "Bills"
    elif any(keyword in processed_text for keyword in TRAVEL_KEYWORDS):
        return "Travel"
    elif any(keyword in processed_text for keyword in ENTERTAINMENT_KEYWORDS):
        return "Entertainment"
    elif any(keyword in processed_text for keyword in SHOPPING_KEYWORDS):
        return "Shopping"
    elif any(keyword in processed_text for keyword in HEALTH_KEYWORDS):
        return "Health"
    elif any(keyword in processed_text for keyword in EDUCATION_KEYWORDS):
        return "Education"
    elif any(keyword in processed_text for keyword in HOME_KEYWORDS):
        return "Home"
    elif any(keyword in processed_text for keyword in TRANSPORTATION_KEYWORDS):
        return "Transportation"
    elif any(keyword in processed_text for keyword in CHILD_CARE_KEYWORDS):
        return "Child Care"
    elif any(keyword in processed_text for keyword in PET_CARE_KEYWORDS):
        return "Pet Care"
    elif any(keyword in processed_text for keyword in PERSONAL_CARE_KEYWORDS):
        return "Personal Care"
    elif any(keyword in processed_text for keyword in SAVINGS_INVESTMENT_KEYWORDS):
        return "Savings/Investments"
    
    else:
        return "Other"

def add_expense(username, users, date, description, amount):
    """ Add an expense for a user. """
    category = categorize_transaction(description)
    expense = {"date": date, "description": description, "amount": amount, "category": category}
    users[username]["expenses"].append(expense)
    save_users_data(users)
    return True  # Indicates success

def view_expenses_by_date(username, users):
    """ Return a user's expenses, sorted by date. """
    if not users[username]["expenses"]:
        return []

    expenses_by_date = {}
    for expense in users[username]["expenses"]:
        expenses_by_date.setdefault(expense['date'], []).append(expense)

    sorted_expenses = {}
    for date in sorted(expenses_by_date):
        sorted_expenses[date] = expenses_by_date[date]
    return sorted_expenses

def modify_user_info(username, users, info_to_modify, new_value):
    """ Modify a user's information. """
    if info_to_modify in users[username] and info_to_modify != "expenses":
        if info_to_modify == "email" and new_value in users:
            return False  # Email already exists
        users[username][info_to_modify] = new_value
        save_users_data(users)
        return True
    return False

# Other utility functions can be added as needed
