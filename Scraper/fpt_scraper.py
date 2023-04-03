# Include necesary packages
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.action_chains import ActionChains

web_url = 'https://fptshop.com.vn/'

catergories = [{'name': 'Laptop', 'links' : ['https://fptshop.com.vn/may-tinh-xach-tay?sort=ban-chay-nhat&trang=1000']},
                    {'name': 'Desktop', 'links' : ['https://fptshop.com.vn/may-tinh-de-ban?sort=ban-chay-nhat&trang=100']},
                    {'name': 'PhuKien', 'links' : ['https://fptshop.com.vn/man-hinh?sort=ban-chay-nhat&trang=1000',
                                   'https://fptshop.com.vn/phu-kien/the-nho',
                                   'https://fptshop.com.vn/phu-kien/tai-nghe',
                                   'https://fptshop.com.vn/phu-kien/usb-o-cung',
                                   'https://fptshop.com.vn/phu-kien/chuot',
                                   'https://fptshop.com.vn/phu-kien/ban-phim',
                                   'https://fptshop.com.vn/phu-kien/balo-tui-xach']},
                    {'name' : 'LinhKien', 'links' : ['https://fptshop.com.vn/linh-kien/mainboard',
                                                     'https://fptshop.com.vn/linh-kien/cpu',
                                                     'https://fptshop.com.vn/linh-kien/vga',
                                                     'https://fptshop.com.vn/linh-kien/ram',
                                                     'https://fptshop.com.vn/linh-kien/o-cung',
                                                     'https://fptshop.com.vn/linh-kien/nguon-may-tinh',
                                                     'https://fptshop.com.vn/linh-kien/vo-case',
                                                     'https://fptshop.com.vn/linh-kien/tan-nhiet',
                                                     'https://fptshop.com.vn/linh-kien/o-dia-quang']} #do linhkien co man hinh -> reconsider
                ]

def expand_see_more_button(browser):
    while True:
        try:
            # see_more_button = browser.find_element(By.XPATH, "//*//div[@class='view-more']//a[@href]")
            see_more_button = browser.find(By.CSS_SELECTOR, 'a[onclick]')
            print(see_more_button)
            see_more_button.click()
            # time.sleep(0.5) # Add a small waiting time to allow the page to load
            browser.implicitly_wait(20)
        except:
            break # If the button can no longer be located, break out of the loop

def scroll_to_lazy(browser):
        elements = browser.find_elements(By.CSS_SELECTOR, 'a .lazy-load-image-background')
                # print(element)
        for element in elements:
            browser.execute_script("arguments[0].scrollIntoView(true);", element)
            # time.sleep(0.5)
            browser.implicitly_wait(20)

##Cách 2: Lấy search
def get_list_fpt(database):
    #Open Chrome browser
    browser = webdriver.Chrome()

    #Navigate to link
    for cater in catergories:
        product_list = []
        for link in cater['links']:

            #Navigate to link
            browser.get(link)

            #Remove ads
            # Wait up to 10 seconds for the element to appear
            # ad_remove = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='onesignal-slidedown-cancel-button']")))

            #Incase not fully expand product page
            expand_see_more_button(browser)

            #scroll to lazy loaded element
            scroll_to_lazy(browser)

            #parse the html text for content
            html_text = browser.page_source
            html_content = BeautifulSoup(html_text, 'lxml')

            # products = html_content.select(create_css_tag()) 
            products = html_content.select('.product-item, .cdt-product, .product__item, .cate-product')

            for product in products:
                #get product info
                print(product)
                link = product.find('a').get('href')
                name = product.select_one('h3').get_text()
                print(name)
                price = product.select_one('.progress, .product_progress, .product_main-price, .price')
                if price != None:
                    price = price.get_text()
                    price = int(price.replace('.', '').replace('đ','').split()[0])                

                img_link = product.select_one('img').get('src')

                product_list.append([name, price, web_url + link, img_link])

                # print(web_url + link)
                # print(name)
                # print(price)
                
                # print("\n######################################################################\n")
        
        # ggs.store_in_db(product_list, cater['name'])
        database.update_with_data(product_list, cater['name'])
        database.remove_duplicate(database.categories_id[cater['name']])

