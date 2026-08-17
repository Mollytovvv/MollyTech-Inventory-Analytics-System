from cli.db import get_connection

def add_item():
    name = input("Item name: ")
    category = input("Category (GPU/CPU/RAM/SSD): ")
    buy_price = float(input("Buy price: "))
    sell_price = float(input("Sell price: "))

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO items (name, category, buy_price, sell_price)
        VALUES (%s, %s, %s, %s)
    """, (name, category, buy_price, sell_price))

    conn.commit()
    conn.close()

    print("Item added successfully!")