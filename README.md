# Feedsomnia

Feedsomnia is a web application for searching classified ads efficiently. It scrapes various websites for ads and stores them in a SQLite database, which can be searched via a web interface.


## Usage

1. **Scrape ads and store them in the database**:
    ```bash
    python scraper/main.py
    ```

2. **Run the web application**:
    ```bash
    python webapp/webapp.py
    ```

3. **Access the web interface**:
    Open a browser and go to `http://127.0.0.1:5000/`.

## Directory Structure

- `scraper/`: Contains the scraping scripts and database management.
- `webapp/`: Contains the Flask application and related files.
- `requirements.txt`: Lists the dependencies.
- `README.md`: Project documentation.
- `LICENSE`: Project license.

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.
