from cli.db import get_connection

def total_profit():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT SUM(profit) FROM sales")
    result = cur.fetchone()[0]

    conn.close()

    print(f"Total Profit: {result if result else 0}")


def total_sales():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM sales")
    result = cur.fetchone()[0]

    conn.close()

    print(f"Total Items Sold: {result if result else 0}")


def inventory_value():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT SUM(buy_price) FROM items WHERE status = 'available'")
    result = cur.fetchone()[0]

    conn.close()

    print(f"Inventory Value: {result if result else 0}")