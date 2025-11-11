import sqlite3
import csv
import datetime

DATABASE_FILE = "scraper.db"
CSV_FILE = "quotes.csv"

def export_to_csv():
    """Fetches all data from the 'quotes' table and saves it to a CSV file."""
    print(f"Connecting to database: {DATABASE_FILE}")
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        
        print("Fetching all data from 'quotes' table...")
        cursor.execute("SELECT text, author, scraped_at FROM quotes ORDER BY scraped_at DESC")
        rows = cursor.fetchall()
        
        if not rows:
            print("Database is empty. No CSV file to create.")
            print("Try running 'python scraper.py' first.")
            return

        print(f"Found {len(rows)} rows. Writing to {CSV_FILE}...")
        
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['text', 'author', 'scraped_at'])
            writer.writerows(rows)
            
        print(f"Successfully exported data to {CSV_FILE}")

    except sqlite3.OperationalError:
        print(f"Error: Database file '{DATABASE_FILE}' not found.")
        print("Have you run the scraper at least once (e.g., `python scraper.py`)?")
    except Exception as e:
        print(f"An error occurred during CSV export: {e}")
    finally:
        if 'conn' in locals() and conn:
            conn.close()

if __name__ == "__main__":
    export_to_csv()