# Import necessary libraries
from selenium import webdriver
from bs4 import BeautifulSoup

domain = 'https://phongvu.vn'

# Specify the path to the webdriver and website URL to scrape
driver_path = './chromedriver/chromedriver.exe'
# url = 'https://www.example.com'

def getText(parent):
    return ''.join(parent.find_all(text=True, recursive=False)).strip()

def getProduct(productName):
    url = domain + '/search?router=productListing&query=' + productName + '&page='

    # Initialize the webdriver
    driver = webdriver.Chrome(executable_path=driver_path)

    # Load the website
    i = 0 
    prod = []
    while True:
        i = i + 1
        cururl = url + str(i)
        driver.get(cururl)

        # Extract the HTML source code of the website
        html = driver.page_source

        # Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        empty_divs = soup.find_all('div', {'class': 'att-no-products-found css-rmetzu'})
        if (len(empty_divs) != 0 or i > 3):
            break

        product_divs = soup.find_all('div', {'class': 'css-13w7uog'})

        print("PAGE: ", i)
        print("Url: ", cururl)
        for product_div in product_divs:
            link = product_div.find('a', {'class': 'css-pxdb0j', 'target': '_self'}).get('href')

            driver.get(domain + link)
            # Extract the HTML source code of the website
            html = driver.page_source

            # Parse the HTML using BeautifulSoup
            soup = BeautifulSoup(html, 'html.parser')

            title = getText(soup.find('h1', {'class': 'css-4kh4rf'}))
            price = soup.find('div', {'class': 'att-product-detail-latest-price css-z55zyl'}).text.strip()

            # image = product_div.find('img').get('src')
            # title = product_div.find('h3').get('title')
            # price = product_div.find('div', {'class': 'att-product-detail-latest-price css-tzkko0'}).text.strip()
            
            print('Link:', domain + link)
            # # print('Image:', image)
            print('Title:', title)
            print('Price:', price)
            print('------------------------')
            prod.append([title, price, domain + link])

    # Close the webdriver
    # print(len(prod))
    driver.quit()

    return prod

# getProduct("")