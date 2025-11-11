Automated Web Scraper with Scheduler & Dashboard
  This project is a complete, automated data pipeline. It scrapes dynamic (JavaScript-rendered) websites, stores the collected data in an SQLite database, and runs the scraper on an automated schedule. It also includes a lightweight Flask web server to display the collected data on a local dashboard.
  This project was built to scrape quotes.toscrape.com/js/ , a website that requires JavaScript to load its content.

Features
  Dynamic Scraping: Uses Selenium to control a real web browser, allowing it to scrape sites that load content with JavaScript.
  Data Parsing: Uses BeautifulSoup4 to parse the rendered HTML and extract specific data.
  Persistent Storage: Saves all collected data in a local SQLite database ( scraper.db ).
  Automation: Uses Celery and Celery Beat to run the scraper on a recurring schedule (e.g., every 30 minutes).
  Web Dashboard: A simple Flask app ( app.py ) reads from the database and displays all collected quotes on a webpage.
 	Data Export: Includes a utility script ( export.py ) to export the data from the database to a
  quotes.csv file.

Technology Stack
  Python 3
  Selenium: For browser automation.
  BeautifulSoup4: For HTML parsing.
  SQLite: For the local, file-based database.
  Celery: For managing and scheduling the automated background tasks.
  Redis: As the message broker for Celery.
 	Flask: To run the web server and display the data.

File Structure

.
├── .gitignore	# Tells Git which files to ignore (like venv, .db, .csv)
├── app.py	# The Flask web server for the dashboard
├── export.py	# Utility script to export data to CSV
├── requirements.txt	# All Python libraries needed for the project
├── scraper.py	# The main Selenium/BS4 web scraping script
├── tasks.py	# Celery configuration and task scheduler
├── scraper.db	# (Will be created) The SQLite database
├── quotes.csv	# (Will be created) The exported CSV file
└── templates/
└── index.html	# The HTML page for the web dashboard
 




Setup & Installation
  1.	Clone the Repository:


    git clone [https://github.com/suvamsen2003-bot/web_scraper_project.git](https://git cd web_scraper_project




  2.	Create and Activate Virtual Environment:


    # Create the environment python -m venv venv

    # Activate it (Windows)
    .\venv\Scripts\activate

    # Or (if using Command Prompt - .bat)
    .\venv\Scripts\activate.bat

    # Or (if using Mac/Linux) source venv/bin/activate




  3.	Install Python Libraries:


    pip install -r requirements.txt




  4.	Install External Tools:
    Redis: This is required for Celery. You must install and run the Redis server.
 	  ChromeDriver: Download the chromedriver.exe that matches your version of Google Chrome. Place the chromedriver.exe file in the main web_scraper_project folder.

How to Run
  There are three ways to run this project. Make sure your venv is active for all of them.

  1.	Run a Manual Scrape (To Get Initial Data)
  This will run the scraper one time and fill the scraper.db database.


    python scraper.py



  2.	View the Data on the Web App
  This will start the Flask website so you can see the data in your database.


    python app.py

  After it starts, open your browser and go to: http://127.0.0.1:5000/


  3.	Run the Full Automated System
  This is the "production" mode. It runs the scheduler, the worker, and the web server all at once. This requires three separate terminals, all with the venv activated.
  Terminal 1 (Start the Celery Worker):
    This terminal waits for jobs.


    celery -A tasks worker --loglevel=info



  Terminal 2 (Start the Celery Beat Scheduler):
    This terminal sends the "run" job every 30 minutes.


    celery -A tasks beat --loglevel=info



  Terminal 3 (Start the Web Server):
   	This terminal runs your website.


    python app.py


  Now, the scraper will run in the background every 30 minutes, and you can watch the new data appear on http://127.0.0.1:5000/ .

  Exporting Data to CSV
  To export all the data from scraper.db into a quotes.csv file, run:


    python export.py
