import sys
import json
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem


USER_DATA_FILE = "users.json"


# Insert the nlp_preprocess function here
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


# Download necessary NLTK data
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)


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




class FinanceAssistantApp(QWidget):
    def __init__(self):
        super().__init__()


        self.init_ui()


    def init_ui(self):
        self.setWindowTitle('Personal Finance Assistant')
        self.setGeometry(100, 100, 600, 400)


        # Add stylesheets for customization
        self.setStyleSheet("""
            QWidget {
                background-color: #000000; /* Set background color */
                font-family: Brada, sans; /* Set font family */
            }
            QLabel {
                color: #ffffff; /* Set text color */
                font-size: 30px; /* Set font size */
            }
            QPushButton {
                background-color: #4CAF50; /* Set button background color */
                color: white; /* Set button text color */
                border: none;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                cursor: pointer;
                border-radius: 5px; /* Add rounded corners to the button */
            }
        """)
       
        self.layout = QVBoxLayout()


        self.label = QLabel('Welcome to the Personal Finance Assistant', self)
        self.layout.addWidget(self.label)


        self.register_button = QPushButton('Register', self)
        self.login_button = QPushButton('Login', self)


        self.register_button.clicked.connect(self.show_register_screen)
        self.login_button.clicked.connect(self.show_login_screen)


        self.layout.addWidget(self.register_button)
        self.layout.addWidget(self.login_button)


        self.setLayout(self.layout)


    def show_register_screen(self):
        self.register_screen = RegisterScreen(self)
        self.register_screen.show()
        self.hide()


    def show_login_screen(self):
        self.login_screen = LoginScreen(self)
        self.login_screen.show()
        self.hide()




class RegisterScreen(QWidget):
    def __init__(self, parent):
        super().__init__()


        self.parent = parent
        self.init_ui()


    def init_ui(self):
        self.setWindowTitle('Register')
        self.setGeometry(200, 200, 600, 400)


        self.layout = QVBoxLayout()


        self.first_name_label = QLabel('First Name:', self)
        self.first_name_entry = QLineEdit(self)


        self.last_name_label = QLabel('Last Name:', self)
        self.last_name_entry = QLineEdit(self)


        self.phone_label = QLabel('Phone Number:', self)
        self.phone_entry = QLineEdit(self)


        self.email_label = QLabel('Email Address:', self)
        self.email_entry = QLineEdit(self)


        self.password_label = QLabel('Password:', self)
        self.password_entry = QLineEdit(self)
        self.password_entry.setEchoMode(QLineEdit.Password)


        self.register_button = QPushButton('Register', self)
        self.register_button.clicked.connect(self.register_user)


        self.back_button = QPushButton('Back', self)
        self.back_button.clicked.connect(self.show_main_screen)


        self.layout.addWidget(self.first_name_label)
        self.layout.addWidget(self.first_name_entry)
        self.layout.addWidget(self.last_name_label)
        self.layout.addWidget(self.last_name_entry)
        self.layout.addWidget(self.phone_label)
        self.layout.addWidget(self.phone_entry)
        self.layout.addWidget(self.email_label)
        self.layout.addWidget(self.email_entry)
        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password_entry)
        self.layout.addWidget(self.register_button)
        self.layout.addWidget(self.back_button)


        self.setLayout(self.layout)


    def register_user(self):
        new_user = {
            "first_name": self.first_name_entry.text(),
            "last_name": self.last_name_entry.text(),
            "phone": self.phone_entry.text(),
            "email": self.email_entry.text(),
            "password": self.password_entry.text(),
            "expenses": []
        }


        users = load_users()
        if self.email_entry.text() in users:
            print("A user with this email already exists.")
        else:
            users[self.email_entry.text()] = new_user
            save_users_data(users)
            print("User registered successfully")


    def show_main_screen(self):
        self.parent.show()
        self.close()




class LoginScreen(QWidget):
    def __init__(self, parent):
        super().__init__()


        self.parent = parent
        self.init_ui()


    def init_ui(self):
        self.setWindowTitle('Login')
        self.setGeometry(200, 200, 600, 400)


        self.layout = QVBoxLayout()


        self.email_label = QLabel('Email Address:', self)
        self.email_entry = QLineEdit(self)


        self.password_label = QLabel('Password:', self)
        self.password_entry = QLineEdit(self)
        self.password_entry.setEchoMode(QLineEdit.Password)


        self.login_button = QPushButton('Login', self)
        self.login_button.clicked.connect(self.login_user)


        self.back_button = QPushButton('Back', self)
        self.back_button.clicked.connect(self.show_main_screen)


        self.layout.addWidget(self.email_label)
        self.layout.addWidget(self.email_entry)
        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password_entry)
        self.layout.addWidget(self.login_button)
        self.layout.addWidget(self.back_button)


        self.setLayout(self.layout)


    def login_user(self):
        username = self.email_entry.text()
        password = self.password_entry.text()


        users = load_users()
        user = users.get(username)


        if user and user["password"] == password:
            print("User logged in successfully")
            self.show_user_actions_screen()
        else:
            print("Invalid username or password.")


    def show_user_actions_screen(self):
        self.user_actions_screen = UserActionsScreen(self)
        self.user_actions_screen.show()
        self.close()


    def show_main_screen(self):
        self.parent.show()
        self.close()




