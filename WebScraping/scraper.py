import sqlite3
import pandas as pd
from playwright.sync_api import sync_playwright

# Connect to SQLite database (or create if not exists)
conn = sqlite3.connect("products.db")
cursor = conn.cursor()

# Create table if it doesn’t exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    price TEXT
)
""")

def scrape_zepto():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Change to False for debugging
        page = browser.new_page()
        page.goto("https://www.zeptonow.com/")
        page.wait_for_load_state("networkidle")

        product_names = page.locator("h5[data-testid='product-card-name']").all_text_contents()
        product_prices = page.locator("h4[data-testid='product-card-price']").all_text_contents()

        # Insert scraped data into SQLite
        cursor.executemany("INSERT INTO products (name, price) VALUES (?, ?)", zip(product_names, product_prices))
        conn.commit()

        print(f"Stored {len(product_names)} products in the database!")
        browser.close()

# Run the scraper
scrape_zepto()

# Close the database connection
conn.close()
