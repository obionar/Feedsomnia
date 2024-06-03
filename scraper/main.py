import time
import logging
from database import create_connection, create_table, sql_insert, DATABASE_PATH
from scrapers import xe, insomnia, offer, dslr, carierista, noiz, bazaraki, ads, urls

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def scrape_and_store(con):
    """
    Scrape data from various websites and store it in the database.

    Parameters:
        con (sqlite3.Connection): The database connection object.
    """
    scrapers = [offer, bazaraki, noiz, carierista, dslr, xe, insomnia]
    for scraper in scrapers:
        scraper()

    if len(ads) > 0:
        for ad in ads:
            sql_insert(con, ad)
        ads.clear()
        logging.info(f'New ads: {len(urls)}')

def main():
    """
    Main function to initialize the database and start the scraping loop.
    """
    con = create_connection(DATABASE_PATH)
    if not con:
        return

    try:
        while True:
            scrape_and_store(con)
            con.commit()  # Ensure any pending transactions are committed
            time.sleep(5)
    except KeyboardInterrupt:
        logging.info("Terminating the script.")
    finally:
        if con:
            con.close()
            logging.info("Database connection closed.")

if __name__ == "__main__":
    main()
