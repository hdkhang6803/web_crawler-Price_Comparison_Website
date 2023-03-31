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

    #Find the sorting button
    sort_button = browser.find_element(By.CLASS_NAME, 'click-sort').click()
    # sort_button = browser.find_element(By.XPATH, "//div[@class='sort-select-main sort ']/p[4]")
    sort_button = browser.find_element(By.LINK_TEXT, 'Giá thấp đến cao')
    browser.implicitly_wait(20)
    #double click button
    click_sort = sort_button.click()
    time.sleep(0.5)
    # click_sort = (WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.LINK_TEXT, 'Giá thấp đến cao')))).click()


    # Pass the page content to BeautifulSoup
    html_text = browser.page_source


    #parse the html text for content
    html_content = BeautifulSoup(html_text, 'html.parser')

    #product = html_content.select("ul > li > a > h3") #dang bị tự bỏ bớt duplicate
    products = html_content.find_all('li', {'class' : 'item __cate_44'})
    product_dict = []
    for product in products:
        link = product.find('a', {'class' : 'main-contain'}, {'target' : '_self'}).get('href')
        name = product.find('a', {'class' : 'main-contain'}, {'target' : '_self'}).get('data-name')
        price = product.find('a', {'class' : 'main-contain'}, {'target' : '_self'}).get('data-price')
        price = int(price.replace('.', ' ').split()[0])

        doc = {'name': name, 'price': price, 'link': web_url +link}
        product_dict.append(doc)
        # print(web_url + link)
        # print(name)
        # print(price)
        
        # print("\n######################################################################\n")

    browser.quit()
    return product_dict

