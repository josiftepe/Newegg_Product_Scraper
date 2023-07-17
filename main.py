import random
import time
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import csv
csv_file = 'product_data_table.csv'
scraped_prods = 0
with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    output = csv.writer(file)
    output.writerow(['Product title', 'Product description', 'Product final pricing', 'Product rating', 'Product seller name', 'Product image URL'])

    for website_idx in range(1, 7):
        url = f"https://www.newegg.com/p/pl?N=100006519&PageSize=96&page={website_idx}"
        driver = webdriver.Chrome()
        driver.get(url)
        time.sleep(random.randint(1, 3))
        imgs = driver.find_elements(By.CLASS_NAME, 'item-img')

        for i in range(0, len(imgs)):
            time.sleep(random.randint(3, 9))
            img_url = imgs[i].find_element(By.TAG_NAME, "img").get_attribute("src")
            driver.execute_script("window.open(arguments[0]);", imgs[i].get_attribute("href"))
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(random.randint(8, 16))
            title = ""
            try:
                title = driver.find_element(By.XPATH, '//h1[@class="product-title"]').text
            except NoSuchElementException:
                title = "N/A"
            rating = ""
            try:
                rating = driver.find_element(By.CLASS_NAME, 'product-rating').find_element(By.TAG_NAME, 'i').get_attribute(
                    "title").split(" eggs")[0]
            except NoSuchElementException:
                rating = "N/A"
            price = ""
            try:
                price = driver.find_element(By.XPATH, '//li[@class="price-current"]').text
            except NoSuchElementException:
                price = "N/A"
            seller = ''
            try:
                seller_data = driver.find_elements(By.XPATH, '//div[@class="product-seller no-border-bottom"]')
                for tmp in seller_data:
                    seller_text = tmp.text
                    idx = seller_text.find("by:")
                    arr = seller_text.split('\n')
                    seller = arr[0]
            except NoSuchElementException:
                seller = 'Newegg'
            details = ""
            try:
                details = driver.find_element(By.XPATH, '//div[@class="product-bullets"]').text
            except NoSuchElementException:
                details = "N/A"
            img = ""
            try:
                img = driver.find_element(By.TAG_NAME, 'img').get_attribute("src")
            except NoSuchElementException:
                img = "N/A"
            if title != "N/A":
                output.writerow([title, details, price, rating, seller, img_url])
                scraped_prods += 1
                print(scraped_prods)
            if scraped_prods == 500:
                break

            driver.close()
            driver.switch_to.window(driver.window_handles[0])

        driver.quit()



