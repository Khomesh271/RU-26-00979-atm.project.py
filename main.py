import json
import os

FILE_NAME = "atm.txt"
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
        with open(FILE_NAME, "r") as file:
            data = json.load(file)

        if not isinstance(data.get("balance"), (int, float)) or isinstance(data.get("balance"), bool) or data["balance"] < 0:
            raise ValueError("Invalid balance data")

        if not isinstance(data.get("transactions"), list):
            raise ValueError("Invalid transaction data")

        return data

    except (json.JSONDecodeError, OSError, ValueError, TypeError) as error:
        print("Error reading ATM file:", error)
        print("Please check atm.txt before running again.")
        raise SystemExit(1)


def save_data(data):
    with open(FILE_NAME, "w") as file:
        json.dump(data, file, indent=4)


def check_balance(data):
    print("Your current balance is:", data["balance"])


def deposit(data):
    try:
        amount = float(input("Enter deposit amount: "))

        if amount <= 0:
            print("Amount must be greater than zero.")
            return

        if not amount.is_integer():
            print("Please enter a whole number amount.")
            return

        amount = int(amount)
        data["balance"] += amount

        data["transactions"].append(
            f"Deposit {amount} | Balance: {data['balance']}"
        )

        save_data(data)
        print("Deposit successful. New Balance:", data["balance"])

    except ValueError:
        print("Invalid amount. Please enter numbers only.")


def withdraw(data):
    try:
        amount = float(input("Enter withdrawal amount: "))

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

        data["transactions"].append(
            f"Withdraw {amount} | Balance: {data['balance']}"
        )

        save_data(data)
        print("Withdrawal successful. New Balance:", data["balance"])

    except ValueError:
        print("Invalid amount. Please enter numbers only.")


def mini_statement(data):
    print("\n--- MINI STATEMENT ---")

    if not data["transactions"]:
        print("No transactions yet.")
    else:
        for transaction in data["transactions"][-5:]:
            print(transaction)

    print("Current Balance:", data["balance"])


def login():
    attempts = 3

    while attempts > 0:
        pin = input("Enter your ATM PIN: ")

        if pin == DEFAULT_PIN:
            print("Login successful!")
            return True

        attempts -= 1

        if attempts > 0:
            print("Invalid PIN. Attempts left:", attempts)

    print("Account locked. Exiting...")
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
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid choice. Please enter a number.")
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
            print("Invalid option. Please choose 1 to 5.")


if __name__ == "_main_":
    main()