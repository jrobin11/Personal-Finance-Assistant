# Personal Finance Assistant

## Project Overview
The Personal Finance Assistant is a Python application designed to help users manage their personal finances more effectively. It allows users to track their expenses by categorizing them into various categories like Food, Fuel, Bills, and Travel. The application also features user account management, enabling personalized expense tracking.

## Features
- User Registration and Login
- Expense Tracking and Categorization
- Admin functionalities to manage user accounts
- Data Persistence across sessions

## NLP in the Project
Natural Language Processing (NLP) plays a crucial role in the Personal Finance Assistant. It is used to enhance the expense categorization process. Here's how NLP is integrated:
- **Text Preprocessing:** The application uses NLP techniques like tokenization and stopword removal to preprocess the descriptions of expenses. This involves breaking down the text into individual words and removing common words that don't contribute significant meaning.
   - Text Preprocessing:
      - Purpose: The goal here is to prepare the raw text from your expense descriptions for further analysis. Text preprocessing is a common first step in many NLP applications.
      - Tokenization: This process involves splitting the text into individual words or tokens. For example, the phrase "Grocery shopping at Walmart" would be split into ['Grocery', 'shopping', 'at', 'Walmart'].
   - Stopword Removal:
      - Stopwords are common words that usually don’t carry significant meaning and are often removed from the text. Examples include words like "at", "the", "and", etc.
      - Removing these words helps to focus on the more meaningful words in your text. So, from our earlier example, after removing stopwords, you might be left with ['Grocery', 'shopping', 'Walmart'].

- **Expense Categorization:** After preprocessing, the application uses keyword-based logic to categorize each expense. For example, if a transaction description contains words like "restaurant" or "grocery," the NLP system categorizes it as "Food." This approach simplifies the user's task of categorizing each transaction manually.
   - Expense Categorization:
      - Purpose: After preprocessing, your application categorizes each expense based on the keywords found in the processed text.
      - Keyword-Based Logic: Here, you have predefined categories (like Food, Fuel, Bills, Travel) and associated keywords for each category. When the preprocessed text of an expense description matches certain keywords, the expense is categorized accordingly.
      - Example: If a user inputs an expense description like "Dinner at an Italian restaurant", after preprocessing, the remaining significant words might be ['Dinner', 'Italian', 'restaurant']. If your categorization logic associates the keyword "restaurant" with the "Food" category, this expense will be categorized as "Food".
      - Benefit: This automated categorization simplifies the process for users, as they don’t have to manually categorize each transaction. It makes tracking expenses more efficient and user-friendly.

## Getting Started

### Prerequisites
- Python 3.x
- Git (for cloning the repository)

### Installation

1. **Clone the Repository**

   First, clone the repository to your local machine using Git:

   ```bash
   git clone git@github.com:jrobin11/Personal-Finance-Assistant.git
   cd Personal-Finance-Assistant

# Install Required Packages
- Before running the application, you need to install the required Python packages:
  ```bash
  pip install -r requirements.txt

# Running the Application
- To run the Personal Finance Assistant, use the following command in your terminal (ensure you are in the project directory):
  ```bash
  python main.py

# Usage
- Upon running the application, you will be prompted to either log in or register as a new user. As an admin, you can use the default credentials (username: admin, password: admin) to access admin functionalities.
  - New Users: Select 'New' and provide the requested details to create a new account.
  - Existing Users: Select 'Existing' and log in with your username and password.
  - Admin: Select 'Existing' and log in with admin credentials to manage user accounts.
Once logged in, follow the on-screen prompts to add, view, or manage your expenses.
