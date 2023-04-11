# Import necessary libraries
from selenium import webdriver
from bs4 import BeautifulSoup
import multi_thread as _thread
import threading

domain = 'https://phongvu.vn'

# Specify the path to the webdriver and website URL to scrape
driver_path = './chromedriver/chromedriver.exe'

categories = [
                {'name': 'Laptop', 'links' : [
                    'https://phongvu.vn/c/laptop',
                    'https://phongvu.vn/c/macbook',
                ]},
                {'name': 'Desktop', 'links' : [
                    'https://phongvu.vn/c/pc',
                    'https://phongvu.vn/c/pc-apple',
                ]},
                {'name': 'PhuKien', 'links' : [
                    'https://phongvu.vn/c/sac-cap-apple',
                    'https://phongvu.vn/c/airpods',
                    'https://phongvu.vn/c/tai-nghe-apple-beats',
                    'https://phongvu.vn/c/ban-phim-chuot-apple',
                    'https://phongvu.vn/c/man-hinh-may-tinh',
                    'https://phongvu.vn/c/phu-kien-pc',
                    'https://phongvu.vn/c/man-hinh-gaming',
                    'https://phongvu.vn/c/chuot',
                    'https://phongvu.vn/c/ban-phim-gaming',
                    'https://phongvu.vn/c/tay-cam-choi-game',
                    'https://phongvu.vn/c/tai-nghe-gaming',
                    'https://phongvu.vn/c/tai-nghe',
                    'https://phongvu.vn/c/loa',
                    'https://phongvu.vn/c/microphone'
                ]},
                {'name': 'LinhKien', 'links' : [
                    'https://phongvu.vn/c/linh-kien-may-tinh',
                ]}
            ]

def get_text(parent):
    if parent == None:
        return ""
    return ''.join(parent.find_all(text=True, recursive=False)).strip()

def site_to_product(soup, link):
    title = get_text(soup.find('h1', {'class': 'css-4kh4rf'}))
    price = soup.find('div', {'class': 'att-product-detail-latest-price css-z55zyl'}).text.strip()
    price = price[:-1]
    price = int(price.replace('.', ''))
    image_link = soup.find('div', {'class': 'productDetailPreview'}).find('img').get("src")

    # print('Link:', link)
    # # # print('Image:', image)
    # print('Title:', title)
    # print('Price:', price)
    # print('------------------------')
    product = [title, price, link, image_link]
    return product

def div_to_product(product_div):
    route_ele = product_div.find('a', {'class': 'css-pxdb0j', 'target': '_self'})
    img_ele = product_div.find('img')
    title_ele = product_div.find('h3')
    price_ele = product_div.find('div', {'class': 'att-product-detail-latest-price css-tzkko0'})
    price_mode = 1

    if (price_ele == None):
        price_ele = product_div.find('div', {'class': 'css-quss1'})
        price_mode = 2

    if (route_ele == None or title_ele == None or price_ele == None):
        return None
    route = route_ele.get('href')
    link = domain + route

    img_link = img_ele.get('src')
    title = title_ele.get('title')
    price = price_ele.get_text().strip()
    if price_mode == 2:
        price = price.split()[0]
    else:
        price = price[:-1]

    try:
        int(price.replace('.', ''))
    except:
        print("Gia khong phai so!")
        return None

    price = int(price.replace('.', ''))

    return [title, price, link, img_link]

def get_products_url(driver, url, max_page = 100):
    # page number
    i = 0 
    # products array
    products = []
    # url of product page
    url = url + "?page="
    # error product count
    error_product_cnt = 0
    error_link = []

    # Load the website
    while True:
        i = i + 1
        cururl = url + str(i)
        driver.get(cururl)

        # Extract the HTML source code of the website
        html = driver.page_source

        # Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        empty_divs = soup.find_all('div', {'class': 'att-no-products-found css-rmetzu'})
        if (len(empty_divs) != 0 or i > max_page):
            print("no more products. page ", i)
            break

        product_divs = soup.find_all('div', {'class': 'css-13w7uog'})
        if (len(product_divs) == 0):
            print("no products with the tag found")
            break

        # print("PAGE: ", i)
        # print("Url: ", cururl)
        for product_div in product_divs:
            tmp = div_to_product(product_div)
            if (tmp != None):
                products.append(tmp) 
            else:
                error_product_cnt += 1
                error_link.append([cururl, product_div])

            # driver.get(link)
            # # Extract the HTML source code of the website
            # html = driver.page_source

            # # Parse the HTML using BeautifulSoup
            # soup = BeautifulSoup(html, 'html.parser')

            # product = site_to_product(soup, link)
            # products.append(product)

        # print(error_product_cnt)

    # Close the webdriver
    # print(len(prod))

    # print(url, " errors count: ", error_product_cnt)
    # if (error_product_cnt > 0):
    #     print(error_link)
    return products

def scrape_all(ggsheet):
    for cate in categories:
        for link in cate['links']:
            products = get_products_url(link)
            print(products)
            # ggsheet.update_with_data(products, cate["name"])
            # ggsheet.remove_duplicate(ggsheet.categories_id[cate["name"]])
            print(link, "successful!")

#KHANG's function
def get_list_cate_pvu(database, cate):
    try:
        #initialize webdriver
        # options = webdriver.ChromeOptions()
        # options.add_experimental_option('excludeSwitches', ['enable-logging'])

        # driver = webdriver.Chrome(executable_path=driver_path, options = options)
        driver = webdriver.Chrome()
        
        #get products of each category
        global product_list
        product_list = []
        for link in cate['links']:
            product_list = product_list + get_products_url(driver, link)
        database.update_with_data(product_list, cate['name'])
        database.remove_duplicate(cate['name'])
        print('######################################' + ' PHONG VU ' + ' ' + cate['name'] + ' FINISHED' + '-----' + str(len(product_list)))
        driver.quit()
        _thread.threads_status_dict[threading.current_thread()] = [0, get_list_cate_pvu, cate]
    except Exception as e:
        _thread.threads_status_dict[threading.current_thread()] = [-1, get_list_cate_pvu, cate]
        print(e)
    

# getProduct("thinkpad")
def get_list_pvu(database):
    return(_thread.run_multi_thread_cate(database, categories, get_list_cate_pvu))

# getProduct("")

# -------------------- not updated ---------------------
def get_products_search(productName):
    url = domain + '/search?router=productListing&query=' + productName + '&page='

    # Initialize the webdriver
    driver = webdriver.Chrome(executable_path=driver_path)

    # Load the website
    i = 0 
    products = []
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
            route = product_div.find('a', {'class': 'css-pxdb0j', 'target': '_self'}).get('href')
            link = domain + route

            driver.get(link)
            # Extract the HTML source code of the website
            html = driver.page_source

            # Parse the HTML using BeautifulSoup
            soup = BeautifulSoup(html, 'html.parser')

            product = site_to_product(soup, link)
            products.append(product)

            

    # Close the webdriver
    # print(len(prod))
    driver.quit()

    return products

