import requests
from bs4 import BeautifulSoup
import csv

def scrape_product_details(product_link):
    # Add your scraping logic for individual product pages here
    # You can create a function to extract details from a single product page
    pass

def scrape_flipkart_search(search_query, max_pages=5):
    base_url = f'https://www.flipkart.com/search?q={search_query}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
    }

    product_data_list = []

    for page in range(1, max_pages + 1):
        url = f'{base_url}&page={page}'
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        product_links = []
        links = soup.find_all(class_='_1fQZEK')

        for link in links:
            href = link.get('href')
            product_links.append("https://www.flipkart.com" + href)

        for product_link in product_links:
            product_data = scrape_product_details(product_link)
            if product_data:
                product_data_list.append(product_data)

    # Save the data to a CSV file
    csv_file = f'{search_query}_product_data.csv'
    csv_header = ["PRODUCT TITLE", "MRP", "PRICE", "DESCRIPTION", "RATING"]

    with open(csv_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_header)
        writer.writeheader()

        for product_data in product_data_list:
            writer.writerow(product_data)

    return product_data_list

# Example usage:
search_query = "mobile"
max_pages = 5  # Set the maximum number of pages to scrape
product_data = scrape_flipkart_search(search_query, max_pages)
print(product_data)
