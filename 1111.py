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

def scrape_flipkart_page(url, process_id):
    '''This function gives me Flipkart Website Page Data
    (like-Title, Mrp, Price, Description, ratings)
    '''
    product_data = scrape_product_details(url)
    if None not in product_data.values():
        csv_file = f'product_data_process_{process_id}.csv'
        csv_header = ["Product Title", "MRP", "Price", "Description", "Rating"]
        
        with open(csv_file, 'a', encoding='utf-8', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_header)
            if csvfile.tell() == 0:
                writer.writeheader()
            writer.writerow(product_data)

def scrape_flipkart_search(max_pages=None, search_query='car', num_processes=4):
    '''This function SEARCH the search_query of Flipkart Website,
    Extract all Pages & apply Multiprocessing which reduces the time of execution
    '''
    base_url = f'https://www.flipkart.com/search?q={search_query}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
    }

    processes = []
    for process_id in range(num_processes):
        process = Process(target=scrape_flipkart_page, args=(base_url, process_id))
        process.start()
        processes.append(process)

    for process in processes:
        process.join()

    # Merge CSV files into one
    merged_csv_file = f'{search_query}_product_data.csv'
    csv_header = ["Product Title", "MRP", "Price", "Description", "Rating"]

    with open(merged_csv_file, 'a', encoding='utf-8', newline='') as merged_csv:
        writer = csv.DictWriter(merged_csv, fieldnames=csv_header)
        writer.writeheader()
        
        for process_id in range(num_processes):
            process_csv_file = f'product_data_process_{process_id}.csv'
            with open(process_csv_file, 'r', encoding='utf-8') as process_csv:
                lines = process_csv.readlines()
                if process_id == 0:
                    # Write the header from the first process
                    merged_csv.writelines(lines[0])
                # Write data from each process (skip the header)
                merged_csv.writelines(lines[1:])

    t1_stop = perf_counter()

    print("Total time:", t1_stop - t1_start)

if __name__ == "__main__":
    search_query = 'iphone14'
    max_pages = input('How many pages do you want: ')
    if max_pages:
        scrape_flipkart_search(max_pages=int(max_pages), search_query=search_query)
    else:
        scrape_flipkart_search(search_query=search_query)
