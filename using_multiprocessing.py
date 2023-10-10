import requests
from bs4 import BeautifulSoup
import csv
from multiprocessing import Process
from time import perf_counter

def scrape_product_details(url):
    '''This function gives me Product Details of Flipkart Website
    (like-Title, Mrp, Price, Description, ratings)
    '''
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    product_title = soup.find(class_="B_NuCI")
    product_mrp = soup.find(class_="_30jeq3 _16Jk6d")
    product_price = soup.find(class_="_3I9_wc _2p6lqe")
    product_description = soup.find(class_="_1mXcCf RmoJUa")
    product_rating = soup.find(class_="_2d4LTz")

    return {
        'Product Title': product_title.text if product_title else None,
        'MRP': product_mrp.text if product_mrp else None,
        'Price': product_price.text if product_price else None,
        'Description': product_description.text if product_description else None,
        'Rating': product_rating.text if product_rating else None
    }

t1_start = perf_counter()

def scrape_flipkart_page(url, product_data_list):
    '''This function gives me Flipkart Website Page Data
    (like-Title, Mrp, Price, Description, ratings)
    '''
    product_data = scrape_product_details(url)
    if None not in product_data.values():
        product_data_list.append(product_data)
        # print(product_data)

def scrape_flipkart_search(max_pages=None, search_query='car'):
    '''This function SEARCH the search_query of Flipkart Website,
    Extract all Pages & apply Multiprocessing which reduces the time of execution
    '''
    base_url = f'https://www.flipkart.com/search?q={search_query}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
    }

    
    product_data_list = []
    if not max_pages:
        max_pages = int(BeautifulSoup(requests.get(base_url, headers=headers).text, 'html.parser').find(class_='_2MImiq').select_one('span').text.split()[-1])

    product_links = []
    page = 1
    while page <= max_pages:
        url = f'{base_url}&page={page}'
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        links = soup.find_all(class_='_1fQZEK')
        if links:
            for link in links:
                href = link.get('href')
                if href:
                    product_links.append("https://www.flipkart.com" + href)
            print(f"Extracting data from page {page}")

            procs = []
            for product_link in product_links:
                proc = Process(target=scrape_flipkart_page, args=(product_link, product_data_list))
                proc.start()
                procs.append(proc)

            for proc in procs:
                proc.join()

            product_links.clear()

        else:
            print(f"No products found on page {page}")

        page += 1

    csv_file = f'{search_query}_product_data.csv'
    csv_header = ["Product Title", "MRP", "Price", "Description", "Rating"]

    with open(csv_file, 'a', encoding='utf-8', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_header)
        if csvfile.tell()==0:    
            writer.writeheader()
        for product_data in product_data_list:
            writer.writerow(product_data)
            

    t1_stop = perf_counter()

    print("Total time:", t1_stop-t1_start)

if __name__ == "__main__":
    search_query = 'iphone14'
    max_pages = input('How many pages do you want: ')
    if max_pages:
        scrape_flipkart_search(max_pages=int(max_pages), search_query=search_query)
    else:
        scrape_flipkart_search(search_query=search_query)
