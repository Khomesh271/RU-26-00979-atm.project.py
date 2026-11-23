# ATM Management System

A simple, beginner-friendly ATM simulation written in Python 3. It uses basic Python concepts such as variables, conditions, loops, functions, exception handling, and file handling.

## Features

- PIN login (default PIN: `1234`)
- Maximum of 3 PIN attempts
- Check account balance
- Deposit money
- Withdraw money (including withdrawing the full balance)
- Mini statement / transaction history
- Saves balance and transactions in local text files
- Handles invalid menu choices and non-numeric amounts

## Requirements

- Python 3 (no extra libraries required)

## Run the project

1. Download or clone this repository.
2. Open a terminal in the project folder.
3. Run:

   ```bash
   python main.py
   ```

   On some Windows systems, use:

   ```bash
   py main.py
   ```

4. Enter the default PIN: `1234`.

## Files created when the program runs

- `atm.txt` — stores the current account balance.
- `transactions.txt` — stores transaction history.

If `atm.txt` does not exist, the program starts with a balance of `10000` and creates the file.

> To reset the balance to the default for a fresh test, close the program and delete `atm.txt`. To reset the transaction history too, delete `transactions.txt`. The files will be recreated as needed.

## Sample test scenarios

### 1. Normal input — deposit

- PIN: `1234`
- Menu choice: `2`
- Amount: `5000`

Expected: deposit is successful and the balance becomes `15000` (when starting from `10000`).

### 2. Boundary input — withdraw the entire balance

- PIN: `1234`
- Menu choice: `3`
- Amount: `10000`

Expected: withdrawal is successful and the balance becomes `0` (when starting from `10000`).

### 3. Invalid PIN

Enter these PINs in order: `1111`, `2222`, `3333`.

Expected: the program shows the remaining attempts and then locks/exits.

### 4. Invalid amount and another valid transaction

Start with a balance of `10000`.

- PIN: `1234`
- Menu choice: `3`
- Amount: `abc`

Expected: `Invalid amount. Please enter numbers only.` The program does not exit.
- Menu choice: `3`
- Amount: `2000`

Expected: withdrawal succeeds and balance becomes `8000`.
- Menu choice: `4`

Expected: the mini statement shows the withdrawal transaction.

## Concepts used (for viva / explanation)

| Concept | Where it is used |
|---|---|
| Variables | PIN, balance, amount, menu choice |
| `if / elif / else` | PIN checking, menu selection, amount validation |
| `while` loops | PIN attempts and repeating the ATM menu |
| Functions | Separate tasks into `deposit`, `withdraw`, `load_balance`, etc. |
| `try / except` | Handle invalid numeric input and missing/corrupted files |
| File handling | Read and save balance and transaction history |
| `return` | Send the updated balance back from deposit/withdraw functions |

## Limitations

This is an educational simulation, not a real banking system. It uses a fixed PIN and plain-text files, so it should not be used for real financial data.
