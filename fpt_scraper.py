# Include necesary packages
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

web_url = 'https://fptshop.com.vn/'


def get_list(input_string):
    # Open Chrome browser
    browser = webdriver.Chrome()

    #Navigate to link
    browser.get(web_url)
    #browser.maximize_window()
    time.sleep(1)

    #Remove ads
    # Wait up to 10 seconds for the element to appear
    ad_remove = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='onesignal-slidedown-cancel-button']")))

    # Click on the element
    ad_remove.click()

    #Navigate to search bar and enter search key
    search_bar = browser.find_element(By.CLASS_NAME, "fs-stxt").send_keys(input_string)
    submit_result = browser.find_element(By.XPATH, "//*[@type='submit']").click()

    #click See More button

    while True:
        try:
            see_more_button = browser.find_element(By.XPATH, "//*//div[@class='c-comment-loadMore']//a[@href='#']")
            see_more_button.click()
            time.sleep(0.5) # Add a small waiting time to allow the page to load
        except:
            break # If the button can no longer be located, break out of the loop


    # Pass the page content to BeautifulSoup
    html_text = browser.page_source


    #parse the html text for content
    html_content = BeautifulSoup(html_text, 'html.parser')

    products = html_content.select('div.row-flex > div.cdt-product:not(.product-status)')

    print(len(products))
    #print(products)
    product_dict = []
    for product in products:

        # print(product)
        # link = product.find('a', {'class' : 'cdt-product__info'}, {'target' : '_self'}).get('href')
        link = product.select_one('div.cdt-product__info a').get('href')
        # name = product.find('a', {'class' : 'cdt-product__info'}, {'target' : '_self'}).get('title')
        name = product.select_one('div.cdt-product__info a').get('title')
        price = product.select_one('div.progress, div.price')
        
        
        # print("https://fptshop.com.vn/" + link)
        # print(name)
        # print(price)
        # print("\n######################################################################\n")
        if price != None:
            price = price.get_text()
            price = int(price.split()[0].replace('.', '').replace(',', '.'))
            doc = {'name': name, 'price': price, 'link': web_url +link}
            product_dict.append(doc)
        
    browser.quit()
    return product_dict


