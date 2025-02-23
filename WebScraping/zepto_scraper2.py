from playwright.sync_api import sync_playwright
import pandas as pd

def scrape_zepto():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Change to False to see the browser
        page = browser.new_page()
        page.goto("https://www.zeptonow.com/")  # Open Zepto homepage
        page.wait_for_load_state("networkidle")  # Wait for JavaScript elements to load

        # Extract product names
        product_names = page.locator("h5[data-testid='product-card-name']").all_text_contents()

        # Extract prices
        product_prices = page.locator("h4[data-testid='product-card-price']").all_text_contents()

        # Store data in a structured format
        data = [{"Product": name, "Price": price} for name, price in zip(product_names, product_prices)]
        df = pd.DataFrame(data)

        # Save to CSV
        df.to_csv("zepto_products.csv", index=False)

        print(df)  # Display the scraped data
        browser.close()

scrape_zepto()

