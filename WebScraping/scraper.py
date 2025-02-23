import sqlite3
import time
from playwright.sync_api import sync_playwright

# Connect to SQLite database
conn = sqlite3.connect("products.db")
cursor = conn.cursor()

# Drop existing table (if necessary) and create a fresh one
cursor.execute("DROP TABLE IF EXISTS products")
cursor.execute("""
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    price TEXT,
    category TEXT
)
""")
conn.commit()

def scrape_category(page, category_name):
    """Scrape product details from a given category page."""
    time.sleep(2)  # Allow page to load

    # Scroll multiple times to load all products
    for _ in range(20):  
        page.mouse.wheel(0, 5000)
        time.sleep(2)

    # Extract product names
    product_names = page.locator("h5[data-testid='product-card-name']").all_text_contents()

    # Extract prices
    product_prices = page.locator("h4[data-testid='product-card-price']").all_text_contents()

    # Ensure both lists are of the same length (handle mismatches)
    if len(product_names) != len(product_prices):
        print(f"⚠️ Mismatch: {len(product_names)} names, {len(product_prices)} prices in {category_name}")

    # Store in database
    for name, price in zip(product_names, product_prices):
        cursor.execute("INSERT INTO products (name, price, category) VALUES (?, ?, ?)", (name, price, category_name))
    
    conn.commit()
    print(f"✅ Stored {len(product_names)} products from {category_name}")

def scrape_zepto():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://www.zeptonow.com/")  
        page.wait_for_load_state("networkidle")

        # Extract category links
        category_elements = page.locator("a.contents").all()  
        categories = [(element.text_content().strip(), element.get_attribute("href")) for element in category_elements if element.get_attribute("href")]

        for category_name, category_url in categories:
            full_url = f"https://www.zeptonow.com{category_url}"
            print(f"🔍 Scraping category: {category_name} -> {full_url}")
            
            page.goto(full_url)  # Visit category page
            scrape_category(page, category_name)

        browser.close()

# Run the scraper
scrape_zepto()

# Close database connection
conn.close()
