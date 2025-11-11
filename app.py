import sqlite3
from flask import Flask, render_template

app = Flask(__name__)
DATABASE_FILE = "scraper.db"

def get_db_connection():
    """Helper function to connect to the database."""
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

@app.route('/')
def index():
    """
    This is the main page.
    It will fetch all quotes from the database and show them.
    """
    quotes_list = []
    conn = get_db_connection()
    
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT text, author, scraped_at FROM quotes ORDER BY scraped_at DESC")
            rows = cursor.fetchall()
            quotes_list = [dict(row) for row in rows]
        except sqlite3.OperationalError:
            print("Database or 'quotes' table not found.")
            print("Please run 'python scraper.py' at least once to create it.")
        except Exception as e:
            print(f"An error occurred fetching data: {e}")
        finally:
            conn.close()
            
    return render_template('index.html', quotes=quotes_list)

if __name__ == '__main__':
    print("Starting Flask server... Visit http://127.0.0.1:5000/ in your browser.")
    app.run(debug=True, port=5000)