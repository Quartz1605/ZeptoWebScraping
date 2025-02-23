from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

# Route for displaying data
@app.route('/')
def dashboard():
    # Connect to database
    conn = sqlite3.connect("products.db")
    cursor = conn.cursor()

    # Fetch all products
    cursor.execute("SELECT name, price FROM products")
    products = cursor.fetchall()

    conn.close()
    
    return render_template("dashboard.html", products=products)

if __name__ == '__main__':
    app.run(debug=True)