class UserActionsScreen(QWidget):
    def __init__(self, parent):
        super().__init__()


        self.parent = parent
        self.init_ui()


    def init_ui(self):
        self.setWindowTitle('User Actions')
        self.setGeometry(300, 300, 800, 600)


        self.layout = QVBoxLayout()


        self.add_expense_button = QPushButton('Add Expense', self)
        self.view_expenses_button = QPushButton('View Expenses', self)
        self.quit_button = QPushButton('Quit', self)


        self.add_expense_button.clicked.connect(self.show_add_expense_screen)
        self.view_expenses_button.clicked.connect(self.show_view_expenses_screen)
        self.quit_button.clicked.connect(self.show_main_screen)


        self.layout.addWidget(self.add_expense_button)
        self.layout.addWidget(self.view_expenses_button)
        self.layout.addWidget(self.quit_button)


        self.setLayout(self.layout)


    def show_add_expense_screen(self):
        self.add_expense_screen = AddExpenseScreen(self)
        self.add_expense_screen.show()
        self.close()


    def show_view_expenses_screen(self):
        self.view_expenses_screen = ViewExpensesScreen(self)
        self.view_expenses_screen.show()
        self.close()


    def show_main_screen(self):
        self.parent.show()
        self.close()




class AddExpenseScreen(QWidget):
    def __init__(self, parent):
        super().__init__()


        self.parent = parent
        self.init_ui()


    def init_ui(self):
        self.setWindowTitle('Add Expense')
        self.setGeometry(400, 400, 600, 400)


        self.layout = QVBoxLayout()


        self.date_label = QLabel('Date (YYYY-MM-DD):', self)
        self.date_entry = QLineEdit(self)


        self.description_label = QLabel('Transaction Description:', self)
        self.description_entry = QLineEdit(self)


        self.amount_label = QLabel('Amount:', self)
        self.amount_entry = QLineEdit(self)


        self.add_expense_button = QPushButton('Add Expense', self)
        self.add_expense_button.clicked.connect(self.add_expense)


        self.back_button = QPushButton('Back', self)
        self.back_button.clicked.connect(self.show_user_actions_screen)


        self.layout.addWidget(self.date_label)
        self.layout.addWidget(self.date_entry)
        self.layout.addWidget(self.description_label)
        self.layout.addWidget(self.description_entry)
        self.layout.addWidget(self.amount_label)
        self.layout.addWidget(self.amount_entry)
        self.layout.addWidget(self.add_expense_button)
        self.layout.addWidget(self.back_button)


        self.setLayout(self.layout)


    def add_expense(self):
        date = self.date_entry.text()
        description = self.description_entry.text()
        amount = float(self.amount_entry.text())


        expense = {"date": date, "description": description, "amount": amount, "category": categorize_transaction(description)}


        users = load_users()
        current_user = users[self.parent.email_entry.text()]
        current_user["expenses"].append(expense)
        save_users_data(users)
        print('Expense added successfully')


    def show_user_actions_screen(self):
        self.parent.show()
        self.close()




class ViewExpensesScreen(QWidget):
    def __init__(self, parent):
        super().__init__()


        self.parent = parent
        self.init_ui()


    def init_ui(self):
        self.setWindowTitle('View Expenses')
        self.setGeometry(500, 500, 800, 600)


        self.layout = QVBoxLayout()


        self.expenses_table = QTableWidget(self)
        self.expenses_table.setColumnCount(4)
        self.expenses_table.setHorizontalHeaderLabels(['Date', 'Description', 'Amount', 'Category'])


        self.layout.addWidget(self.expenses_table)


        self.back_button = QPushButton('Back', self)
        self.back_button.clicked.connect(self.show_user_actions_screen)


        self.layout.addWidget(self.back_button)


        self.setLayout(self.layout)


        self.load_expenses()


    def load_expenses(self):
        users = load_users()
        current_user = users[self.parent.parent.email_entry.text()]
        expenses = current_user["expenses"]


        self.expenses_table.setRowCount(len(expenses))


        for row, expense in enumerate(expenses):
            self.expenses_table.setItem(row, 0, QTableWidgetItem(expense["date"]))
            self.expenses_table.setItem(row, 1, QTableWidgetItem(expense["description"]))
            self.expenses_table.setItem(row, 2, QTableWidgetItem(str(expense["amount"])))
            self.expenses_table.setItem(row, 3, QTableWidgetItem(expense["category"]))


    def show_user_actions_screen(self):
        self.parent.show()
        self.close()




def load_users():
    try:
        with open(USER_DATA_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}




def save_users_data(users):
    with open(USER_DATA_FILE, 'w') as file:
        json.dump(users, file, indent=4)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_app = FinanceAssistantApp()
    main_app.show()
    sys.exit(app.exec_())
