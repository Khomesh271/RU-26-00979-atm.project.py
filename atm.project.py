# # ATM Management System
# # A beginner-friendly Python project using functions, loops, conditions and files.

# PIN = "1234"
# BALANCE_FILE = "atm.txt"
# TRANSACTION_FILE = "transactions.txt"
# DEFAULT_BALANCE = 10000


# def load_balance():
#     """Read the saved balance. If the file is missing, start with 10000."""
#     try:
#         with open(BALANCE_FILE, "r") as file:
#             return float(file.read())
#     except (FileNotFoundError, ValueError):
#         save_balance(DEFAULT_BALANCE)
#         return DEFAULT_BALANCE


# def save_balance(balance):
#     """Save the current balance in a file."""
#     with open(BALANCE_FILE, "w") as file:
#         file.write(str(balance))


# def save_transaction(message):
#     """Add a transaction message to the transaction history file."""
#     with open(TRANSACTION_FILE, "a") as file:
#         file.write(message + "\n")


# def show_mini_statement():
#     """Display the saved transaction history."""
#     print("\n--- Mini Statement ---")
#     try:
#         with open(TRANSACTION_FILE, "r") as file:
#             history = file.read()
#             if history.strip():
#                 print(history, end="")
#             else:
#                 print("No transactions yet.")
#     except FileNotFoundError:
#         print("No transactions yet.")


# def deposit(balance):
#     """Add money to the account."""
#     try:
#         amount = float(input("Enter deposit amount: "))
#         if amount <= 0:
#             print("Amount must be greater than zero.")
#         else:
#             balance += amount
#             save_balance(balance)
#             message = "Deposit: " + format_amount(amount) + " | Balance: " + format_amount(balance)
#             save_transaction(message)
#             print("Deposit successful. New Balance:", format_amount(balance))
#     except ValueError:
#         print("Invalid amount. Please enter numbers only.")
#     return balance


# def withdraw(balance):
#     """Withdraw money if the amount is valid and affordable."""
#     try:
#         amount = float(input("Enter withdrawal amount: "))
#         if amount <= 0:
#             print("Amount must be greater than zero.")
#         elif amount > balance:
#             print("Insufficient balance.")
#         else:
#             balance -= amount
#             save_balance(balance)
#             message = "Withdraw: " + format_amount(amount) + " | Balance: " + format_amount(balance)
#             save_transaction(message)
#             print("Withdrawal successful. New Balance:", format_amount(balance))
#     except ValueError:
#         print("Invalid amount. Please enter numbers only.")
#     return balance


# def main():
#     # Check the PIN. The user gets a maximum of 3 attempts.
#     attempts = 0
#     while attempts < 3:
#         entered_pin = input("Enter PIN: ")
#         if entered_pin == PIN:
#             print("Login successful.")
#             break
#         attempts += 1
#         if attempts < 3:
#             print("Invalid PIN. Attempts left:", 3 - attempts)
#         else:
#             print("Account locked. Exiting...")
#             return

#     balance = load_balance()

#     # Keep showing the menu until the user chooses to exit.
#     while True:
#         print("\n--- ATM Menu ---")
#         print("1. Check Balance")
#         print("2. Deposit")
#         print("3. Withdraw")
#         print("4. Mini Statement")
#         print("5. Exit")

#         choice = input("Enter your choice: ")

#         if choice == "1":
#             print("Current Balance:", format_amount(balance))
#         elif choice == "2":
#             balance = deposit(balance)
#         elif choice == "3":
#             balance = withdraw(balance)
#         elif choice == "4":
#             show_mini_statement()
#         elif choice == "5":
#             print("Thank you for using the ATM.")
#             break
#         else:
#             print("Invalid choice. Please select 1 to 5.")


# if __name__ == "__main__":
#     main()
import json
import os
from datetime import datetime

FILE_NAME = "atm.json"  # Use .json extension for proper data format representation
TEMP_FILE_NAME = "atm.tmp.json"
DEFAULT_PIN = "1234"
DEFAULT_BALANCE = 10000


