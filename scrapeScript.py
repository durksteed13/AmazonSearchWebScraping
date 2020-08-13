from bs4 import BeautifulSoup
import requests
import json

# take input, generate Amazon search url
searchItem = input("Enter Amazon search: ")
searchItem = searchItem.replace(' ', '+')
searchURL = "https://www.amazon.com/s?k=" + searchItem

# gather html from Amazon search results
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding": "gzip, deflate", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT": "1", "Connection": "close", "Upgrade-Insecure-Requests": "1"}
response = requests.get(searchURL, headers=headers)
content = response.content
soup = BeautifulSoup(content)

# parse through html, find product info (brand, name, price, rating, image)
for d in soup.findAll('div', attrs={'class': 's-expand-height s-include-content-margin s-latency-cf-section'}):
    brandInfo = d.find('h5', attrs={'class': 's-line-clamp-1'})
    productInfo = d.find('span', attrs={'class': 'a-size-base-plus a-color-base a-text-normal'})
    p = d.find('span', attrs={'class': 'a-price'})
    priceInfo = p.find('span', attrs={'class': 'a-offscreen'})
    ratingInfo = d.find('span', attrs={'class': 'a-icon-alt'})
    imageInfo = d.find('div', attrs={'class': 'a-section aok-relative s-image-tall-aspect'})
    if brandInfo is not None:
        brand = brandInfo.text
        brand = brand.replace('\n', '')
    if productInfo is not None:
        name = productInfo.text
    if priceInfo is not None:
        price = priceInfo.text
    if ratingInfo is not None:
        rating = ratingInfo.text
    if imageInfo is not None:
        imageFound = imageInfo.find('img')
        image = "none"
        if imageFound is not None:
            image = imageFound['src']

    # generate json
    item = {
        "brand": brand,
        "name": name,
        "price": price,
        "rating": rating,
        "image": image
    }

    itemJson = json.dumps(item)
    print(itemJson)
