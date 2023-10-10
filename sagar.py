from bs4 import BeautifulSoup
import requests
import csv
import time
import multiprocessing

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Referer': 'https://www.example.com/',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'max-age=0',
}

def isObjectEmpty(productdetailname):
    if productdetailname:
        return productdetailname.text
    else:
        return None

def scrapProductDetails(url, lock, manager_list, processed_urls):
    dict1 = {}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    fullcontainer = soup.find(class_="a-container")
    title = fullcontainer.find(id="productTitle")

    if title:
        print(f"Title of this Product is ---> {title.text}")
        imagecontainer = fullcontainer.find(id="imgTagWrapperId")
        images = imagecontainer.find_all("img")
        image = images[0]['src']
        price = fullcontainer.find(class_="a-price-whole")
        price = isObjectEmpty(price)
        print(f"Price of this product is -----> {price}")
        mrp = fullcontainer.find(class_="a-price a-text-price")
        mrp1 = isObjectEmpty(mrp)
        finalmrp = None
        if mrp1:
            finalmrp = mrp.find(class_="a-offscreen")
            finalmrp = isObjectEmpty(finalmrp)
        print(finalmrp)
        ratingcontainer = fullcontainer.find(id="averageCustomerReviews")
        ratingcontainer1 = isObjectEmpty(ratingcontainer)
        rating = None
        if ratingcontainer1:
            rating = ratingcontainer.find(class_='a-size-base a-color-base')
            rating = isObjectEmpty(rating)
        print(f"Rating of this product out of 5 is ---> {rating}")

        print("-------------------DESCRIPTIONS--------------------- ")
        listofdes = fullcontainer.find(class_="a-unordered-list a-vertical a-spacing-mini")
        listofdes = isObjectEmpty(listofdes)
        dict1["PRODUCT TITLE"] = title.text
        dict1["Images"] = image
        dict1["MRP"] = finalmrp
        dict1["PRICE"] = price
        dict1["RATING"] = rating
        dict1["DESCRIPTION"] = listofdes

        with lock:
            if url not in processed_urls:  # Check for duplicates
                manager_list.append(dict1)
                processed_urls.add(url)  # Add to processed URLs
                if len(manager_list) >= 20:
                    writeInFile(manager_list)
                    manager_list.clear()

def writeInFile(manager_list):
    with open("webscrap7.csv", mode="a", encoding="utf-8") as file:
        fieldnames = manager_list[0].keys()
        productfile = csv.DictWriter(file, fieldnames=fieldnames)
        for item in manager_list:
            productfile.writerow(item)

def scrape_product(url, lock, manager_list, processed_urls):
    scrapProductDetails(url, lock, manager_list, processed_urls)

def getAllPagesHref(keyword, lock, manager_list):
    listOfEveryPageUrls = []
    url = f"https://www.amazon.in/s?k={keyword}&page=1"
    res = requests.get(url, headers=headers)
    time.sleep(1)
    soup1 = BeautifulSoup(res.text, "html.parser")
    hrefsclass = soup1.find_all(class_="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal")
    if hrefsclass:
        listOfEveryPageUrls.append(url)
        maxPages = int(soup1.find(class_="s-pagination-item s-pagination-disabled").text)
        print(maxPages)
        for i in range(2, maxPages + 1):
            url = f"https://www.amazon.in/s?k={keyword}&page={i}"
            listOfEveryPageUrls.append(url)

        print(listOfEveryPageUrls)
        fetchEveryPageProductHref(listOfEveryPageUrls, lock, manager_list)
    else:
        print(f"No results for {keyword} try checking your spelling or use more general terms")

def fetchEveryPageProductHref(listOfEveryPageUrls, lock, manager_list):
    listOfProductLinks = []
    index = 0
    for i in range(0, len(listOfEveryPageUrls)):
        if i == 3:
            break
        print("hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh,", i)
        onePageUrl = listOfEveryPageUrls[i]
        res = requests.get(onePageUrl, headers=headers)
        time.sleep(2)
        soup1 = BeautifulSoup(res.text, "html.parser")
        hrefsclasses = soup1.find_all(
            class_="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal")
        print(hrefsclasses)
        for hrefclass in hrefsclasses:
            link = hrefclass.get("href")
            prefix = "https://www.amazon.in"
            url = f"{prefix}{link}"
            listOfProductLinks.append(url)
            print(len(listOfProductLinks))
            if len(listOfProductLinks) >= index + 20:
                doScrapingWithMultiprocessing(listOfProductLinks[index:index + 20], lock, manager_list)
                index = index + 20

def doScrapingWithMultiprocessing(listOfProductLinks, lock, manager_list):
    processes = []

    # Create a set to keep track of processed URLs to avoid duplicates
    processed_urls = set()

    for url in listOfProductLinks:
        process = multiprocessing.Process(target=scrape_product, args=(url, lock, manager_list, processed_urls))
        process.start()
        processes.append(process)

    for process in processes:
        process.join()

def enterKeyword(lock, manager_list):
    keyword = input("SEARCH HERE----------> ")
    start = time.perf_counter()
    getAllPagesHref(keyword,lock, manager_list)
    elapsed = time.perf_counter() - start
    print(elapsed, 566666666666666666666666666666666666666666666666666666666666666)

if __name__ == "__main__":
    manager = multiprocessing.Manager()
    manager_list = manager.list()
    lock = multiprocessing.Lock()
    enterKeyword(lock, manager_list)
