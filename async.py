import asyncio
import csv
from bs4 import BeautifulSoup
import aiohttp
import time

async def extract_product_links(url, headers):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            soup = BeautifulSoup(await response.text(), 'html.parser')
            elements = soup.find_all(class_='_2kHMtA')

            product_links = []
            for element in elements:
                link = element.find('a', class_='_1fQZEK')
                if link:
                    href = link.get('href')
                    product_links.append("https://www.flipkart.com" + href)

            return product_links

async def scrape_product_details(url, headers, result_list):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            soup = BeautifulSoup(await response.text(), 'html.parser')
            product_title = soup.find(class_="B_NuCI").text
            product_image = soup.find('img', class_='_396cs4').get('src')
            
            product_mrp = soup.find(class_="_30jeq3 _16Jk6d")
            product_mrp = product_mrp.text if product_mrp else "N/A"
            
            product_price = soup.find(class_="_3I9_wc _2p6lqe")
            product_price = product_price.text if product_price else "N/A"

            product_description = soup.find(class_="_3zQntF")
            if product_description:
                product_description = product_description.text
            else:
                product_description = "N/A"

            product_rating = soup.find(class_="_2d4LTz")
            if product_rating:
                product_rating = product_rating.text
            else:
                product_rating = "N/A"

            product_info = {
                'Product Title': product_title,
                'Image': product_image,
                'MRP': product_mrp,
                'Price': product_price,
                'Description': product_description,
                'Rating': product_rating
            }

            result_list.append(product_info)

async def scrape_flipkart_search(search_query, max_pages=None):
    base_url = f'https://www.flipkart.com/search?q={search_query}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    }

    start_time = time.perf_counter() 

    product_links = []
    page = 1

    while True:
        url = f'{base_url}&page={page}'
        current_product_links = await extract_product_links(url, headers)

        if not current_product_links:
            break

        product_links.extend(current_product_links)

        if max_pages and page >= max_pages:
            break

        page += 1

    product_data_list = []

    async def scrape_product_data(product_links, result_list):
        tasks = []
        for product_link in product_links:
            task = scrape_product_details(product_link, headers, result_list)
            tasks.append(task)
        await asyncio.gather(*tasks)

    await scrape_product_data(product_links, product_data_list)

    end_time = time.perf_counter()
    total_time = end_time - start_time
    print(f'Total time taken for scraping: {total_time} seconds')


    return product_data_list

if __name__ == "__main__":
    search_query = input('Enter your search query (e.g., "iPhone 14"): ')
    max_pages = input('How many pages do you want to scrape (leave empty for all pages)? ')

    if max_pages:
        max_pages = int(max_pages)
    else:
        max_pages = None

    loop = asyncio.get_event_loop()
    product_data_list = loop.run_until_complete(scrape_flipkart_search(search_query=search_query, max_pages=max_pages))

    csv_file = f'{search_query}_product_data.csv'
    csv_header = ["Product Title", "MRP", "Price", "Description", "Rating", "Image"]

    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_header)
        writer.writeheader()

        for product_data in product_data_list:
            writer.writerow(product_data)

    print(f'Total number of product links: {len(product_data_list)}')
