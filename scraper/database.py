import sqlite3
from sqlite3 import Error
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Path to the SQLite database file
DATABASE_PATH = '../feeds.db'

def create_connection(db_file=DATABASE_PATH):
    """
    Create a database connection to the SQLite database specified by db_file.

    Parameters:
        db_file (str): The database file path.

    Returns:
        conn (sqlite3.Connection): The database connection object, or None if an error occurs.
    """
    try:
        conn = sqlite3.connect(db_file)
        logging.info("Connection to database established.")
        return conn
    except Error as e:
        logging.error(f"Error: {e}")
        return None

def create_table(conn):
    """
    Create the Feeds table in the database if it doesn't exist.

    Parameters:
        conn (sqlite3.Connection): The database connection object.
    """
    try:
        sql_create_feeds_table = """
        CREATE TABLE IF NOT EXISTS Feeds (
            id INTEGER PRIMARY KEY,
            Title TEXT NOT NULL,
            Price INTEGER,
            Description TEXT,
            URL TEXT NOT NULL UNIQUE,
            Date TEXT NOT NULL,
            Sitename TEXT NOT NULL,
            Country TEXT NOT NULL
        );
        """
        cur = conn.cursor()
        cur.execute(sql_create_feeds_table)
        logging.info("Feeds table created or already exists.")
    except Error as e:
        logging.error(f"Error: {e}")

def sql_insert(conn, entities):
    """
    Insert a new ad into the Feeds table.

    Parameters:
        conn (sqlite3.Connection): The database connection object.
        entities (tuple): A tuple containing the ad data (Title, Price, Description, URL, Date, Sitename, Country).
    """
    try:
        sql_insert_ad = """
        INSERT OR IGNORE INTO Feeds(Title, Price, Description, URL, Date, Sitename, Country)
        VALUES(?, ?, ?, ?, ?, ?, ?);
        """
        cur = conn.cursor()
        cur.execute(sql_insert_ad, entities)
        conn.commit()
        logging.info("Ad inserted into Feeds table.")
    except Error as e:
        logging.error(f"Error: {e}")

def initialize_database():
    """
    Initialize the database and create the Feeds table if it doesn't exist.
    """
    conn = create_connection()
    if conn is not None:
        create_table(conn)
    else:
        logging.error("Error! Cannot create the database connection.")
    return conn

if __name__ == "__main__":
    conn = initialize_database()
    if conn:
        conn.close()
