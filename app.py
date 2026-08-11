from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
import os

app = Flask(__name__)
app.secret_key = "compose-practice-secret"

def get_db():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "mysql"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", "rootpass"),
        database=os.getenv("MYSQL_DATABASE", "shop")
    )

@app.route("/")
def home():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products ORDER BY id DESC")
    products = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template("index.html", products=products)

@app.route("/add", methods=["POST"])
def add_product():
    name = request.form["name"].strip()
    price = request.form["price"].strip()
    if not name or not price:
        flash("Name and price are required.")
        return redirect(url_for("home"))
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO products (name, price) VALUES (%s, %s)", (name, price))
    db.commit()
    cursor.close()
    db.close()
    flash("Product added successfully.")
    return redirect(url_for("home"))

@app.route("/delete/<int:product_id>", methods=["POST"])
def delete_product(product_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
    db.commit()
    cursor.close()
    db.close()
    flash("Product deleted.")
    return redirect(url_for("home"))

@app.route("/health")
def health():
    try:
        db = get_db()
        db.close()
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        return {"status": "error", "database": str(e)}, 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
