import requests 
from tqdm import tqdm
from constants import *
from bs4 import BeautifulSoup
from collections import defaultdict


"""
get_restaurants_links scrapes restaurant links from multiple pages of a website
Input args: number_of_pages (int): The number of pages to scrape. Defaults to 100.
output args: list: A list of full restaurant links, prefixed with the page number.
"""
def get_restaurants_links(number_of_pages=100):
    restaurants_list = []

    for i in tqdm(range(1, number_of_pages + 1)):
        url = os.path.join(init_page, f'page/{i}')  # Construct the page URL
        response = requests.get(url, headers=headers)  # Fetch the page content

        if response.status_code == 200:  # If the page loads successfully
            soup = BeautifulSoup(response.content, "html.parser")  # Parse the HTML
            restaurants = soup.select('.card__menu.selection-card.js-restaurant__list_item')  # Find restaurant cards

            for restaurant in restaurants:  
                link = restaurant.find('a')
                full_link = os.path.join(main_site, link.get('href')[1:])  # Construct the full link
                restaurants_list.append(f'page{i}>' + full_link)  # Add page prefix and store the link

    return restaurants_list 


"""
download_restaurants_pages Downloads the HTML content of restaurant pages from their URLs and saves them to local directories.
"""
def download_restaurants_pages(restaurants_list):
    for rest in tqdm(restaurants_list): 
        page, url = rest.split('>')  # Separate the page number and URL
        path = os.path.join(pages_base_dir, page)  # Create a directory path for the page

        if not os.path.exists(path):  # If the directory doesn't exist, create it
            os.mkdir(path)

        name = url.split('/')[-1] + '.html'  # Use the last part of the URL as the file name
        response = requests.get(url)  # Fetch the HTML content of the URL

        if response.status_code == 200:  # If the request is successful
            with open(os.path.join(path, name), 'w') as _file:  # Save the content as an HTML file
                _file.write(response.text)



def extract_title(soup):
    # Extract the restaurant's title from the parsed HTML content.
    titles = soup.select('.data-sheet__title')
    return titles[0].text.strip() if titles else None

def extract_address(info):
    # Extract and structure the address, city, postal code, and country from the provided information block.
    address = info[0].text.strip().split(',')
    return {
        'address': address[0].strip(),
        'city': address[1].strip(),
        'postalCode': address[2].strip(),
        'country': address[3].strip()
    }

def extract_details(info):
    # Extract the price range and cuisine type from the provided information block.
    detail = info[1].text.strip().split('·')
    return {
        'priceRange': detail[0].strip(),
        'cuisineType': detail[1].strip()
    }

def extract_description(soup):
    # Extract the restaurant's description from the parsed HTML content.
    description = soup.select('.data-sheet__description')[0]
    return description.text.strip() if description else None

def extract_facilities(soup):
    # Extract a list of facilities/services available at the restaurant.
    facilities = soup.find(class_='restaurant-details__services').find_all('li')
    return [fac.text.strip() for fac in facilities]

def extract_cards(soup):
    # Extract and format accepted credit card names from the provided HTML content.
    try:
        cards = soup.find(class_='list--card').find_all('img')
        return [card.get('data-src').split('/')[-1].split('-')[0].capitalize() for card in cards]
    except:
        return None

def extract_phone_number(soup):
    # Extract the restaurant's phone number from the parsed HTML content.
    information = soup.select('.collapse__block-item')
    return information[0].find('span').text.strip() if information else None

def extract_website(soup):
    # Extract the restaurant's website URL if available.
    links = soup.select('.link.js-dtm-link')
    for link in links:
        if link.get('data-event') == 'CTA_website' and 'www' in link.get('href'):
            return link.get('href').strip()
    return None