def load_data():
    if not os.path.exists(FILE_NAME):
        data = {
            "balance": DEFAULT_BALANCE,
            "transactions": []
        }
        save_data(data)
        return data

    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Strict type checking for JSON schema safety
        balance = data.get("balance")
        if not isinstance(balance, (int, float)) or isinstance(balance, bool) or balance < 0:
            raise ValueError("Invalid balance data found in storage.")

        transactions = data.get("transactions")
        if not isinstance(transactions, list):
            raise ValueError("Invalid transaction data found in storage.")

        return data

    except (json.JSONDecodeError, OSError, ValueError, TypeError) as error:
        print(f"Critical Error reading ATM data: {error}")
        print("Please check or remove the corrupted storage file before running again.")
        raise SystemExit(1)


def save_data(data):
    """Saves data atomically to prevent corruption during unexpected crashes."""
    try:
        with open(TEMP_FILE_NAME, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
        os.replace(TEMP_FILE_NAME, FILE_NAME)
    except OSError as error:
        print(f"Critical Error saving data: {error}")
        raise SystemExit(1)


def check_balance(data):
    print(f"\nYour current balance is: ₹{data['balance']:,}")


def deposit(data):
    try:
        raw_input = input("Enter deposit amount: ").strip()
        amount = float(raw_input)

        if amount <= 0:
            print("Amount must be greater than zero.")
            return

        if not amount.is_integer():
            print("Please enter a whole number amount.")
            return

        amount = int(amount)
        data["balance"] += amount

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data["transactions"].append(
            f"[{timestamp}] Deposit: +₹{amount} | Balance: ₹{data['balance']}"
        )

        save_data(data)
        print(f"Deposit successful. New Balance: ₹{data['balance']:,}")

    except ValueError:
        print("Invalid amount. Please enter numbers only.")


def withdraw(data):
    try:
        raw_input = input("Enter withdrawal amount: ").strip()
        amount = float(raw_input)

        if amount <= 0:
            print("Amount must be greater than zero.")
            return

        if not amount.is_integer():
            print("Please enter a whole number amount.")
            return

        amount = int(amount)

        if amount > data["balance"]:
            print("Insufficient balance.")
            return

        data["balance"] -= amount

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data["transactions"].append(
            f"[{timestamp}] Withdraw: -₹{amount} | Balance: ₹{data['balance']}"
        )

        save_data(data)
        print(f"Withdrawal successful. New Balance: ₹{data['balance']:,}")

    except ValueError:
        print("Invalid amount. Please enter numbers only.")


def mini_statement(data):
    print("\n--- MINI STATEMENT ---")

    if not data["transactions"]:
        print("No transactions yet.")
    else:
        # Show last 5 transactions
        for transaction in data["transactions"][-5:]:
            print(transaction)

    print(f"Current Balance: ₹{data['balance']:,}")


def login():
    attempts = 3

    while attempts > 0:
        pin = input("Enter your ATM PIN: ").strip()

        if pin == DEFAULT_PIN:
            print("Login successful!")
            return True

        attempts -= 1

        if attempts > 0:
            print(f"Invalid PIN. Attempts left: {attempts}")

    print("Account locked due to multiple incorrect attempts. Exiting...")
    return False


def main():
    data = load_data()

    if not login():
        return

    while True:
        print("\n===== ATM MANAGEMENT SYSTEM =====")
        print("1. Check Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Mini Statement")
        print("5. Exit")

        try:
            choice = int(input("Enter your choice: ").strip())
        except ValueError:
            print("Invalid choice. Please enter a number between 1 and 5.")
            continue

        if choice == 1:
            check_balance(data)
        elif choice == 2:
            deposit(data)
        elif choice == 3:
            withdraw(data)
        elif choice == 4:
            mini_statement(data)
        elif choice == 5:
            print("Thank you for using our ATM!")
            break
        else:
            print("Invalid option. Please choose between 1 to 5.")


if __name__ == "__main__":
    main()
