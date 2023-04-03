from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import re

def show_more(driver, show_more_class, ad_remove_class):
    while True:
        try:
            show_more_button = driver.find_element(By.CLASS_NAME, show_more_class)
            show_more_button.click()
            sleep(0.5)
        except:
            try:
                close_ads_btn = driver.find_element(By.CLASS_NAME, ad_remove_class)
                close_ads_btn.click()
                sleep(0.5)
            except:
                break 

def extractProductInfo(product_html, link_class, title_class, price_class, img_class):
    title = product_html.select_one(title_class).get_text().strip()
    price = product_html.select_one(price_class).get_text().strip()
    link = product_html.select_one(link_class).get('href')
    img = product_html.select_one(img_class).get('src')

    if price != None:
        price = re.sub('\D', '', price)
        if (price != ''):
            price = int(price)
            return [title, price, link, img]
    return []
        
def get_products_in_category(category):
    driver = webdriver.Chrome()
    domain = 'https://cellphones.com.vn/'
    subcats = parse_category(category)
    category_dictionary = []

    for subcat in subcats:
        driver.get(domain + subcat + '.html')
        sleep(10)
        show_more(driver, 'btn-show-more', 'cancel-button-top')
        html_text = driver.page_source
        html_content = BeautifulSoup(html_text, 'html.parser')
        products = html_content.select('div.product-info-container.product-item .product-info')

        for product in products:
            pro_info = extractProductInfo(product, 
                '.product__link', 'div.product__name h3', 
                '.box-info__box-price p.product__price--show', '.product__image img')
            category_dictionary.append(pro_info)
    driver.quit()
    return category_dictionary

def parse_category(category):
    if (category == 'Laptop'):
        return ['/laptop']
    if (category == 'Desktop'):
        return [ 
            '/may-tinh-de-ban/lap-rap',
            '/may-tinh-de-ban/all-in-one',
            '/may-tinh-de-ban/dong-bo'
        ]
    if (parse_category == 'LinhKien'):
        return ['/linh-kien']
    if (parse_category == 'PhuKien'):
        return [
            '/phu-kien/chuot-ban-phim-may-tinh',
            '/phu-kien/may-tinh-laptop/phan-mem',
            'phu-kien/may-tinh-laptop/webcam',
            '/phu-kien/may-tinh-laptop/de-tan-nhiet',
            '/phu-kien/thiet-bi-mang',
            '/thiet-bi-am-thanh'
            '/man-hinh',
        ]
    return []






    
