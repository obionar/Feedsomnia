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
                Date = datetime.datetime.fromtimestamp(int(time.time()))
                urls.append(URL)
                ad = (Title, Price, Description, URL, Date, Sitename, Country)
                logging.info(f"{Date} {Sitename}: {Title}")
                ads.append(ad)

####################### INSOMNIA.GR #######################
@handle_exceptions
def insomnia():
    Country = 'gr'
    Sitename = 'insomnia.gr'
    url = 'https://www.insomnia.gr/classifieds/'
    content = fetch_url(url)
    if not content:
        return

    soup = BeautifulSoup(content, 'html.parser')
    ads_block = soup.find('section', class_='classifieds-index-adverts-latest')
    h4_tags = ads_block.find_all('h4')

    for h4 in h4_tags:
        ad_url = h4.find('a')['href']
        if ad_url and ad_url not in urls:
            urls.append(ad_url)
            fetch_insomnia_ad_details(ad_url, Sitename, Country)

@handle_exceptions
def fetch_insomnia_ad_details(URL, Sitename, Country):
    content = fetch_url(URL)
    if not content:
        return

    soup = BeautifulSoup(content, 'html.parser')
    top_section = soup.find('div', class_='classifieds-product-title')
    if not top_section:
        return

    Date = datetime.datetime.fromtimestamp(int(time.time()))
    Title = top_section.find('h4', class_='ipsType_sectionHead ipsType_break ipsType_bold ipsTruncate ipsSpacer_bottom ipsType_reset').text
    Price = int(top_section.find('span', class_='cFilePrice').text.replace('€', '').replace('.', '').replace(',', '').strip()) if top_section.find('span', class_='cFilePrice') else 0
    article_section = soup.find('div', class_='classifieds-product-tabs-outer-wrap').find('section').text.strip()
    Description = (article_section.replace('\n', ' ') + ' ' + Title).lower()

    ad = (Title, Price, Description, URL, Date, Sitename, Country)
    logging.info(f"{Date} {Sitename}: {Title}")
    ads.append(ad)

####################### OFFER.COM.CY #######################
@handle_exceptions
def offer():
    Country = 'cy'
    Sitename = 'offer.com.cy'
    url = 'https://www.offer.com.cy/en/offers-cy/20/'
    content = fetch_url(url)
    if not content:
        return

    soup = BeautifulSoup(content, 'lxml')
    ad_list = soup.find('div', class_='cls_list')

    for item in ad_list.find_all('div', class_='item'):
        t = item.find('h3', class_='title-a')
        a_tag = t.find('a')['href']
        ad_url = 'https://www.offer.com.cy' + a_tag
        if ad_url and ad_url not in urls:
            urls.append(ad_url)
            fetch_offer_ad_details(ad_url, Sitename, Country)

@handle_exceptions
def fetch_offer_ad_details(URL, Sitename, Country):
    content = fetch_url(URL)
    if not content:
        return

    soup = BeautifulSoup(content, 'html.parser')
    article = soup.find('article')
    if not article:
        return

    Date = datetime.datetime.fromtimestamp(int(time.time()))
    Title = article.find('h1', class_='mf_s_b det-head').text
    Price = int(article.find('p', class_='ad_price b_r_4 top_mar_d mf_s mf_s_c').text.split()[1].replace('€', '').replace('.', '').replace(',', '').strip()) if article.find('p', class_='ad_price b_r_4 top_mar_d mf_s mf_s_c') else 0

    try:
        Description = article.find('div', class_='top_mar_b e_b').text.replace('Information from owner', '').strip() + ' ' + Title
    except AttributeError:
        logging.warning('Wrong description')
        Description = Title

    Description = Description.lower()
    ad = (Title, Price, Description, URL, Date, Sitename, Country)
    logging.info(f"{Date} {Sitename}: {Title}")
    ads.append(ad)

####################### DSLR.GR #######################
@handle_exceptions
def dslr():
    Country = 'gr'
    Sitename = 'dslr.gr'
    recent_url = 'https://dslr.gr/recent/'
    content = fetch_url(recent_url)
    if not content:
        return

    soup = BeautifulSoup(content, 'html.parser')
    a_tags = soup.find_all('a', class_='no_underline')

    for a in a_tags:
        if '/product/' in a['href']:
            ad_url = 'https://dslr.gr' + a['href']
            if ad_url and ad_url not in urls:
                urls.append(ad_url)
                fetch_dslr_ad_details(ad_url, Sitename, Country)

