import requests
from scrap import scrape_product_details
from bs4 import BeautifulSoup
# import csv
search_query = "mobile"
url=f'https://www.flipkart.com/search?q={search_query}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

res=requests.get(url,headers=headers)

soup= BeautifulSoup(res.text,'html.parser')
product_links=[]
links=soup.find_all(class_='_1fQZEK')

for link in links:
    href=link.get('href')
    
    product_links.append("https://www.flipkart.com" +href)
# print(product_links)

product_data_list=[]
product_data = scrape_product_details('https://www.flipkart.com/search?q=15000%20mobile&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off')
print(product_data)

# for product_link in product_links:
#     product_data=scrape_product_details(produnct_link)
#     if product_data['Product Title']:
#         product_data_list.append(product_data)

# csv_file='product_data_csv'
# csv_header=["PRODUCT TITLE","MRP","PRICE","DESCRIPTION","RATING"]

# with open(csv_file,'w',newline='')as csvfile:
#     writer=csv.DictWriter(csvfile,filenames=csv_header)

# for product_data in product_data_list:
#     writer.writerow(product_data)
with open("data.txt","w") as f:
    f.write(str(soup))
