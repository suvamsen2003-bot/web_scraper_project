import sqlite3
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import datetime

DATABASE_FILE = "scraper.db"
TARGET_URL = "https://quotes.toscrape.com/js/"

def setup_database():
    """Creates the database and the 'quotes' table if they don't exist."""
    print("Setting up database...")
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS quotes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT NOT NULL,
        author TEXT NOT NULL,
        scraped_at TIMESTAMP NOT NULL
    )
    """)
    cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_quote_text ON quotes (text, author)")
    conn.commit()
    conn.close()
    print("Database setup complete.")

def save_quote_to_db(text, author):
    """Saves a single quote to the database, avoiding duplicates."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    scraped_at = datetime.datetime.now()
    
    try:
        cursor.execute(
            "INSERT INTO quotes (text, author, scraped_at) VALUES (?, ?, ?)",
            (text, author, scraped_at)
        )
        conn.commit()
        print(f"SAVED: {author} - {text[:50]}...")
    except sqlite3.IntegrityError:
        print(f"SKIPPED (Duplicate): {author} - {text[:50]}...")
    except Exception as e:
        print(f"Error saving to database: {e}")
    finally:
        conn.close()


def get_selenium_driver():
    """Initializes and returns a headless Selenium Chrome driver."""
    print("Initializing Selenium driver...")
    chrome_options = Options()
    chrome_options.add_argument("--headless")  
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        return driver
    except Exception as e:
        print(f"Error initializing driver: {e}")
        print("Please ensure 'chromedriver.exe' is in your system PATH or the project directory.")
        return None

def run_scraper():
    """
    Main scraping function.
    - Sets up the database.
    - Initializes Selenium.
    - Scrapes all pages of the target site.
    - Saves data to SQLite.
    """
    print("--- Starting Scraper Run ---")
    setup_database()
    driver = get_selenium_driver()
    if not driver:
        return

    current_url = TARGET_URL
    
    try:
        while current_url:
            print(f"Scraping: {current_url}")
            driver.get(current_url)
            
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "quote"))
            )
            
            time.sleep(1)
            
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            
            quote_elements = soup.find_all('div', class_='quote')
            if not quote_elements:
                print("No quotes found, finishing.")
                break
                
            for quote in quote_elements:
                text = quote.find('span', class_='text').get_text(strip=True)
                author = quote.find('small', class_='author').get_text(strip=True)
                save_quote_to_db(text, author)
            
            next_li = soup.find('li', class_='next')
            if next_li and next_li.find('a'):
                relative_url = next_li.find('a')['href']
                current_url = TARGET_URL + relative_url.lstrip('/')
            else:
                print("No 'Next' button found. End of scraping.")
                current_url = None  
                
    except Exception as e:
        print(f"An error occurred during scraping: {e}")
    finally:
        if driver:
            driver.quit()
        print("Selenium driver closed.")
        print("--- Scraper Run Finished ---")


if __name__ == "__main__":
    run_scraper()