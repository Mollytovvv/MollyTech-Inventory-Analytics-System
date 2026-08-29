import os
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
from cli.db import get_connection

import secrets
from datetime import datetime, timedelta
import smtplib
from email.message import EmailMessage
from functools import wraps
from email.mime.image import MIMEImage

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
    raise Exception("Email credentials not set in .env file")

# =========================
# EMAIL UTILITY FUNCTION
# =========================
# =========================
# EMAIL UTILITY FUNCTION
# =========================
def send_reset_email(to_email, token, username):

    msg = EmailMessage()
    msg["Subject"] = "MollyTech Inventory Analytics - Password Reset"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email

    reset_link = url_for(
        "reset_password",
        token=token,
        _external=True
    )

    # =========================
    # PLAIN-TEXT FALLBACK
    # =========================
    msg.set_content(f"""
Hello {username},

We received a request to reset the password for your MollyTech Inventory Analytics account.

To reset your password, visit the following link:

{reset_link}

This password reset link will expire in 15 minutes.

If you did not request a password reset, you can safely ignore this email.

MollyTech Inventory Analytics
Automated System Notification
""")

    # =========================
    # HTML EMAIL
    # =========================
    html_content = f"""
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Password Reset</title>
</head>

<body style="
    margin:0;
    padding:0;
    background-color:#f4f6f8;
    font-family:Arial, Helvetica, sans-serif;
">

<table width="100%" cellpadding="0" cellspacing="0" border="0"
       style="background-color:#f4f6f8;padding:40px 20px;">

<tr>
<td align="center">

<table width="600" cellpadding="0" cellspacing="0" border="0"
       style="
           max-width:600px;
           width:100%;
           background-color:#ffffff;
           border-radius:10px;
           overflow:hidden;
       ">

<!-- HEADER -->
<tr>
<td style="
    background-color:#111827;
    padding:30px;
    text-align:center;
">

    <img src="cid:mollytech_logo"
         alt="MollyTech"
         width="100"
         style="
             display:block;
             margin:0 auto 15px auto;
             border:0;
             outline:none;
             text-decoration:none;
         ">

    <div style="
        color:#ffffff;
        font-size:24px;
        font-weight:bold;
        letter-spacing:1px;
    ">
        MOLLYTECH
    </div>

    <div style="
        color:#9ca3af;
        font-size:13px;
        margin-top:6px;
    ">
        Inventory Analytics
    </div>

</td>
</tr>

<!-- CONTENT -->
<tr>
<td style="padding:40px;">

    <h1 style="
        margin:0 0 20px 0;
        color:#111827;
        font-size:24px;
    ">
        Password Reset Request
    </h1>

    <p style="
        margin:0 0 16px 0;
        color:#374151;
        font-size:15px;
        line-height:1.6;
    ">
        Hello <strong>{username}</strong>,
    </p>

    <p style="
        margin:0 0 24px 0;
        color:#374151;
        font-size:15px;
        line-height:1.6;
    ">
        We received a request to reset the password associated
        with your MollyTech Inventory Analytics account.
    </p>

    <p style="
        margin:0 0 28px 0;
        color:#374151;
        font-size:15px;
        line-height:1.6;
    ">
        Click the button below to create a new password:
    </p>

    <!-- BUTTON -->
    <table cellpadding="0" cellspacing="0" border="0" align="center">

        <tr>

            <td align="center"
                style="
                    background-color:#111827;
                    border-radius:6px;
                ">

                <a href="{reset_link}"
                   style="
                       display:inline-block;
                       padding:14px 28px;
                       color:#ffffff;
                       text-decoration:none;
                       font-size:14px;
                       font-weight:bold;
                   ">
                    RESET PASSWORD
                </a>

            </td>

        </tr>

    </table>

    <!-- SECURITY NOTICE -->
    <div style="
        margin-top:30px;
        padding:15px;
        background-color:#f9fafb;
        border-left:4px solid #111827;
    ">

        <p style="
            margin:0;
            color:#374151;
            font-size:13px;
            line-height:1.5;
        ">

            <strong>Security Notice:</strong><br>

            This password reset link will expire in
            <strong>15 minutes</strong>.

        </p>

    </div>

    <p style="
        margin:25px 0 0 0;
        color:#6b7280;
        font-size:13px;
        line-height:1.6;
    ">
        If you did not request a password reset,
        you can safely ignore this email.
        Your account will remain unchanged.
    </p>

    <!-- FALLBACK LINK -->
    <p style="
        margin:25px 0 0 0;
        color:#6b7280;
        font-size:12px;
        line-height:1.5;
    ">
        If the button above does not work,
        copy and paste the following link into your browser:
    </p>

    <p style="
        word-break:break-all;
        color:#4b5563;
        font-size:12px;
    ">
        {reset_link}
    </p>

</td>
</tr>

<!-- FOOTER -->
<tr>

<td style="
    background-color:#f9fafb;
    padding:22px 30px;
    text-align:center;
    border-top:1px solid #e5e7eb;
">

    <p style="
        margin:0;
        color:#6b7280;
        font-size:12px;
    ">
        MollyTech Inventory Analytics
    </p>

    <p style="
        margin:6px 0 0 0;
        color:#9ca3af;
        font-size:11px;
    ">
        Automated System Notification
    </p>

</td>

</tr>

</table>

</td>
</tr>

</table>

</body>
</html>
"""

    msg.add_alternative(html_content, subtype="html")

    # =========================
    # EMBED LOGO
    # =========================

    logo_path = os.path.join(
        BASE_DIR,
        "static",
        "images",
        "mollytech_logo.jpg"
    )

    with open(logo_path, "rb") as img:
        logo_data = img.read()

    msg.get_payload()[1].add_related(
        logo_data,
        maintype="image",
        subtype="jpeg",
        cid="<mollytech_logo>"
    )

    # =========================
    # SEND EMAIL
    # =========================

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, template_folder=os.path.join(BASE_DIR, "templates"))

