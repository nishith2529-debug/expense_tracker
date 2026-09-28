import csv
from datetime import datetime
from pathlib import Path

DATA_FILE = Path(__file__).with_name("expenses.csv")


def load_expenses():
    expenses = []
    if not DATA_FILE.exists():
        return expenses

    with DATA_FILE.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            expenses.append({
                "date": row.get("date", ""),
                "category": row.get("category", "Other"),
                "description": row.get("description", ""),
                "amount": float(row.get("amount", 0)),
            })
    return expenses


def save_expenses(expenses):
    with DATA_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["date", "category", "description", "amount"])
        writer.writeheader()
        writer.writerows(expenses)


def add_expense():
    print("\nAdd Expense")
    date = input("Date (YYYY-MM-DD or press Enter for today): ").strip() or datetime.now().strftime("%Y-%m-%d")
    category = input("Category: ").strip() or "Other"
    description = input("Description: ").strip() or "No description"

    while True:
        try:
            amount = float(input("Amount: ").strip())
            if amount <= 0:
                raise ValueError
            break
        except ValueError:
            print("Please enter a valid positive amount.")

    expense = {
        "date": date,
        "category": category,
        "description": description,
        "amount": round(amount, 2),
    }

    expenses = load_expenses()
    expenses.append(expense)
    save_expenses(expenses)
    print("Expense added successfully.")


def list_expenses():
    expenses = load_expenses()
    if not expenses:
        print("No expenses found.")
        return

    print("\nExpense List")
    print("-" * 70)
    print(f"{'Date':<12} {'Category':<12} {'Description':<20} {'Amount':>10}")
    print("-" * 70)

    total = 0.0
    for item in expenses:
        print(f"{item['date']:<12} {item['category']:<12} {item['description']:<20} ${item['amount']:>9.2f}")
        total += item["amount"]

    print("-" * 70)
    print(f"{'Total':>45} ${total:>9.2f}")


def monthly_summary():
    expenses = load_expenses()
    if not expenses:
        print("No expenses found.")
        return

    month = input("Enter month (YYYY-MM): ").strip()
    total = 0.0
    print(f"\nSummary for {month}")
    print("-" * 50)

    for item in expenses:
        if item["date"].startswith(month):
            print(f"{item['date']} | {item['category']:<12} | {item['description']:<20} | ${item['amount']:.2f}")
            total += item["amount"]

    print("-" * 50)
    print(f"Total spent in {month}: ${total:.2f}")


def category_summary():
    expenses = load_expenses()
    if not expenses:
        print("No expenses found.")
        return

    totals = {}
    for item in expenses:
        totals[item["category"]] = totals.get(item["category"], 0.0) + item["amount"]

    print("\nCategory Summary")
    print("-" * 40)
    for category, amount in sorted(totals.items()):
        print(f"{category:<12} ${amount:.2f}")
    print("-" * 40)


def delete_expense():
    expenses = load_expenses()
    if not expenses:
        print("No expenses found.")
        return

    print("\nDelete Expense")
    for index, item in enumerate(expenses, start=1):
        print(f"{index}. {item['date']} | {item['category']} | {item['description']} | ${item['amount']:.2f}")

    try:
        choice = int(input("Enter the number to delete: ").strip())
        if 1 <= choice <= len(expenses):
            removed = expenses.pop(choice - 1)
            save_expenses(expenses)
            print(f"Deleted: {removed['description']} (${removed['amount']:.2f})")
        else:
            print("Invalid selection.")
    except ValueError:
        print("Please enter a valid number.")


def show_menu():
    print("\nExpense Tracker")
    print("1. Add Expense")
    print("2. View All Expenses")
    print("3. Monthly Summary")
    print("4. Category Summary")
    print("5. Delete Expense")
    print("6. Exit")


def main():
    while True:
        show_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            list_expenses()
        elif choice == "3":
            monthly_summary()
        elif choice == "4":
            category_summary()
        elif choice == "5":
            delete_expense()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please choose from 1 to 6.")


if __name__ == "__main__":
    main()
