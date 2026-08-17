from cli.db import get_connection

def sell_item():
    item_id = int(input("Enter Item ID to sell: "))
    sell_price = float(input("Enter selling price: "))

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT buy_price, status FROM items WHERE id = %s", (item_id,))
    item = cur.fetchone()

    if not item:
        print("Item not found.")
        return

    buy_price, status = item

    if status == "sold":
        print("This item is already sold.")
        return

    profit = sell_price - float(buy_price)

    cur.execute("""
        INSERT INTO sales (item_id, sold_price, profit)
        VALUES (%s, %s, %s)
    """, (item_id, sell_price, profit))

    cur.execute("""
        UPDATE items
        SET status = 'sold'
        WHERE id = %s
    """, (item_id,))

    conn.commit()
    conn.close()

    print(f"Item sold successfully! Profit: {profit}")