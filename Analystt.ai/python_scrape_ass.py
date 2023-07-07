from bs4 import BeautifulSoup
from selenium import webdriver
import re
import csv

options = webdriver.ChromeOptions()
options.add_argument("--headless")  
driver = webdriver.Chrome(options=options)

num_pages = 20

product_urls = []
product_names = []
product_prices = []
product_ratings = []
product_reviews = []
descriptions = []
product_descriptions = []
product_asins = []
product_manufactures = []
for page in range(1,num_pages+1):
    url = f"https://www.amazon.in/s?k=bags&page={str(page)}&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_{str(page)}"
    driver.get(url)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    product_containers = soup.find_all('div', {'data-component-type': 's-search-result'})
    for container in product_containers:
        product_url = container.find('a', {'class': 'a-link-normal s-no-outline'}).get('href')
        product_urls.append('https://www.amazon.in/' + product_url)
        if i<=250:
            driver.get('https://www.amazon.in/' + product_url)
            product_page_source = driver.page_source
            product_soup = BeautifulSoup(product_page_source, 'html.parser')
            product_asin = product_soup.select_one('div[id="detailBulletsWrapper_feature_div"] li:-soup-contains("ASIN")') 
            product_asin1 = product_soup.select_one('th:-soup-contains("ASIN") + td')
            product_manufacture = product_soup.select_one('div[id="detailBulletsWrapper_feature_div"] li:-soup-contains("Manufacturer"):not(:-soup-contains("Discontinued"))')
            product_manufacture1=product_soup.select_one('th:-soup-contains("Manufacturer") + td')
            product_description = product_soup.select('div.aplus-module-content, div.aplus-module-wrapper.apm-fixed-width,div#productDescription,div.launchpad-text-left-justify')
            des_text = product_soup.find('div', id='feature-bullets')
            if product_asin:
                product_asin = product_asin.find('span').text.strip()
                pd1 = product_asin.split(':')[-1].strip()
                pm = re.findall(r'([^\u200e]?[A-Za-z0-9]+)', pd1)
                product_asin = ' '.join(pm)
                product_asins.append(product_asin)
            elif product_asin1:
                product_asin1 = product_asin1.get_text(strip=True)
                pd1 = product_asin1.split(':')[-1].strip()
                pa = re.findall(r'([^\u200e]?[A-Za-z0-9]+)', pd1)
                product_asin1 = ' '.join(pa)
                product_asins.append(product_asin1)
            if product_manufacture:
                product_manufacture = product_manufacture.find('span').text.strip()
                pd1 = product_manufacture.split(':')[-1].strip()
                pm = re.findall(r'([^\u200e]?[A-Za-z0-9]+)', pd1)
                product_manufacture = ' '.join(pm)
                product_manufactures.append(product_manufacture)
            elif product_manufacture1:
                product_manufacture1 = product_manufacture1.get_text(strip=True)
                pm = re.findall(r'([^\u200e]?[A-Za-z0-9]+)', product_manufacture1)
                product_manufacture1 = ' '.join(pm)
                product_manufactures.append(product_manufacture1)
            if product_description:
                pd = ""
                for div in product_description:
                    text = div.get_text(strip=True)
                    pd = pd + text
            product_descriptions.append(pd)
            if des_text:
                des_text = des_text.get_text(strip=True)
                descriptions.append(des_text)
        i += 1
        product_name = container.find('span', {'class': 'a-size-medium a-color-base a-text-normal'})
        product_name = product_name.text.strip() if product_name else ' '
        product_names.append(product_name)

        price_element = container.find('span', {'class': 'a-offscreen'})
        product_price = price_element.text.strip() if price_element else ' '
        product_prices.append(product_price)

        rating = container.find('span', {'class': 'a-icon-alt'})
        if rating:
            product_rating = rating.text.split()[0]
        else:
            product_rating = 'Not Rated'
        product_ratings.append(product_rating)

        reviews = container.find('span', {'class': 'a-size-base'})
        if reviews:
            product_review = reviews.text.strip()
        else:
            product_review = '0'
        product_reviews.append(product_review)

driver.quit()
filename = "product_data.csv"
with open(filename, 'a',newline='',encoding='utf-8',errors='ignore') as file:
    writer = csv.writer(file)
    if file.tell() == 0:
        header = ['product_urls', 'product_names', 'product_prices', 'product_ratings', 'product_reviews', 'descriptions', 'product_descriptions', 'product_asins', 'product_manufactures']
        writer.writerow(header)
    for i in range(len(product_urls)):
        clean_pro_description = product_descriptions[i].replace('\n', '').strip()
        if i<220:
            row = product_urls[i],product_names[i],product_prices[i],product_ratings[i],product_reviews[i],clean_description,clean_pro_description,product_asins[i],product_manufactures[i]
            writer.writerow(row)
        else:
            row = product_urls[i],product_names[i],product_prices[i],product_ratings[i],product_reviews[i]
            writer.writerow(row)