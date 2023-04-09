# Include necesary packages
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import multi_thread as _thread
import threading
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, MoveTargetOutOfBoundsException
from DataStructures.GoogleSheet import GoogleSheet
web_url = 'https://fptshop.com.vn/'

categories = [
    {'name': 'Laptop', 
     'links' : ['https://fptshop.com.vn/may-tinh-xach-tay?sort=ban-chay-nhat&trang=1000']},
    {'name': 'Desktop', 
     'links' : ['https://fptshop.com.vn/may-tinh-de-ban?sort=ban-chay-nhat&trang=100']},
    {'name': 'PhuKien', 
     'links' : ['https://fptshop.com.vn/man-hinh?sort=ban-chay-nhat&trang=1000',
                'https://fptshop.com.vn/phu-kien/the-nho',
                'https://fptshop.com.vn/phu-kien/tai-nghe',
                'https://fptshop.com.vn/phu-kien/usb-o-cung',
                'https://fptshop.com.vn/phu-kien/chuot',
                'https://fptshop.com.vn/phu-kien/ban-phim',
                'https://fptshop.com.vn/phu-kien/balo-tui-xach']},
    {'name' : 'LinhKien', 
     'links' : ['https://fptshop.com.vn/linh-kien/mainboard',
                'https://fptshop.com.vn/linh-kien/cpu',
                'https://fptshop.com.vn/linh-kien/vga',
                'https://fptshop.com.vn/linh-kien/ram',
                'https://fptshop.com.vn/linh-kien/o-cung',
                'https://fptshop.com.vn/linh-kien/nguon-may-tinh',
                'https://fptshop.com.vn/linh-kien/vo-case',
                'https://fptshop.com.vn/linh-kien/tan-nhiet',
                'https://fptshop.com.vn/linh-kien/o-dia-quang']}
]

def expand_see_more_button(browser, cater):
    while True:
        try:
            # see_more_button = browser.find_element(By.XPATH, "//*//div[@class='view-more']//a[@href]")
            # see_more_button = browser.find_element(By.XPATH, new_button_xpath)
            see_more_button = browser.find_element(By.XPATH, "//*//div//a[@style='cursor: pointer;']")
            if cater == "LinhKien":
                browser.execute_script("arguments[0].scrollIntoView({behavior : 'instant', block : 'center'});", see_more_button)
                time.sleep(1)
                hover = ActionChains(browser).move_to_element_with_offset(see_more_button, 160, 0)
                hover.perform()
                time.sleep(1)
                hover = ActionChains(browser).move_to_element(see_more_button)
                hover.perform()
                
            see_more_button.click()
            time.sleep(1) # Add a small waiting time to allow the page to load
            # browser.implicitly_wait(20)
        except NoSuchElementException:
            break # If the button can no longer be located, break out of the loop
        except ElementNotInteractableException:
            break
        except MoveTargetOutOfBoundsException:
            break

def scroll_to_lazy(browser):
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);") #scroll from top to bot
        # elements = browser.find_elements(By.CSS_SELECTOR, 'a .lazy-load-image-background, .product__img, .product_img')
        #         # print(element)
        # for element in elements:
        #     browser.execute_script("arguments[0].scrollIntoView(true);", element)
        #     time.sleep(0.02)
        #     browser.implicitly_wait(20)

def get_list_cate_fpt(database, cate):
    product_list = []
    browser = webdriver.Chrome()
    for link in cate['links']:
        #Navigate to link
        browser.get(link)
        browser.maximize_window()

        #Remove ads
        # Wait up to 10 seconds for the element to appear
        # ad_remove = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='onesignal-slidedown-cancel-button']")))

        #Incase not fully expand product page
        expand_see_more_button(browser, cate['name'])

        #scroll to lazy loaded element
        scroll_to_lazy(browser)

        #parse the html text for content
        html_text = browser.page_source
        html_content = BeautifulSoup(html_text, 'lxml')

        # products = html_content.select(create_css_tag()) 
        products = html_content.select('.product-item, .cdt-product, .product__item, .cate-product')

        for product in products:
            #get product info
            # print(product)
            link = product.find('a').get('href')
            if web_url not in link:
                link = web_url + link
            name = product.select_one('h3').get_text().strip()
            # print(name)
            price = product.select_one('.progress, .product_progress, .product_main-price, .price')
            if price == None or price == 0:
                continue
            
            price = price.get_text()
            price = int(price.replace('.', '').replace('đ','').split()[0])         
                   

            img_tag = product.select_one('img')
            if img_tag != None:
                img_link = img_tag.get('src')
                if img_link is None:
                    img_link = img_tag.get('data-src')


            product_list.append([name, price, link, img_link])

            # print(web_url + link)
            # print(name)
            # print(price)
            
            # print("\n######################################################################\n")
    database.update_with_data(product_list, cate['name'])
    database.remove_duplicate(cate['name'])
    print('######################################' + 'FPT' + ' ' + cate['name'] + ' FINISHED' + '-----' + str(len(product_list)))
    browser.quit()
    # return product_list
       


