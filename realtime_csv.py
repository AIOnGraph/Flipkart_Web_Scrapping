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

    product_data = {
        'Product Title': product_title.text if product_title else None,
        'MRP': product_mrp.text if product_mrp else None,
        'Price': product_price.text if product_price else None,
        'Description': product_description.text if product_description else None,
        'Rating': product_rating.text if product_rating else None
    }


    save_to_csv([product_data])

    return product_data

def save_to_csv(data_list):
    csv_file = 'product_data.csv'
    csv_header = ["Product Title", "MRP", "Price", "Description", "Rating"]

    with open(csv_file, 'a', newline='', encoding='utf-8') as csvfile: 
        writer = csv.DictWriter(csvfile, fieldnames=csv_header)
        
        for product_data in data_list:
            writer.writerow(product_data)

def scrape_flipkart_search(search_query, max_pages=5, allPages=False):
    base_url = f'https://www.flipkart.com/search?q={search_query}&as=on&as-show=on&otracker=AS_Query_OrganicAutoSuggest_6_3_na_na_ps&otracker1=AS_Query_OrganicAutoSuggest_6_3_na_na_ps&as-pos=6&as-type=RECENT&suggestionId=air+purifier&requestId=8c304015-494f-4cb9-8d3e-906ff79a37a3&as-searchtext=airpods%20pro'

    headers = {
        'User-Agent': 'Your-User-Agent-Here'
    }

    product_data_list = []

    if allPages:
        max_pages = BeautifulSoup(requests.get(base_url, headers=headers).text, 'html.parser').find(class_='_2MImiq').select_one('span').text.split()[-1]
        # print(max_pages)
        quit()

    for page in range(1, max_pages + 1):
        url = f'{base_url}&page={page}'
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        product_links = []
        links = soup.find_all(class_='_1fQZEK')
        if links:
            

            for link in links:
                href = link.get('href')
                product_links.append("https://www.flipkart.com" + href)

            for product_link in product_links:
                product_data = scrape_product_details(product_link)
                if product_data:
                    product_data_list.append(product_data)

    return product_data_list

search_query = 'air purifier'
print(scrape_flipkart_search(search_query, allPages=True))
print(scrape_flipkart_search(search_query,max_pages=5,allPages=False))










