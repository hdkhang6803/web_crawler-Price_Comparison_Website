# Include necesary packages
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import DataStructures.GoogleSheet as ggs
import multi_thread as _thread
import threading
web_url = 'https://www.thegioididong.com'

categories = [
    {'name': 'Laptop', 
     'links' : ['https://www.thegioididong.com/laptop#c=44&o=17&pi=1000']},
    {'name': 'Desktop', 
     'links' : ['https://www.thegioididong.com/may-tinh-de-ban']},
    {'name': 'PhuKien', 
     'links' : ['https://www.thegioididong.com/chuot-ban-phim#c=9386&o=8&pi=1000',
                'https://www.thegioididong.com/tui-chong-soc#c=7923&o=14&pi=1000',
                'https://www.thegioididong.com/gia-do-dien-thoai?g=de-laptop-macbook',
                'https://www.thegioididong.com/o-cung-di-dong',
                'https://www.thegioididong.com/the-nho-dien-thoai',
                'https://www.thegioididong.com/usb',
                'https://www.thegioididong.com/man-hinh-may-tinh#c=5697&o=7&pi=100'],}
]
 
def expand_see_more_button(browser):
    while True:
        try:
            # see_more_button = browser.find_element(By.XPATH, "//*//div[@class='view-more']//a[@href]")
            see_more_button = browser.find_element(By.CSS_SELECTOR,'.view-more a')
            # print(see_more_button)
            see_more_button.click()
            time.sleep(0.5) # Add a small waiting time to allow the page to load
        except:
            break # If the button can no longer be located, break out of the loop

def scrape_all(database, cate_ = 0):
    try:
        #Open Chrome browser
        browser = webdriver.Chrome()
        #Navigate to link
        for cate in categories:
            product_list = []
            for link in cate['links']:

                #Navigate to link
                browser.get(link)

                #Incase not fully expand product page
                expand_see_more_button(browser)

                #parse the html text for content
                html_text = browser.page_source
                html_content = BeautifulSoup(html_text, 'lxml')

                # products = html_content.select(create_css_tag()) 
                products = html_content.select('li[data-price]')

                for product in products:
                    link = product.find('a', {'class' : 'main-contain'}, {'target' : '_self'}).get('href')
                    name = product.find('a', {'class' : 'main-contain'}, {'target' : '_self'}).get('data-name')
                    img_link = ""
                    img_tag = product.find('img')
                    if 'src' in img_tag.attrs:
                        img_link = img_tag['src']
                    else:
                        img_link = img_tag['data-src']
                    price = product.find('a', {'class' : 'main-contain'}, {'target' : '_self'}).get('data-price')
                    if (price == None or price == '0'):
                        continue
                    price = int(price.replace('.', ' ').split()[0])

                    product_list.append([name, price, web_url + link, img_link])

                    if 'Laptop Lenovo Ideapad 3 15ITL6 i5 1135G7/8GB/512GB/Win11 (82H801P9VN)' in name:
                        print(product)     
                        print(web_url + link)
                        print(name)
                        print(price)          
                    # if 'HP Pavilion 15 eg2088TU' in name:
                    #     print(product)
                    # print(web_url + link)
                    # print(name)
                    # print(price)
                    
                    # print("\n######################################################################\n")
            
            # ggs.store_in_db(product_list, cate['name'])
            database.update_with_data(product_list, cate['name'])
            print('######################################' + ' THEGIOIDIDONG ' + ' ' + cate['name'] + ' FINISHED' + '-----' + str(len(product_list)))

        browser.quit() 
        
        _thread.threads_status_dict[threading.current_thread()] = [0, scrape_all, cate_]
    except Exception as e:
        _thread.threads_status_dict[threading.current_thread()] = [-1, scrape_all, cate_]
        print(e)

def get_list_tgdd(database):
    return([threading.Thread(target=scrape_all, args={database})])











# def get_list(input_string): 
#     # Open Chrome browser
#     browser = webdriver.Chrome()

#     #Navigate to link
#     browser.get(web_url)
#     #browser.maximize_window()
#     browser.implicitly_wait(20)

#     #Navigate to search bar and enter search key
#     search_bar = browser.find_element(By.CLASS_NAME, "input-search").send_keys(input_string)
#     submit_result = browser.find_element(By.XPATH, "//*[@type='submit']").click()

#     # #Find the sorting button
#     # sort_button = browser.find_element(By.CLASS_NAME, 'click-sort').click()
#     # # sort_button = browser.find_element(By.XPATH, "//div[@class='sort-select-main sort ']/p[4]")
#     # sort_button = browser.find_element(By.LINK_TEXT, 'Giá thấp đến cao')
#     # browser.implicitly_wait(20)
#     # #double click button
#     # click_sort = sort_button.click()
#     # time.sleep(0.5)
#     # # click_sort = (WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.LINK_TEXT, 'Giá thấp đến cao')))).click()

#     while True:
#         try:
#             # see_more_button = browser.find_element(By.XPATH, "//*//div[@class='view-more']//a[@href]")
#             see_more_button = browser.find_element(By.CSS_SELECTOR,'.view-more a')
#             print(see_more_button)
#             see_more_button.click()
#             time.sleep(0.5) # Add a small waiting time to allow the page to load
#         except:
#             break # If the button can no longer be located, break out of the loop

#     # Pass the page content to BeautifulSoup
#     html_text = browser.page_source


#     #parse the html text for content
#     html_content = BeautifulSoup(html_text, 'lxml')

#     #product = html_content.select("ul > li > a > h3") #dang bị tự bỏ bớt duplicate
#     # products = html_content.find_all('li', {'class' : 'item __cate_44'})
#     products = html_content.select('li.item.__cate_44:not(.ajaxed), li.item.__cate_60:not(.ajaxed), li.item.cat60:not(.ajaxed)') #moi san pham co them tag moi :(

#     product_dict = []
#     for product in products:
#         link = product.find('a', {'class' : 'main-contain'}, {'target' : '_self'}).get('href')
#         name = product.find('a', {'class' : 'main-contain'}, {'target' : '_self'}).get('data-name')
#         price = product.find('a', {'class' : 'main-contain'}, {'target' : '_self'}).get('data-price')
#         price = int(price.replace('.', ' ').split()[0])

#         product_dict.append([name, price, web_url + link])
#         # print(web_url + link)
#         # print(name)
#         # print(price)
        
#         # print("\n######################################################################\n")

#     browser.quit()
#     return product_dict

