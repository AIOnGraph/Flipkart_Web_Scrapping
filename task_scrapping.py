import requests
from bs4 import BeautifulSoup
import pandas as pd
def scrapping():
    url = "https://www.flipkart.com/realme-c55-sunshower-64-gb/p/itm054283d14c56e?id=LSTMOBGNBYJCXN6WRB3NDXTAJ&marketplace=FLIPKART&q=15000+mobile&store=tyy%2F4io&srno=s_1_1&otracker=search&otracker1=search&fm=Search&iid=en_Yk-JSqlkgS7dt1XNCkoRq4W54gKbpGDBGfWZW0wvzqv3SwXnM2XsyzQK4rJDsBTUH0_zxzz8w7OBdFcwCV_-MQ%3D%3D&ppt=sp&ppn=sp&ssid=qolugpc82o0000001696313052151&qH=7268607c477b8993"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    res=requests.get(url,headers=headers)


# print(response)
    soup= BeautifulSoup(res.text,'html.parser')
# print(soup)

# product_title=[]
# product_images=[]
# mrps=[]
# prices=[]
# description=[]
# ratings=[]

# for product in soup.find_all('div',class_="_2kHMtA"):
    with open("data.txt","w") as f:
        f.write(str(soup))
# print(soup)
# product=soup.find('div',class_="_2kHMtA")
    product_title=soup.find(class_="B_NuCI")
    # print(product_title.text)


# product_images=soup.find('img'['src'])
# # print(product_images)
# # product_images = soup.find('img')
# print(product_images)

# # Extract and print the image URLs
# for image in product_images:
#     img_url = image.get('src')
# print(img_url)
    # if img_url:
    #     # Print the image URL
    #     print(img_url)


    product_mrp=soup.find(class_="_30jeq3 _16Jk6d")
    print(product_mrp.text)
    product_price=soup.find(class_=("_3I9_wc _2p6lqe"))
# print(product_price.text)
    product_description=soup.find(class_="_1mXcCf RmoJUa")
# print(product_description.text)
    product_rating=soup.find(class_="_2d4LTz")
# print(product_rating.text)
    return:





# print(product_title.title)
# product_images=soup.find_all('div',class_="_396cs4")
# print(product_images)

    # product_images.append(product.find('img'['src']))
    # mrps.append(product.find('div',class_="_30jeq3 _1_WHN1").text)
    # prices.append(product.find('div',class_="_3I9_wc _27UcVY".text))
# print(product)
# info = {
#     'Product MRP': [product_mrp.text],
#     'Product Price': [product_price.text],
#     'Product Description': [product_description.text],
#     'Product Rating': [product_rating.text]
# }

# df = pd.DataFrame(info)
# print(df)

