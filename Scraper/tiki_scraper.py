from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import re
import multi_thread as _thread
class product_selector:
    def __init__(self, card, title, price, image):
        self.card = card
        self.title = title
        self.price = price
        self.image = image

categories = [
    {'name': 'Laptop', 
     'links' : ['https://tiki.vn/laptop/c8095']},
    {'name': 'Desktop', 
     'links' : ['https://tiki.vn/pc-may-tinh-bo/c8093']},
    {'name': 'LinhKien',
     'links': ['https://tiki.vn/linh-kien-may-tinh-phu-kien-may-tinh/c8129']},
    {'name': 'PhuKien', 
     'links' : ['https://tiki.vn/thiet-bi-luu-tru/c8060']
    }
    ]

def extractProductInfo(prod_html, prod_selector):
    title = prod_html.select_one(prod_selector.title).get_text().strip()
    price = prod_html.select_one(prod_selector.price).get_text().strip()

    prelink =  prod_html.get('href')
    if '//tka.tiki.vn' in prelink: link = 'https:' + prelink
    else: link = 'https://tiki.vn' + prelink

    if prod_html.select_one(prod_selector.image) == None or price == None:
        return []
    
    img = prod_html.select_one(prod_selector.image).get('src')
    price = re.sub('\D', '', price)
    if (price != ''):
        price = int(price)
        return [title, price, link, img]
    
    return []

def get_products_in_category(database, category, used_spreadsheet):
    driver = webdriver.Chrome()
    product_list = []
    common_prod_selector = product_selector(
        '.product-item',
        'div.name h3',
        '.price-discount__price', 
        'img')

    for link in category['links']:
        i = 0 
        while True:
            i = i + 1
            pagelink = link + '?page=' + str(i)
            driver.get(pagelink)
            # sleep(0.25)
            html_text = driver.page_source
            html_content = BeautifulSoup(html_text, 'html.parser')
            
            products = html_content.select(common_prod_selector.card)
            if len(products) == 0: break

            for product in products:
                pro_info = extractProductInfo(product, common_prod_selector)
                product_list.append(pro_info)
            # print('Scraped', pagelink, '-', len(category_dictionary), category['name'])
            sleep(0.5)
    cates_id = database.switch_spreadsheet_id(used_spreadsheet)
    database.update_with_data(product_list, category['name'], used_spreadsheet)
    database.remove_duplicate(cates_id[category['name']])
    print('######################################' + 'tiki.vn/' + ' ' + category['name'] + ' FINISHED')
    driver.quit()
    return product_list

def scrape_all(database, categories_id):
    for cat in categories:
        print('---- Started crawling', cat['name'], '----')
        product_list = get_products_in_category(cat)
        print('Finished crawling', cat['name'], '-', 
              len(product_list), 'products scraped.')
        # database.update_with_data(product_list, cat['name'])
        print('Updated products on', cat['name'])
        # database.remove_duplicate(categories_id[cat['name']])
        print('Removed duplicates on', cat['name'], '\n')

def get_list_tiki(database, used_spreadsheet):
    _thread.run_multi_thread_cate(database,categories,  used_spreadsheet, get_products_in_category)





    