##Cách 1: Đi vào từng trang lấy elements
# def get_list_fpt(database):
#     #Open Chrome browser
#     browser = webdriver.Chrome()

#     #Navigate to link
#     for cater in catergories:
#         product_list = []
#         for link in cater['links']:

#             #Navigate to link
#             browser.get(link)

#             #Remove ads
#             # Wait up to 10 seconds for the element to appear
#             ad_remove = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='onesignal-slidedown-cancel-button']")))

#             #Incase not fully expand product page
#             expand_see_more_button(browser)

#             #parse the html text for content
#             html_text = browser.page_source
#             html_content = BeautifulSoup(html_text, 'html.parser')

#             # products = html_content.select(create_css_tag()) 
#             products = html_content.select('.product-item, .cdt-product, .product__item, .cate-product')

#             for product in products:

#                 print(product)
#                 link = product.find('a').get('href')

#                 #get to product page
#                 browser.get(web_url + link)

#                 #parse product HTML
#                 product_script = BeautifulSoup(browser.page_source, 'html.parser')
#                 # print(product_script)

#                 #get product info
#                 name = product_script.select_one('h1.st-name').get_text()
#                 print(name)
#                 price = product_script.select_one('div.st-price-main').get_text()
#                 price = int(price.replace('.', '').replace('₫',''))
#                 img_link = product_script.select_one('div > div > div > div > div > img').get('src')

#                 product_list.append([name, price, web_url + link, img_link])

#                 # if 'Laptop Dell Inspiron 16 5620 i5 1235U' in name:
#                 #     print(product)
#                 # if 'HP Pavilion 15 eg2088TU' in name:
#                 #     print(product)
#                 print(web_url + link)
#                 print(name)
#                 print(price)
                
#                 print("\n######################################################################\n")
        
#         # ggs.store_in_db(product_list, cater['name'])
#         database.update_with_data(product_list, cater['name'])
#         database.remove_duplicate(database.categories_id[cater['name']])



# def get_list(input_string):
#     # Open Chrome browser
#     browser = webdriver.Chrome()

#     #Navigate to link
#     browser.get(web_url)
#     #browser.maximize_window()
#     time.sleep(1)

#     #Remove ads
#     # Wait up to 10 seconds for the element to appear
#     ad_remove = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='onesignal-slidedown-cancel-button']")))

#     # Click on the element
#     ad_remove.click()

#     #Navigate to search bar and enter search key
#     search_bar = browser.find_element(By.CLASS_NAME, "fs-stxt").send_keys(input_string)
#     submit_result = browser.find_element(By.XPATH, "//*[@type='submit']").click()
#     time.sleep(2)

#     #click See More button

#     while True:
#         try:
#             see_more_button = browser.find_element(By.XPATH, "//*//div[@class='c-comment-loadMore']//a[@href='#']")
#             see_more_button.click()
#             time.sleep(0.5) # Add a small waiting time to allow the page to load
#         except:
#             break # If the button can no longer be located, break out of the loop


#     # Pass the page content to BeautifulSoup
#     html_text = browser.page_source


#     #parse the html text for content
#     html_content = BeautifulSoup(html_text, 'html.parser')

#     products = html_content.select('div.row-flex > div.cdt-product:not(.product-status)')

#     print(len(products))
#     #print(products)
#     product_dict = []
#     for product in products:

#         # print(product)
#         # link = product.find('a', {'class' : 'cdt-product__info'}, {'target' : '_self'}).get('href')
#         link = product.select_one('div.cdt-product__info a').get('href')
#         # name = product.find('a', {'class' : 'cdt-product__info'}, {'target' : '_self'}).get('title')
#         name = product.select_one('div.cdt-product__info a').get('title')
#         price = product.select_one('div.progress, div.price')
        
        
#         # print("https://fptshop.com.vn/" + link)
#         print(name)
#         # print(price)
#         print("\n######################################################################\n")
#         if price != None:
#             price = price.get_text()
#             price = int(price.split()[0].replace('.', '').replace(',', '.'))
#             product_dict.append([name, price, web_url + link])
        
#     browser.quit()
#     return product_dict


