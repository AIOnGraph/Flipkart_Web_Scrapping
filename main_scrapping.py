import requests
from bs4 import BeautifulSoup
import csv
from time import perf_counter

def scrape_product_details(url):
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
def scrape_flipkart_search(max_pages=None,search_query='car'):
    base_url = f'https://www.flipkart.com/search?q={search_query}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off'
    # base_url = f'https://www.flipkart.com/search?q={search_query}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off'
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
    }

    product_data_list = []
    if not max_pages:
        max_pages=int(BeautifulSoup(requests.get(base_url, headers=headers).text, 'html.parser').find(class_='_2MImiq').select_one('span').text.split()[-1])
    # if allPages:
    #     max_pages=BeautifulSoup(requests.get(base_url, headers=headers).text, 'html.parser').find(class_='_2MImiq').select_one('span').text.split()[-1]
    #     print(max_pages,111111111111111)
    #     quit()

    product_links = []
    productNo=0
    page=1
    while True:
    # for page in range(1, max_pages + 1):
        url = f'{base_url}&page={page}'
        # print(url,'URL-------------------')
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        links = soup.find_all(class_='_1fQZEK')
        if links:
            # print(11111111111)

            for link in links:
                href = link.get('href')
                if href:
                    product_links.append("https://www.flipkart.com" + href)
            # print(len(product_links))

            for product_link in product_links:
                product_data = scrape_product_details(product_link)
                if None in product_data.values():
                    continue
                product_data_list.append(product_data)
                productNo+=1
                print(productNo)
                # print(len(product_data_list))


            csv_file = f'{search_query}_product_data.csv'
            csv_header = ["Product Title", "MRP", "Price", "Description", "Rating"]

            with open(csv_file, 'a', encoding='utf-8') as csvfile: 
                writer = csv.DictWriter(csvfile, fieldnames=csv_header)
                if page==1:
                    writer.writeheader()

                for product_data in product_data_list:
                    writer.writerow(product_data)

        else:
            print(f"PRODUCT NOT FOUND ON PAGE NO {page}")
        # return product_data_list
        product_links.clear()
        product_data_list.clear()

        next_button=soup.find(class_='_1LKTO3')
        if not next_button or (max_pages and page>= max_pages):
            break

        page+=1
    # else:
    #     print("no page found")
    #     break
        t1_stop = perf_counter()
 
    print("Total time:",t1_start-t1_stop) 


search_query = '1phone 14'
max_pages=input('How much page do you want')
if max_pages:

    print(scrape_flipkart_search(max_pages=int(max_pages),search_query=search_query))
else:
    print(scrape_flipkart_search(search_query=search_query))

# print(len(scrape_flipkart_search(search_query,max_pages)))
