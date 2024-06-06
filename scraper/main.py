#!/usr/bin/env python3
import time
import logging
from database import create_connection, create_table, sql_insert, DATABASE_PATH
from scrapers import ergodotisi, car, xe, insomnia, offer, dslr, carierista, noiz, bazaraki, ads, urls

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def scrape_and_store(con):
    scrapers = [bazaraki, car, offer, noiz, carierista, dslr, xe, insomnia, ergodotisi]
    for scraper in scrapers:
        scraper()

    if len(ads) > 0:
        for ad in ads:
            sql_insert(con, ad)
        ads.clear()
        logging.info(f'New ads: {len(urls)}')

def main():
    con = create_connection(DATABASE_PATH)
    if not con:
        return

    try:
        while True:
            scrape_and_store(con)
            con.commit()  # Ensure any pending transactions are committed
            time.sleep(60) # Sleep between scrapes
    except KeyboardInterrupt:
        logging.info("Terminating the script.")
    finally:
        if con:
            con.close()
            logging.info("Database connection closed.")

if __name__ == "__main__":
    main()
