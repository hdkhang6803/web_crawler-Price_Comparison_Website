from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import re
import multi_thread as _thread
import threading

class product_selector:
    def __init__(self, card, link, title, price, image):
        self.card = card
        self.link = link
        self.title = title
        self.price = price
        self.image = image

categories = [
    {'name': 'Laptop', 
     'links' : ['https://cellphones.com.vn/laptop.html']},
    {'name': 'Desktop', 
     'links' : ['https://cellphones.com.vn/may-tinh-de-ban.html']},
    {'name': 'LinhKien',
     'links': ['https://cellphones.com.vn/linh-kien.html']},
    {'name': 'PhuKien', 
     'links' : ['https://cellphones.com.vn/phu-kien/may-tinh-laptop.html',
                'https://cellphones.com.vn/thiet-bi-am-thanh.html',
                'https://cellphones.com.vn/man-hinh.html']}
]

def show_more(driver, show_more_selector, remove_ad_selector, close_reminder_selector):
    while True:
        try:
            show_more_button = driver.find_element(By.CSS_SELECTOR, show_more_selector)
            show_more_button.click()
            sleep(0.25)
        except:
            try:
                sleep(0.75)
                show_more_button = driver.find_element(By.CSS_SELECTOR, show_more_selector)
                show_more_button.click()
                sleep(0.25)
            except:
                try:
                    sleep(10)
                    close_ads_btn = driver.find_element(By.CSS_SELECTOR, remove_ad_selector) 
                    close_ads_btn.click()
                    sleep(0.5)
                except:
                    try:
                        close_reminder_btn = driver.find_element(By.CSS_SELECTOR, close_reminder_selector)
                        close_reminder_btn.click()
                        sleep(0.5)
                    except:
                        break

def extractProductInfo(prod_html, prod_selector):
    title = prod_html.select_one(prod_selector.title).get_text().strip()
    price = prod_html.select_one(prod_selector.price).get_text().strip()
    link = prod_html.select_one(prod_selector.link).get('href')
    img = prod_html.select_one(prod_selector.image).get('src')

    if price != None:
        price = re.sub('\D', '', price)
        if (price != ''):
            price = int(price)
            return [title, price, link, img]
    return []

def get_products_in_category_cphones(database, category):
    try:
        driver = webdriver.Chrome()
        product_list = []
        common_prod_selector = product_selector(
            'div.product-info-container.product-item .product-info',
            '.product__link', 
            'div.product__name h3',
            '.box-info__box-price p.product__price--show', 
            '.product__image img')

        for link in category['links']:
            driver.get(link)
            show_more(driver, 
                '.button.btn-show-more', # show_more_selector
                '.cancel-button-top', # remove_ad_selector
                '.ins-web-opt-in-reminder-close-button') # close_reminder_selector
            html_text = driver.page_source
            html_content = BeautifulSoup(html_text, 'lxml')
            
            products = html_content.select(common_prod_selector.card)
            for product in products:
                pro_info = extractProductInfo(product, common_prod_selector)
                product_list.append(pro_info)
            database.update_with_data(product_list, category['name'])
            print('Scraped', link, '-', len(product_list), category['name'])
        print('######################################' + ' CELLPHONES ' + ' ' + category['name'] + ' FINISHED' + '-----' + str(len(product_list)))
        driver.quit()
        _thread.threads_status_dict[threading.current_thread()] = [0, get_products_in_category_cphones, category]
    except Exception as e:
        _thread.threads_status_dict[threading.current_thread()] = [-1, get_products_in_category_cphones, category]
        print(e)
    # return product_list

def scrape_all(database, categories_id):
    for cat in categories:
        print('---- Started crawling', cat['name'], '----')
        product_list = get_products_in_category_cphones(cat)
        print('Finished crawling', cat['name'], '-', 
              len(product_list), 'products scraped.')
        # database.update_with_data(product_list, cat['name'])
        print('Updated products on', cat['name'])
        # database.remove_duplicate(categories_id[cat['name']])
        print('Removed duplicates on', cat['name'], '\n')

def get_list_cellphones(database):
    return(_thread.run_multi_thread_cate(database, categories, get_products_in_category_cphones))






    
