import json
import os
import time
from playwright.sync_api import sync_playwright, Page, Browser

def authenticate_and_save_session(browser: Browser, session_file: str) -> Page:
    context = browser.new_context()
    page = context.new_page()
    
    page.goto("https://www.example.com/login")

    page.locator("#username-input").fill("user@example.com")
    page.locator("#password-input").fill("password123")
    page.locator("button#login-button").click()

    page.wait_for_url("https://www.example.com/dashboard")

    context.storage_state(path=session_file)
    print("New session created and saved.")
    
    return context.new_page()

def navigate_to_products(page: Page):
    print("Navigating to the product table...")
    page.locator("text=Menu").click()
    page.locator("text=Data Management").click()
    page.locator("text=Inventory").click()
    page.locator("text=View All Products").click()
    page.wait_for_load_state('domcontentloaded')

def scrape_all_pages(page: Page) -> list:
    all_products = []
    page_number = 1
    
    while True:
        print(f"Scraping page {page_number}...")
        
        page.wait_for_selector('table.products-table')

        headers = [th.inner_text().strip() for th in page.locator('table.products-table thead th').all()]
        
        rows = page.locator('table.products-table tbody tr').all()
        
        for row in rows:
            cells = row.locator('td').all()
            if cells:
                product_data = {}
                for i, cell in enumerate(cells):
                    if i < len(headers):
                        product_data[headers[i]] = cell.inner_text().strip()
                all_products.append(product_data)
        
        next_button = page.locator('button.next-page')
        
        if not next_button.is_visible() or next_button.is_disabled():
            break
        
        next_button.click()
        page.wait_for_load_state('networkidle')
        page_number += 1
        
    return all_products

def run(playwright):
    browser = playwright.chromium.launch(headless=False)
    session_file = "state.json"
    page = None
    
    if os.path.exists(session_file):
        print("Existing session found. Loading session state...")
        context = browser.new_context(storage_state=session_file)
        page = context.new_page()
        page.goto("https://www.example.com/dashboard")
        
        if "login" in page.url:
            print("Session expired. Re-authenticating...")
            page.close()
            context.close()
            page = authenticate_and_save_session(browser, session_file)
        else:
            print("Session loaded successfully.")
    else:
        print("No existing session found. Authenticating and creating a new session...")
        page = authenticate_and_save_session(browser, session_file)
    
    try:
        navigate_to_products(page)

        all_products = scrape_all_pages(page)

        print(f"Exporting {len(all_products)} products to products.json...")
        with open("products.json", "w") as f:
            json.dump(all_products, f, indent=4)
        
        print("Data extraction complete. products.json file created.")

    finally:
        page.close()
        page.context.close()
        browser.close()

if __name__ == "__main__":
    with sync_playwright() as p:
        run(p)

