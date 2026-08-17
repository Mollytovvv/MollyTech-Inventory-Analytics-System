from cli.inventory import add_item
from cli.sales import sell_item
from cli.reports import total_profit, total_sales, inventory_value


def menu():
    while True:
        print("\n===== MOLLYTECH SYSTEM =====")
        print("1. Add Item")
        print("2. Sell Item")
        print("3. Reports")
        print("0. Exit")

        choice = input("Choose: ")

        if choice == "1":
            add_item()

        elif choice == "2":
            sell_item()

        elif choice == "3":
            print("\n--- REPORTS ---")
            total_profit()
            total_sales()
            inventory_value()

        elif choice == "0":
            break

        else:
            print("Invalid choice")

if __name__ == "__main__":
    menu()