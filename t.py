import requests
from bs4 import BeautifulSoup
import csv

def scrape_product_details(url):


    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    product_title = soup.find(class_="B_NuCI")
    product_mrp = soup.find(class_="_30jeq3 _16Jk6d")
    product_price = soup.find(class_=("_3I9_wc _2p6lqe"))
    product_description = soup.find(class_="_1mXcCf RmoJUa")
    product_rating = soup.find(class_="_2d4LTz")

    return {
        'Product Title': product_title.text if product_title else None,
        'MRP': product_mrp.text if product_mrp else None,
        'Price': product_price.text if product_price else None,
        'Description': product_description.text if product_description else None,
        'Rating': product_rating.text if product_rating else None
    }



def scrape_flipkart_search(search_query, max_pages=5):
    base_url = f'https://www.flipkart.com/search?q={search_query}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
    }

    product_data_list = []
    print(product_data_list)

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
    print(product_data_list)

  
    csv_file = f'{search_query}_product_data.csv'
    csv_header = ["PRODUCT TITLE", "MRP", "PRICE", "DESCRIPTION", "RATING"]

    with open(csv_file, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_header)
        writer.writeheader()

        for product_data in product_data_list:
            writer.writerow(product_data)

    return product_data_list


search_query = "mobile"
max_pages = 5
url = "https://www.flipkart.com/infinix-note-30-5g-sunset-gold-128-gb/p/itm12c179f0a6281?pid=MOBGQ9HPVTGHZCQG&lid=LSTMOBGQ9HPVTGHZCQGQFEYKE&marketplace=FLIPKART&q=15000+mobile&store=tyy%2F4io&srno=s_1_1&otracker=search&otracker1=search&fm=organic&iid=d2fdf3e4-4743-4550-b9bd-916c92724e16.MOBGQ9HPVTGHZCQG.SEARCH&ppt=hp&ppn=homepage&ssid=6aulwjvksg0000001696339720232&qH=7268607c477b8993"

product_data = scrape_product_details(url)
# print(product_data['Product Title'])
print(product_data)
# if product_data['Product Title']:
#     print(product_data)
# else:
#     print("Product details not found.")
product_data = scrape_flipkart_search(search_query, max_pages)
print(product_data)
