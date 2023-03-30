# Include necesary packages
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

web_url = 'https://fptshop.com.vn'


def get_list(input_string):
    # Open Chrome browser
    browser = webdriver.Chrome()

    #Navigate to link
    browser.get(web_url)
    #browser.maximize_window()
    browser.implicitly_wait(20)

    #Remove ads
    ad_remove = browser.find_element(By.XPATH, "//*[@id='onesignal-slidedown-cancel-button']").click()

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
        link = product.find('a', {'class' : 'cdt-product__name'}, {'target' : '_self'}).get('href')
        name = product.find('a', {'class' : 'cdt-product__name'}, {'target' : '_self'}).get('title')
        price = product.find('div', {'class' : 'progress'}).text

        # print(web_url + link)
        # print(name)
        # print(price.get_text())
        # print("\n######################################################################\n")
        doc = {'name': name, 'price': price, 'link': web_url +link}
        product_dict.append(doc)
        
    browser.quit()
    return product_dict


