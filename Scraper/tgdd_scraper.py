# Include necesary packages
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

web_url = 'https://www.thegioididong.com'

def get_list(input_string): 
    # Open Chrome browser
    browser = webdriver.Chrome()

    #Navigate to link
    browser.get(web_url)
    #browser.maximize_window()
    browser.implicitly_wait(20)

    #Navigate to search bar and enter search key
    search_bar = browser.find_element(By.CLASS_NAME, "input-search").send_keys(input_string)
    submit_result = browser.find_element(By.XPATH, "//*[@type='submit']").click()

    # #Find the sorting button
    # sort_button = browser.find_element(By.CLASS_NAME, 'click-sort').click()
    # # sort_button = browser.find_element(By.XPATH, "//div[@class='sort-select-main sort ']/p[4]")
    # sort_button = browser.find_element(By.LINK_TEXT, 'Giá thấp đến cao')
    # browser.implicitly_wait(20)
    # #double click button
    # click_sort = sort_button.click()
    # time.sleep(0.5)
    # # click_sort = (WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.LINK_TEXT, 'Giá thấp đến cao')))).click()

    while True:
        try:
            # see_more_button = browser.find_element(By.XPATH, "//*//div[@class='view-more']//a[@href]")
            see_more_button = browser.find_element(By.CSS_SELECTOR,'.view-more a')
            print(see_more_button)
            see_more_button.click()
            time.sleep(0.5) # Add a small waiting time to allow the page to load
        except:
            break # If the button can no longer be located, break out of the loop

    # Pass the page content to BeautifulSoup
    html_text = browser.page_source


    #parse the html text for content
    html_content = BeautifulSoup(html_text, 'html.parser')

    #product = html_content.select("ul > li > a > h3") #dang bị tự bỏ bớt duplicate
    # products = html_content.find_all('li', {'class' : 'item __cate_44'})
    products = html_content.select('li.item.__cate_44:not(.ajaxed), li.item.__cate_60:not(.ajaxed), li.item.cat60:not(.ajaxed)') #moi san pham co them tag moi :(

    product_dict = []
    for product in products:
        link = product.find('a', {'class' : 'main-contain'}, {'target' : '_self'}).get('href')
        name = product.find('a', {'class' : 'main-contain'}, {'target' : '_self'}).get('data-name')
        price = product.find('a', {'class' : 'main-contain'}, {'target' : '_self'}).get('data-price')
        price = int(price.replace('.', ' ').split()[0])
        
        product_dict.append([name, price, web_url + link])
        # print(web_url + link)
        # print(name)
        # print(price)
        
        # print("\n######################################################################\n")

    browser.quit()
    return product_dict

