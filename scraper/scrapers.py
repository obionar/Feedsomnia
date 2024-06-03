import datetime
import time
import requests
from bs4 import BeautifulSoup
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# User agent for web requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36'
}

# Lists to store ads and URLs
ads = []
urls = []

def handle_exceptions(func):
    """Decorator to handle exceptions and log errors."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Error in {func.__name__}: {e}")
            return None
    return wrapper

@handle_exceptions
def fetch_url(url):
    """Fetch content from a URL with error handling."""
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.content

def formatted_current_time():
    """Return the current time formatted as YYYY-MM-DD HH:MM:SS"""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

####################### XE.GR #######################
@handle_exceptions
def xe():
    Sitename = 'xe.gr'
    Country = 'gr'
    url = 'https://www.xe.gr/search?System.item_type=xe_stelexos&sort_by=Publication.effective_date_start&sort_direction=desc'
    content = fetch_url(url)
    if not content:
        return

    soup = BeautifulSoup(content, 'html.parser')
    new_ads_block = soup.find('div', id='xeResultsColumn')
    summaries = new_ads_block.find_all('div', class_='rSummary')

    for summary in summaries:
        a_tag = summary.find('a')
        if a_tag:
            Title = a_tag.text
            URL = 'https://www.xe.gr' + a_tag['href']
            Description = (summary.find('p').text + ' ' + Title).lower()
            
            try:
                Price = int(summary.find('span', class_='rPriceLabel').text.replace('€', '').replace('.', '').replace(',', '').strip())
            except (AttributeError, ValueError):
                Price = 0

            if URL not in urls:
                Date = formatted_current_time()
                urls.append(URL)
                ad = (Title, Price, Description, URL, Date, Sitename, Country)
                logging.info(f"{Sitename}: {Title}")
                ads.append(ad)

####################### INSOMNIA.GR #######################
@handle_exceptions
def insomnia():
    Sitename = 'insomnia.gr'
    Country = 'gr'
    url = 'https://www.insomnia.gr/classifieds/'
    content = fetch_url(url)
    if not content:
        return

    soup = BeautifulSoup(content, 'html.parser')
    new_ads_block = soup.find('ul', class_='cWidget__body')
    summaries = new_ads_block.find_all('li', class_='ipsStreamItem')

    for summary in summaries:
        a_tag = summary.find('a', class_='ipsStreamItem_title')
        if a_tag:
            Title = a_tag.text
            URL = a_tag['href']
            Description = (summary.find('div', class_='ipsStreamItem_snippet').text + ' ' + Title).lower()
            
            try:
                Price = int(summary.find('span', class_='ipsStreamItem_price').text.replace('€', '').replace('.', '').replace(',', '').strip())
            except (AttributeError, ValueError):
                Price = 0

            if URL not in urls:
                Date = formatted_current_time()
                urls.append(URL)
                ad = (Title, Price, Description, URL, Date, Sitename, Country)
                logging.info(f"{Sitename}: {Title}")
                ads.append(ad)

####################### OFFER.GR #######################
@handle_exceptions
def offer():
    Sitename = 'offer.gr'
    Country = 'gr'
    url = 'https://www.offer.gr/ads'
    content = fetch_url(url)
    if not content:
        return

    soup = BeautifulSoup(content, 'html.parser')
    new_ads_block = soup.find('div', class_='container')
    summaries = new_ads_block.find_all('div', class_='listing-item')

    for summary in summaries:
        a_tag = summary.find('a', class_='listing-item__link')
        if a_tag:
            Title = a_tag['title']
            URL = 'https://www.offer.gr' + a_tag['href']
            Description = (summary.find('div', class_='listing-item__desc').text + ' ' + Title).lower()
            
            try:
                Price = int(summary.find('span', class_='listing-item__price').text.replace('€', '').replace('.', '').replace(',', '').strip())
            except (AttributeError, ValueError):
                Price = 0

            if URL not in urls:
                Date = formatted_current_time()
                urls.append(URL)
                ad = (Title, Price, Description, URL, Date, Sitename, Country)
                logging.info(f"{Sitename}: {Title}")
                ads.append(ad)

####################### DSLR.GR #######################
@handle_exceptions
def dslr():
    Sitename = 'dslr.gr'
    Country = 'gr'
    url = 'https://www.dslr.gr/classifieds'
    content = fetch_url(url)
    if not content:
        return

    soup = BeautifulSoup(content, 'html.parser')
    new_ads_block = soup.find('div', class_='ipsWidget_inner')
    summaries = new_ads_block.find_all('li', class_='ipsDataItem')

    for summary in summaries:
        a_tag = summary.find('a', class_='ipsDataItem_title')
        if a_tag:
            Title = a_tag.text
            URL = a_tag['href']
            Description = (summary.find('div', class_='ipsDataItem_meta').text + ' ' + Title).lower()
            
            try:
                Price = int(summary.find('span', class_='ipsDataItem_price').text.replace('€', '').replace('.', '').replace(',', '').strip())
            except (AttributeError, ValueError):
                Price = 0

            if URL not in urls:
                Date = formatted_current_time()
                urls.append(URL)
                ad = (Title, Price, Description, URL, Date, Sitename, Country)
                logging.info(f"{Sitename}: {Title}")
                ads.append(ad)

####################### CARIERISTA.COM #######################
@handle_exceptions
def carierista():
    Country = 'cy'
    Sitename = 'carierista.com'
    url = 'https://www.carierista.com/en/jobs'
    content = fetch_url(url)
    if not content:
        return

    soup = BeautifulSoup(content, 'html.parser')
    summaries = soup.find_all('div', class_='position')

    for summary in summaries:
        a_tag = summary.find('a', class_='position-link')
        if a_tag:
            Title = a_tag.find('h3').text
            URL = 'https://www.carierista.com' + a_tag['href']
            Category = summary.find('span', class_='position-category').text
            Description = (Title + ' - ' + Category + ' - ' + soup.find('div', class_="position-desc").text.strip() + Sitename).lower()
            Date = formatted_current_time()
            Price = 0

            if URL not in urls:
                urls.append(URL)
                ad = (Title, Price, Description, URL, Date, Sitename, Country)
                logging.info(f"{Sitename}: {Title}")
                ads.append(ad)

####################### SMART.NOIZ.GR #######################
@handle_exceptions
def noiz():
    Country = 'gr'
    Sitename = 'smart.noiz.gr'
    recent_ads_url = 'https://smart.noiz.gr/recent_ads.php'
    content = fetch_url(recent_ads_url)
    if not content:
        return

    soup = BeautifulSoup(content, 'lxml')
    titles = soup.find_all('div', class_='title')

    for title in titles:
        ad_url = title.find('a')['href']
        if ad_url and ad_url not in urls:
            urls.append(ad_url)
            fetch_noiz_ad_details(ad_url, Sitename, Country)

@handle_exceptions
def fetch_noiz_ad_details(URL, Sitename, Country):
    content = fetch_url(URL)
    if not content:
        return

    soup = BeautifulSoup(content, 'lxml')
    try:
        Price = int(soup.find('div', class_='dt-price price').text.strip().replace('€', '').replace('.', '').replace(',', '').strip())
    except AttributeError:
        Price = 0

    top_section = soup.find('div', class_='details-top')
    cat = top_section.find('div', class_='cat-path dtl').find_all('a')[1].text
    Title = top_section.find('h1').text + ' / ' + cat
    fdesc = soup.find_all('div', class_='fdesc ld')[0].text.strip().replace('\n', '').replace('  ', '')
    pdesc = soup.find_all('div', class_='fdesc ld')[1].text.strip().replace('\n', '').replace('  ', '')
    Description = fdesc + ' / ' + pdesc

    Date = formatted_current_time()
    ad = (Title, Price, Description, URL, Date, Sitename, Country)
    logging.info(f"{Sitename}: {Title}")
    ads.append(ad)

####################### BAZARAKI.COM #######################
@handle_exceptions
def bazaraki():
    Country = 'cy'
    Sitename = 'bazaraki.com'
    search_url = 'https://www.bazaraki.com/search/'

    content = fetch_url(search_url)
    if not content:
        return

    soup = BeautifulSoup(content, 'lxml')
    titles = soup.find_all('div', class_='offer-title')

    for title in titles:
        ad_url = 'https://www.bazaraki.com' + title.find('a')['href']
        if ad_url and ad_url not in urls:
            urls.append(ad_url)
            fetch_bazaraki_ad_details(ad_url, Sitename, Country)

@handle_exceptions
def fetch_bazaraki_ad_details(URL, Sitename, Country):
    content = fetch_url(URL)
    if not content:
        return

    soup = BeautifulSoup(content, 'lxml')
    Title = soup.find('h1', class_='offer-title').text.strip()
    try:
        Price = int(soup.find('div', class_='price-value').text.strip().replace('€', '').replace('.', '').replace(',', '').strip())
    except AttributeError:
        Price = 0

    desc_block = soup.find('div', class_='text-description')
    Description = desc_block.text.strip().replace('\n', '').replace('  ', '')

    Date = formatted_current_time()
    ad = (Title, Price, Description, URL, Date, Sitename, Country)
    logging.info(f"{Sitename}: {Title}")
    ads.append(ad)

if __name__ == "__main__":
    # Run each scraper standalone for debugging and experiments
    scrapers = [xe, insomnia, offer, dslr, carierista, noiz, bazaraki]
    for scraper in scrapers:
        scraper()
    
    # Print the number of collected ads
    print(f"Total collected ads: {len(ads)}")