@handle_exceptions
def fetch_dslr_ad_details(URL, Sitename, Country):
    content = fetch_url(URL)
    if not content:
        return

    soup = BeautifulSoup(content, 'html.parser')
    breadcrumb = soup.find('ol', class_='breadcrumb').find_all('li')
    if len(breadcrumb) < 4:
        return

    Category = breadcrumb[2].text
    Title = '{} ({})'.format(breadcrumb[3].text, breadcrumb[2].text)
    info_call = soup.find('div', class_='col-lg-6 col-md-6 col-sm-6 col-xs-12 info_call')
    Price = int(info_call.find_all('div', class_='info')[1].find('span').text.replace('€', '').replace('.', '').replace(',', '').strip()) if info_call.find_all('div', class_='info') else 0

    Description = (Title + info_call.text.strip().replace('\n', ' ') + Sitename).lower()
    Date = datetime.datetime.fromtimestamp(int(time.time()))
    ad = (Title, Price, Description, URL, Date, Sitename, Country)
    logging.info(f"{Date} {Sitename}: {Title}")
    ads.append(ad)

####################### CARIERISTA.COM #######################
@handle_exceptions
def carierista():
    Country = 'cy'
    Sitename = 'carierista.com'
    url = "https://www.carierista.com/en/jobs/search"
    content = fetch_url(url)
    if not content:
        return

    soup = BeautifulSoup(content, 'html.parser')
    jobs = soup.find_all('div', class_="position-details col-xs-12 col-md-8 matched-height")

    for job in jobs:
        job_url = job.find_all('a')[0]['href']
        cat = job.find('p', class_="cat").find_all('span')
        Title = job.find('h5').text
        Category = cat[1].text + ' / ' + cat[0].text
        if job_url and job_url not in urls:
            urls.append(job_url)
            fetch_carierista_ad_details(job_url, Title, Category, Sitename, Country)

@handle_exceptions
def fetch_carierista_ad_details(URL, Title, Category, Sitename, Country):
    content = fetch_url(URL)
    if not content:
        return

    soup = BeautifulSoup(content, 'html.parser')
    Description = (Title + ' - ' + Category + ' - ' + soup.find('div', class_="position-desc").text.strip() + Sitename).lower()
    Date = datetime.datetime.fromtimestamp(int(time.time()))
    Price = 0

    ad = (Title, Price, Description, URL, Date, Sitename, Country)
    logging.info(f"{Date} {Sitename}: {Title}")
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
    pdesc = soup.find('div', id='pdescription').text
    Description = (Title + fdesc + pdesc + Sitename).lower()
    Date = datetime.datetime.fromtimestamp(int(time.time()))
    ad = (Title, Price, Description, URL, Date, Sitename, Country)
    logging.info(f"{Date} {Sitename}: {Title}")
    ads.append(ad)

####################### BAZARAKI.COM #######################
@handle_exceptions
def bazaraki():
    Country = 'cy'
    Sitename = 'bazaraki.com'
    url = 'https://m.bazaraki.com/search/'
    content = fetch_url(url)
    if not content:
        return

    soup = BeautifulSoup(content, 'html.parser')
    new_ads = soup.find('div', class_='list-announcement__items')

    for a in soup.find_all('a', class_='name'):
        ad_url = 'https://m.bazaraki.com' + a['href']
        if ad_url and ad_url not in urls:
            urls.append(ad_url)
            fetch_bazaraki_ad_details(ad_url, Sitename, Country)

@handle_exceptions
def fetch_bazaraki_ad_details(URL, Sitename, Country):
    content = fetch_url(URL)
    if not content:
        return

    soup = BeautifulSoup(content, 'html.parser')
    Date = datetime.datetime.fromtimestamp(int(time.time()))
    Title = soup.find('h1', class_='item__title').text

    try:
        Price = float(soup.find('div', class_='item__price').text.strip().split()[0].replace('.', '').replace('€', ' ').replace(',', '.').strip())
    except (AttributeError, ValueError):
        Price = 0

    Desc = soup.find('div', class_='js-description')
    City = soup.find('div', class_='city-bar').text.strip()
    Description = (Title + ' ' + City + ' ' + Desc.text.strip()).lower()

    ad = (Title, Price, Description, URL, Date, Sitename, Country)
    logging.info(f"{Date} {Sitename}: {Title}")
    ads.append(ad)


