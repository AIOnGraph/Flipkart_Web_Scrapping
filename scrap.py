import requests
from bs4 import BeautifulSoup

def scrape_product_details(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
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

url = "https://www.flipkart.com/realme-c55-sunshower-64-gb/p/itm054283d14c56e?id=LSTMOBGNBYJCXN6WRB3NDXTAJ&marketplace=FLIPKART&q=15000+mobile&store=tyy%2F4io&srno=s_1_1&otracker=search&otracker1=search&fm=Search&iid=en_Yk-JSqlkgS7dt1XNCkoRq4W54gKbpGDBGfWZW0wvzqv3SwXnM2XsyzQK4rJDsBTUH0_zxzz8w7OBdFcwCV_-MQ%3D%3D&ppt=sp&ppn=sp&ssid=qolugpc82o0000001696313052151&qH=7268607c477b8993"

product_data = scrape_product_details(url)
print(product_data['Product Title'])
if product_data['Product Title']:
    print(product_data)
else:
    print("Product details not found.")
