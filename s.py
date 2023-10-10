import requests
from bs4 import BeautifulSoup
import csv

def scrape_product_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Check for the presence of different selectors based on alignment
    product_title = soup.find(class_="B_NuCI")
    if product_title is None:
        product_title = soup.find("h1")

    product_mrp = soup.find(class_="_30jeq3 _16Jk6d")
    if product_mrp is None:
        product_mrp = soup.find(class_="_30jeq3")

    product_price = soup.find(class_=("_3I9_wc _2p6lqe"))
    if product_price is None:
        product_price = soup.find(class_=("_3qQ9m1"))

    product_description = soup.find(class_="_1mXcCf RmoJUa")
    if product_description is None:
        product_description = soup.find(class_="_3la3Fn _1zZOAc")

    product_rating = soup.find(class_="_2d4LTz")

    return {
        'Product Title': product_title.text.strip() if product_title else None,
        'MRP': product_mrp.text.strip() if product_mrp else None,
        'Price': product_price.text.strip() if product_price else None,
        'Description': product_description.text.strip() if product_description else None,
        'Rating': product_rating.text.strip() if product_rating else None
    }

def scrape_flipkart_search(search_query, max_pages=5, allPages=False):
    base_url = f'https://www.flipkart.com/search?q={search_query}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off'
    
    headers = {
        'User-Agent': 'Your-User-Agent-Here'
    }

    product_data_list = []

    if allPages:
        max_pages = BeautifulSoup(requests.get(base_url, headers=headers).text, 'html.parser').find(class_='_2MImiq').select_one('span').text.split()[-1]
        print(max_pages, 111111111111111)
        quit()

    for page in range(1, max_pages + 1):
        url = f'{base_url}&page={page}'
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        product_links = []
        links = soup.find_all(class_='_1fQZEK')
        if links:
            print(11111111111)

            for link in links:
                href = link.get('href')
                product_links.append("https://www.flipkart.com" + href)

            for product_link in product_links:
                product_data = scrape_product_details(product_link)
                if product_data:
                    product_data_list.append(product_data)

            csv_file = f'{search_query}_product_data.csv'
            csv_header = ["Product Title", "MRP", "Price", "Description", "Rating"]

            with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_header)
                writer.writeheader()

                for product_data in product_data_list:
                    writer.writerow(product_data)

            return product_data_list

    return "PRODUCT NOT FOUND"

search_query = 'books'
print(scrape_flipkart_search(search_query, allPages=False))