###################### ERGODOTISI.COM ######################
@handle_exceptions
def ergodotisi():
    ergodotisi_country = 'cy'
    ergodotisi_sitename = 'ergodotisi.com'
    url = 'https://www.ergodotisi.com/en/SearchResults.aspx?q='
    content = fetch_url(url)
    if not content:
        return

    ergodotisi_adlist_soup = BeautifulSoup(content, 'html.parser')
    ergodotisi_ads = ergodotisi_adlist_soup.find_all('a', class_='text-orane ref-number font-weight-bold')
    for ergodotisi_ad in ergodotisi_ads:
        ergodotisi_ad_url = 'https://www.ergodotisi.com/en/' + ergodotisi_ad['href']
        if ergodotisi_ad_url not in urls:
            ergodotisi_ad_content = fetch_url(ergodotisi_ad_url)
            if not ergodotisi_ad_content:
                return
            ergodotisi_ad_soup = BeautifulSoup(ergodotisi_ad_content, 'html.parser')
            ergodotisi_ad_title = ergodotisi_ad_soup.find('h1').text
            ergodotisi_ad_category = ergodotisi_ad_soup.find('div', class_='col-md-12 seprate-box-border m-t-2 m-b-2 p-t-1').text
            ergodotisi_ad_description = ergodotisi_ad_soup.find('div', class_='col-md-12 description-part alpha').text
            ergodotisi_ad_description = (ergodotisi_ad_description + ' ' + ergodotisi_ad_category + ' ' + ergodotisi_sitename).strip().lower()
            ergodotisi_ad_date = datetime.datetime.fromtimestamp(int(time.time()))
            ad = (ergodotisi_ad_title, 0, ergodotisi_ad_description, ergodotisi_ad_url, ergodotisi_ad_date, ergodotisi_sitename, ergodotisi_country)
            logging.info(f"{ergodotisi_sitename}: {ergodotisi_ad_title}")
            urls.append(ergodotisi_ad_url)
            ads.append(ad)


##################### CAR.GR #####################
@handle_exceptions
def car():
    car_country = 'gr'
    car_sitename = 'car.gr'
    url = 'https://www.car.gr/xyma/?category=50&created=%3E1'
    content = fetch_url(url)
    if not content:
        return

    car_adlist_soup = BeautifulSoup(content, 'html.parser')
    car_ads = car_adlist_soup.find_all('a', class_='row-anchor')
 
    for car_ad in car_ads:
        car_ad_url = 'https://www.car.gr' + car_ad['href']
        if car_ad_url not in urls:
            car_ad_content = fetch_url(car_ad_url)
            if not car_ad_content:
                return
            car_ad_soup = BeautifulSoup(car_ad_content, 'html.parser')
            car_ad_title = car_ad_soup.find('h1' , class_='tw-font-bold tw-text-2xl tw-mb-0 classified-title tw-mt-2 tw-block').text.strip()

            try:
                car_ad_price = car_ad_soup.find('h3', class_='tw-text-3xl tw-font-extrabold tw-mt-2 tw-opacity-95 tw-block tw-leading-normal tw-text-center tw-rounded tw-flex-shrink-0 price-only tw-mb-0 tw-mr-3 tw-text-grey-800').text
                car_ad_price = int(car_ad_price.replace('€', '').replace('.', '').replace(',', '').strip())
            except AttributeError:
                car_ad_price = 0
            car_ad_description = car_ad_soup.find('div', class_='tw-overflow-hidden tw-ease-out tw-duration-200 tw-transition-[max-height] print-full-height tw-whitespace-pre-wrap').text
            car_ad_description = (car_ad_description + ' ' + car_ad_title + ' ' + car_sitename).strip().lower()
            car_ad_date = datetime.datetime.fromtimestamp(int(time.time()))
            ad = (car_ad_title, car_ad_price, car_ad_description, car_ad_url, car_ad_date, car_sitename, car_country)
            logging.info(f"{car_sitename}: {car_ad_title}")
            urls.append(car_ad_url)
            ads.append(ad)
    


# Main function for standalone execution
if __name__ == "__main__":
    #scrapers = [xe, insomnia, offer, dslr, carierista, noiz, bazaraki]
    scrapers = [ergodotisi, car]
    for scraper in scrapers:
        scraper()
    
    # Print collected ads
    for ad in ads:
        print(ad)