if not os.getenv("SECRET_KEY"):
    raise Exception("SECRET_KEY not set in .env")

app.secret_key = os.getenv("SECRET_KEY")

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper

# =========================
# LOGIN PAGE
# =========================
@app.route("/login", methods=["GET", "POST"])
def login():

    if "user" in session:
        return redirect(url_for("home"))

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT password_hash
            FROM admin_users
            WHERE username = %s
        """, (username,))

        result = cur.fetchone()

        cur.close()
        conn.close()

        if result and check_password_hash(result[0], password):
            session["user"] = username
            return redirect(url_for("home"))

        flash("Invalid username or password", "error")
        return redirect(url_for("login"))
    return render_template("login.html")

# =========================
# DASHBOARD (HOME PAGE)
# =========================
@app.route("/")
@login_required
def home():

    conn = get_connection()
    cur = conn.cursor()

    # ITEMS DATA
    cur.execute("""
        SELECT id, name, brand, category, buy_price, sell_price, status
        FROM items
        ORDER BY id ASC
    """)
    items = cur.fetchall()

    # SALES DATA (for charts)
    cur.execute("""
        SELECT 
            TO_CHAR(date_sold, 'YYYY-MM-DD HH24:MI:SS'),
            sold_price,
            profit
        FROM sales
        ORDER BY date_sold ASC
    """)
    chart_data = cur.fetchall()

    dates = []
    revenue = []
    profits = []

    running_revenue = 0
    running_profit = 0

    for row in chart_data:
        sold_price = float(row[1] or 0)
        profit_value = float(row[2] or 0)

        running_revenue += sold_price
        running_profit += profit_value

        dates.append(str(row[0]))
        revenue.append(running_revenue)
        profits.append(running_profit)

    # TODAY
    cur.execute("""
        SELECT COALESCE(SUM(sold_price), 0), COALESCE(SUM(profit), 0)
        FROM sales
        WHERE DATE(date_sold) = CURRENT_DATE
    """)
    today_revenue, today_profit = cur.fetchone()

    # YESTERDAY
    cur.execute("""
        SELECT COALESCE(SUM(sold_price), 0), COALESCE(SUM(profit), 0)
        FROM sales
        WHERE DATE(date_sold) = CURRENT_DATE - INTERVAL '1 day'
    """)
    yesterday_revenue, yesterday_profit = cur.fetchone()

    # MONTH
    cur.execute("""
        SELECT COALESCE(SUM(sold_price), 0), COALESCE(SUM(profit), 0)
        FROM sales
        WHERE date_trunc('month', date_sold) = date_trunc('month', CURRENT_DATE)
    """)
    monthly_revenue, monthly_profit = cur.fetchone()

    # PREVIOUS MONTH
    cur.execute("""
        SELECT COALESCE(SUM(sold_price), 0)
        FROM sales
        WHERE date_trunc('month', date_sold) = date_trunc('month', CURRENT_DATE - INTERVAL '1 month')
    """)
    previous_month_revenue = cur.fetchone()[0]

    # GROWTH
    def percent_change(today, yesterday):
        if yesterday == 0:
            return 100 if today > 0 else 0
        return ((today - yesterday) / yesterday) * 100

    daily_growth = percent_change(float(today_revenue), float(yesterday_revenue))

    if previous_month_revenue == 0:
        monthly_growth = 100 if monthly_revenue > 0 else 0
    else:
        monthly_growth = ((monthly_revenue - previous_month_revenue) / previous_month_revenue) * 100

    # KPI
    total = len(items)
    available = sum(1 for i in items if i[6] == "available")
    sold = sum(1 for i in items if i[6] == "sold")

    cur.close()
    conn.close()

    return render_template(
        "Homepage.html",
        items=items,
        total=total,
        available=available,
        sold=sold,
        chartDates=dates,
        chartRevenue=revenue,
        chartProfit=profits,
        today_revenue=float(today_revenue or 0),
        today_profit=float(today_profit or 0),
        yesterday_revenue=float(yesterday_revenue or 0),
        monthly_revenue=float(monthly_revenue or 0),
        monthly_profit=float(monthly_profit or 0),
        daily_growth=daily_growth,
        monthly_growth=monthly_growth
    )


# =========================
# ADD ITEM
# =========================
@app.route("/add", methods=["GET", "POST"])
@login_required
def add_item():

    if request.method == "POST":
        name = request.form["name"]
        brand = request.form["brand"]
        category = request.form["category"]
        buy_price = float(request.form["buy_price"])
        sell_price = float(request.form["sell_price"])

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO items (name, brand, category, buy_price, sell_price, status)
            VALUES (%s, %s, %s, %s, %s, 'available')
        """, (name, brand, category, buy_price, sell_price))

        conn.commit()
        cur.close()
        conn.close()

        return redirect(url_for("products", added="1"))

    return render_template("add_item.html")


