import sqlite3

# Create a database connection
conn = sqlite3.connect('bank.db')

# Create a table to store account information
conn.execute('''CREATE TABLE IF NOT EXISTS accounts (
                  account_number INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  balance REAL NOT NULL
               )''')


def display_menu():
    """
    Displays the menu options for the user.
    """
    print("\nWelcome to My Bank System!")
    print("1. Create a New Account")
    print("2. Deposit Funds")
    print("3. Withdraw Funds")
    print("4. Check Balance")
    print("5. Exit")
    print("\nEnter your choice (1-5): ")


def create_account(name, balance):
    """
    Creates a new account and stores it in the database.
    """
    cursor = conn.cursor()  # Create a cursor object
    cursor.execute("INSERT INTO accounts (name, balance) VALUES (?, ?)", (name, balance))
    conn.commit()
    print("Account created successfully!")
    print(f"Your account number is: {cursor.lastrowid}")  # Get last inserted ID using cursor
    cursor.close()  # Close the cursor after use


def deposit(account_number, amount):
    """
    Deposits funds into an account and updates the balance.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM accounts WHERE account_number = ?", (account_number,))
    balance = cursor.fetchone()
    if not balance:
        print("Invalid account number!")
        return
    new_balance = balance[0] + amount
    conn.execute("UPDATE accounts SET balance = ? WHERE account_number = ?", (new_balance, account_number))
    conn.commit()
    print("Deposit successful! New balance:", new_balance)


def withdraw(account_number, amount):
    """
    Withdraws funds from an account, ensuring sufficient balance.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM accounts WHERE account_number = ?", (account_number,))
    balance = cursor.fetchone()
    if not balance:
        print("Invalid account number!")
        return
    if amount > balance[0]:
        print("Insufficient funds!")
        return
    new_balance = balance[0] - amount
    conn.execute("UPDATE accounts SET balance = ? WHERE account_number = ?", (new_balance, account_number))
    conn.commit()
    print("Withdrawal successful! New balance:", new_balance)


def check_balance(account_number):
    """
    Retrieves and displays the balance of a specified account.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM accounts WHERE account_number = ?", (account_number,))
    balance = cursor.fetchone()
    if not balance:
        print("Invalid account number!")
        return
    print("Your current balance is:", balance[0])


def main():
    """
    Main loop to handle user interaction and menu options.
    """
    while True:
        display_menu()
        choice = int(input())
        if choice == 1:
            name = input("Enter your name: ")
            balance = float(input("Enter initial balance: "))
            create_account(name, balance)
        elif choice == 2:
            while True:
                account_number = int(input("Enter account number: "))
                amount = float(input("Enter deposit amount: "))
                deposit(account_number, amount)
                print("\nBank Transaction:")
                print("3. Withdraw Funds")
                print("4. Check Balance")
                print("5. Exit Submenu")
                sub_choice = int(input("\nEnter your choice (3-5): "))
                if sub_choice == 3:
                    withdraw_account_number = int(input("Enter account number: "))
                    withdraw_amount = float(input("Enter withdrawal amount: "))
                    withdraw(withdraw_account_number, withdraw_amount)
                    break
                elif sub_choice == 4:
                    check_balance(account_number)
                    break
                elif sub_choice == 5:
                    break
                else:
                    print("Invalid choice. Please try again.")
        elif choice == 3:
            account_number = int(input("Enter account number: "))
            amount = float(input("Enter withdrawal amount: "))
            withdraw(account_number, amount)
            print("\nBank Transaction:")
            print("2. Deposit Funds")
            print("4. Check Balance")
            print("5. Exit Submenu")
            sub_choice = int(input("\nEnter your choice (2-4-5): "))
            if sub_choice == 2:
                    withdraw_account_number = int(input("Enter account number: "))
                    amount = float(input("Enter deposit amount: "))
                    deposit(account_number, amount)
            elif sub_choice == 4:
                    check_balance(account_number)
                    break
            elif sub_choice == 5:
                    break
            else:
                    print("Invalid choice. Please try again.")
            
        elif choice == 4:
            account_number = int(input("Enter account number: "))
            check_balance(account_number)
            print("\nBank Transaction:")
            print("2. Deposit Funds")
            print("3. Withdraw Funds")
            print("5. Exit Submenu")
            sub_choice = int(input("\nEnter your choice (2-3-5): "))
            if sub_choice == 2:
                    withdraw_account_number = int(input("Enter account number: "))
                    amount = float(input("Enter deposit amount: "))
                    deposit(account_number, amount)
            if sub_choice == 3:
                    withdraw_account_number = int(input("Enter account number: "))
                    withdraw_amount = float(input("Enter withdrawal amount: "))
                    withdraw(withdraw_account_number, withdraw_amount)
            elif sub_choice == 5:
                    break
            else:
                    print("Invalid choice. Please try again.")

        elif choice == 5:
            print("Exiting the system...")
            break
        else:
            print("Invalid choice. Please try again.")




if __name__ == "__main__":
    main()

# Close the database connection
conn.close()