def get_list_fpt(database):
    return (_thread.run_multi_thread_cate(database, categories, get_list_cate_fpt))




##Cách 2: Lấy search
# def get_list_fpt(database, used_spreadsheet):
# browser = webdriver.Chrome()
# browser.get('https://fptshop.com.vn/linh-kien/ram')
# browser.maximize_window()
# expand_see_more_button(browser, 'LinhKien')
# #parse the html text for content
# html_text = browser.page_source
# html_content = BeautifulSoup(html_text, 'lxml')

# # products = html_content.select(create_css_tag()) 
# products = html_content.select('.product-item, .cdt-product, .product__item, .cate-product')

# for product in products:
#     #get product info
#     # print(product)
#     link = product.find('a').get('href')
#     if web_url not in link:
#         link = web_url + link
#     name = product.select_one('h3').get_text().strip()
#     # print(name)
#     price = product.select_one('.progress, .product_progress, .product_main-price, .price')
#     if price != None:
#         price = price.get_text()
#         price = int(price.replace('.', '').replace('đ','').split()[0])                

#     img_tag = product.select_one('img')
#     if img_tag != None:
#         img_link = img_tag.get('src')
#         if img_link is None:
#             img_link = img_tag.get('data-src')

#     print(web_url + link)
#     print(name)
#     print(price)
    
#     print("\n######################################################################\n")

# ##Cách 3: Lấy the0 element
# def get_list_fpt(database):
#     #Open Chrome browser
#     browser = webdriver.Chrome()

#     #Navigate to link
#     for cater in categories:
#         product_list = []
#         for link in cater['links']:

#             #Navigate to link
#             browser.get(link)

#             #Remove ads
#             # Wait up to 10 seconds for the element to appear
#             # ad_remove = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='onesignal-slidedown-cancel-button']")))

#             #Incase not fully expand product page
#             expand_see_more_button(browser)

#             #scroll to lazy loaded element
#             scroll_to_lazy(browser)

#             # products = html_content.select(create_css_tag()) 
#             products = browser.find_elements(By.CSS_SELECTOR, '.product-item, .cdt-product, .product__item, .cate-product')

#             for product in products:
#                 #get product info
#                 # print(product)
#                 link = product.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
#                 name = product.find_element(By.CSS_SELECTOR, 'h3').text.strip()
#                 # print(name)
#                 try:
#                     price = product.find_element(By.CSS_SELECTOR, '.progress, .product_progress, .product_main-price, .price')
#                     price = price.text
#                     price = int(price.replace('.', '').replace('đ','').split()[0])                
#                 except:
#                     price = ""

#                 try:
#                     img_link = product.find_element(By.CSS_SELECTOR, 'img')
#                     img_link = img_link.get_attribute('src')
#                 except:
#                     img_link = ""

#                 product_list.append([name, price, web_url + link, img_link])

#                 # print(web_url + link)
#                 # print(name)
#                 # print(price)
                
#                 # print("\n######################################################################\n")
        
#         # ggs.store_in_db(product_list, cater['name'])
#         database.update_with_data(product_list, cater['name'])
#         database.remove_duplicate(database.categories_id[cater['name']])

##Cách 1: Đi vào từng trang lấy elements
# def get_list_fpt(database):
#     #Open Chrome browser
#     browser = webdriver.Chrome()

#     #Navigate to link
#     for cater in categories:
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