# =========================
# SELL ITEM
# =========================
@app.route("/sell/<int:item_id>", methods=["POST"])
@login_required
def sell_item(item_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT buy_price, sell_price, status
        FROM items
        WHERE id = %s
    """, (item_id,))

    item = cur.fetchone()

    if not item:
        cur.close()
        conn.close()
        return "Item not found", 404

    buy_price, sell_price, status = item

    # already sold → just go back to products
    if status == "sold":
        cur.close()
        conn.close()
        return redirect(url_for("products", sold="0"))

    profit = float(sell_price) - float(buy_price)

    # update item status
    cur.execute("""
        UPDATE items
        SET status = 'sold'
        WHERE id = %s
    """, (item_id,))

    # insert into sales table
    cur.execute("""
        INSERT INTO sales (item_id, sold_price, profit, date_sold)
        VALUES (%s, %s, %s, NOW())
    """, (item_id, sell_price, profit))

    conn.commit()
    cur.close()
    conn.close()

    return redirect(url_for("products", sold="1"))

# EDIT BUTTON
@app.route("/edit/<int:item_id>", methods=["POST"])
@login_required
def edit_item(item_id):

    conn = get_connection()
    cur = conn.cursor()

    name = request.form["name"]
    brand = request.form["brand"]
    category = request.form["category"]
    buy_price = float(request.form["buy_price"])
    sell_price = float(request.form["sell_price"])

    cur.execute("""
        UPDATE items
        SET name = %s,
            brand = %s,
            category = %s,
            buy_price = %s,
            sell_price = %s
        WHERE id = %s
    """, (name, brand, category, buy_price, sell_price, item_id))

    conn.commit()
    cur.close()
    conn.close()

    return redirect(url_for("products", updated="1"))

# =========================
# PRODUCTS PAGE
# =========================
@app.route("/products")
@login_required
def products():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, name, brand, category, buy_price, sell_price, status
        FROM items
        WHERE is_archived = FALSE
        ORDER BY id ASC
    """)

    items = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("products.html", items=items)

