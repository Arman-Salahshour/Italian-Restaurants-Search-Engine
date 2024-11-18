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


