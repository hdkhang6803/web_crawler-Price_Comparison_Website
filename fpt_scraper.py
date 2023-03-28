# Include necesary packages
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

input_string = "Laptop"
web_url = 'https://fptshop.com.vn/'

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
see_more_button = browser.find_element(By.XPATH, "//*[@href='#']")
while (see_more_button):
    see_more_button.click()
    browser.implicitly_wait(30)
    see_more_button = browser.find_element(By.XPATH, "//*[@href='#']")


# # Pass the page content to BeautifulSoup
# html_text = browser.page_source


# #parse the html text for content
# html_content = BeautifulSoup(html_text, 'html.parser')

# #product = html_content.select("ul > li > a > h3") #dang bị tự bỏ bớt duplicate
# products = html_content.find_all('li', {'class' : 'item __cate_44'})
# product_dict = []
# for product in products:
#     link = product.find('a', {'class' : 'main-contain'}, {'target' : '_self'}).get('href')
#     name = product.find('a', {'class' : 'main-contain'}, {'target' : '_self'}).get('data-name')
#     price = product.find('a', {'class' : 'main-contain'}, {'target' : '_self'}).get('data-price')
    
#     print(web_url + link)
#     print(name)
#     print(price)
    
#     print("\n######################################################################\n")

# browser.quit()