# =========================
# ARCHIVES PAGE
# =========================
@app.route("/archives")
@login_required
def archives():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, name, brand, category, buy_price, sell_price, status
        FROM items
        WHERE is_archived = TRUE
        ORDER BY id DESC
    """)

    items = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("archives.html", items=items)


# =========================
# ARCHIVE ITEM
# =========================
@app.route("/archive/<int:item_id>", methods=["POST"])
@login_required
def archive_item(item_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id FROM items WHERE id = %s", (item_id,))
    item = cur.fetchone()

    if not item:
        cur.close()
        conn.close()
        return "Item not found", 404

    cur.execute("""
        UPDATE items
        SET is_archived = TRUE
        WHERE id = %s
    """, (item_id,))

    conn.commit()
    cur.close()
    conn.close()

    # send toast flag
    return redirect(url_for("products", archived="1"))


# =========================
# UNARCHIVE ITEM
# =========================
@app.route("/unarchive/<int:item_id>", methods=["POST"])
@login_required
def unarchive_item(item_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE items
        SET is_archived = FALSE
        WHERE id = %s
    """, (item_id,))

    conn.commit()
    cur.close()
    conn.close()

    return redirect(url_for("archives", restored="1"))

# =========================
# SALES PAGE
# =========================
@app.route("/sales")
@login_required
def sales():

    conn = get_connection()
    cur = conn.cursor()

    # =========================
    # SALES LIST (TABLE) 
    # =========================
    cur.execute("""
        SELECT 
            s.date_sold,
            i.name,
            i.brand,
            i.category,
            s.sold_price,
            s.profit
        FROM sales s
        JOIN items i ON i.id = s.item_id
        ORDER BY s.date_sold ASC
    """)
    sales_data = cur.fetchall()

    # =========================
    # BEST SELLING PRODUCT
    # =========================
    cur.execute("""
        SELECT 
            i.name,
            i.brand,
            COUNT(*) AS total_sold
        FROM sales s
        JOIN items i ON i.id = s.item_id
        GROUP BY i.name, i.brand
        ORDER BY total_sold DESC
        LIMIT 1
    """)

    top_product = cur.fetchone()

    if top_product:
        top_product_name = top_product[0]
        top_product_brand = top_product[1]
        top_product_count = top_product[2]
    else:
        top_product_name = "No Sales Yet"
        top_product_brand = ""
        top_product_count = 0

    # =========================
    # CHART (CUMULATIVE PROFIT)
    # =========================
    profits = []
    dates = []
    running_total = 0

    for s in sales_data:
        running_total += float(s[5] or 0)
        dates.append(str(s[0]))
        profits.append(running_total)

    # =========================
    # TODAY STATS
    # =========================
    cur.execute("""
        SELECT 
            COALESCE(SUM(sold_price), 0),
            COALESCE(SUM(profit), 0)
        FROM sales
        WHERE DATE(date_sold) = CURRENT_DATE
    """)
    today_revenue, today_profit = cur.fetchone()

    # =========================
    # MONTH STATS
    # =========================
    cur.execute("""
        SELECT 
            COALESCE(SUM(sold_price), 0),
            COALESCE(SUM(profit), 0)
        FROM sales
        WHERE date_trunc('month', date_sold) =
              date_trunc('month', CURRENT_DATE)
    """)
    monthly_revenue, monthly_profit = cur.fetchone()

    # =========================
    # TOTAL PROFIT
    # =========================
    cur.execute("""
        SELECT COALESCE(SUM(profit), 0)
        FROM sales
    """)
    total_profit = cur.fetchone()[0]

    # =========================
    # CLOSE DB
    # =========================
    cur.close()
    conn.close()

    return render_template(
        "sales.html",

        sales=sales_data,

        dates=dates,
        amounts=profits,

        today_revenue=float(today_revenue or 0),
        today_profit=float(today_profit or 0),

        monthly_revenue=float(monthly_revenue or 0),
        monthly_profit=float(monthly_profit or 0),

        total_profit=float(total_profit or 0),

        top_product_name=top_product_name,
        top_product_brand=top_product_brand,
        top_product_count=top_product_count
    )

