import requests
import pandas as pd
from bs4 import BeautifulSoup
import json

headers = {
    'cookie': "",
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    'Accept-Language': "en-GB,en-US;q=0.9,en;q=0.8",
    'Cache-Control': "max-age=0",
    'Connection': "keep-alive",
    'Cookie': "",
    'Referer': "https://www.emag.hu/",
    'Sec-Fetch-Dest': "document",
    'Sec-Fetch-Mode': "navigate",
    'Sec-Fetch-Site': "same-origin",
    'Sec-Fetch-User': "?1",
    'Upgrade-Insecure-Requests': "1",
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
    'sec-ch-ua': "^\^Chromium^^;v=^\^104^^, ^\^"
}

products = []

for page in range(0, 30):
    url = f'https://www.emag.hu/mobiltelefonok/brand/apple/raktaron/vendor/emag/p{page}/c?ref=lst_leftbar_6409_stock'
    response = requests.get(url, headers)
    doc = BeautifulSoup(response.text, 'html.parser')
    container = doc.find(class_='page-container')
    phones = container.find_all(class_=['card-item', 'card-standard'])

    for phone in phones:
        toolbox = phone.find(class_='add-to-favorites')['data-product']
        product = json.loads(toolbox)

        if 'Apple' in product['product_name']:
            rating = phone.find(class_='card-v2-rating')
            rating_number = rating.find(class_='average-rating')
            if rating_number is not None:
                product['rating'] = rating.string
            number_of_ratings = rating.find(class_='hidden-xs')
            if number_of_ratings is not None:
                product['number_of_ratings'] = number_of_ratings.string
            product['link'] = phone.find(class_='js-product-url')['href']
            products.append(product)

df = pd.DataFrame(products)

df.to_csv('results.csv')