# ACCOUNT 
@app.route("/account")
@login_required
def account():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT username, email
        FROM admin_users
        WHERE username = %s
    """, (session["user"],))

    user = cur.fetchone()

    cur.close()
    conn.close()

    return render_template("account.html", user=user)

# UPDATE ACCOUNT
@app.route("/update-account", methods=["POST"])
@login_required
def update_account():

    new_email = request.form["email"]

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE admin_users
        SET email = %s
        WHERE username = %s
    """, (new_email, session["user"]))

    conn.commit()
    cur.close()
    conn.close()

    flash("Account updated successfully!", "success")
    return redirect(url_for("account"))

# =========================
# LOGOUT
# =========================
@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/forgot-password", methods=["POST"])
def forgot_password():

    username = request.form["username"]

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, email
        FROM admin_users
        WHERE username = %s
    """, (username,))

    user = cur.fetchone()

    # Always same response (security)
    if not user:
        cur.close()
        conn.close()
        flash("If the account exists, a reset email has been sent.", "success")
        return redirect(url_for("login"))

    user_id, email = user

    if not email:
        cur.close()
        conn.close()
        flash("No email found for this account.", "error")
        return redirect(url_for("login"))

    token = secrets.token_urlsafe(32)
    expiry = datetime.now() + timedelta(minutes=15)

    cur.execute("""
        UPDATE admin_users
        SET reset_token = %s,
            reset_token_expiry = %s
        WHERE id = %s
    """, (token, expiry, user_id))

    conn.commit()
    cur.close()
    conn.close()

    send_reset_email(email, token, username)

    flash("Reset link sent to email!", "success")
    return redirect(url_for("login"))

@app.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT username, reset_token_expiry
        FROM admin_users
        WHERE reset_token = %s
    """, (token,))

    user = cur.fetchone()

    if not user:
        cur.close()
        conn.close()
        flash("Invalid or expired reset link.", "error")
        return redirect(url_for("login"))

    username, expiry = user

    # check expiry
    if datetime.now() > expiry:
        cur.close()
        conn.close()

        flash("Reset link expired. Please request again.", "error")
        return redirect(url_for("login"))

    if request.method == "POST":
        new_password = request.form["password"]

        if len(new_password) < 8:
            flash("Password must be at least 8 characters.", "error")
            return redirect(request.url)

        hashed = generate_password_hash(new_password)

        cur.execute("""
            UPDATE admin_users
            SET password_hash = %s,
                reset_token = NULL,
                reset_token_expiry = NULL
            WHERE username = %s
        """, (hashed, username))

        conn.commit()
        cur.close()
        conn.close()

        return redirect(url_for("login"))

    cur.close()
    conn.close()

    return render_template("reset_password.html")

# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    app.run(debug=True)