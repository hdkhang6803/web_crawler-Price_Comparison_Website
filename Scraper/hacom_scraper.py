# Import necessary libraries
from selenium import webdriver
from bs4 import BeautifulSoup
import multi_thread as _thread

# TODO: update this file and PhongVuScraper so they use the same class
domain = 'https://hacom.vn'

# Specify the path to the webdriver and website URL to scrape
driver_path = './chromedriver/chromedriver.exe'

categories = [
                {'name': 'Laptop', 'links' : [
                    'https://hacom.vn/laptop',
                ]},
                {'name': 'Desktop', 'links' : [
                    'https://hacom.vn/may-tinh-de-ban', 
                    'https://hacom.vn/pc-gaming-streaming',
                    "https://hacom.vn/pc-do-hoa-render-hnc",
                    'https://hacom.vn/may-tram-hang',
                    'https://hacom.vn/may-chu-hang'
                ]},
                {'name': 'LinhKien', 'links' : [
                    'https://hacom.vn/linh-kien-may-tinh',
                    'https://hacom.vn/linh-kien-laptop',
                    'https://hacom.vn/quat-tan-nhiet',
                ]},
                {'name': 'PhuKien', 'links' : [
                    'https://hacom.vn/linh-phu-kien-laptop',
                    'https://hacom.vn/day-cap-cac-loai',
                    'https://hacom.vn/thiet-bi-chuyen-doi',
                    'https://hacom.vn/bo-chia-tin-hieu',
                    'https://hacom.vn/phu-kien-khac',
                    'https://hacom.vn/phu-kien-hdd',
                    'https://hacom.vn/phu-kien-man-hinh',
                    'https://hacom.vn/man-hinh-may-tinh',
                    'https://hacom.vn/phim-chuot-gaming-gear',
                    'https://hacom.vn/thiet-bi-nghe-nhin'
                ]}
            ]

def get_text(parent):
    if parent == None:
        return ""
    return ''.join(parent.find_all(text=True, recursive=False)).strip()

def site_to_product(soup, link):
    if (soup.find('div', {'class', 'ngung-kdoanh'}) != None):
        return None
    title = get_text(soup.find('div', {'class': 'product_detail-title'}).find('h1'))
    print(title)
    price = get_text(soup.find('strong', {'class': 'giakm'}))
    price = price[:-1]
    price = int(price.replace('.', ''))
    image_link = soup.find('div', {'class': 'img-item'}).find('img').get("src")

    # print('Link:', link)
    # # # print('Image:', image)
    # print('Title:', title)
    # print('Price:', price)
    # print('------------------------')
    product = [title, price, link, image_link]
    return product

def div_to_product(product_div):
    info_ele = product_div.find('div', class_='p-info')
    img_ele = product_div.find('div', {'class': 'p-img'})

    if (info_ele == None or img_ele == None):
        return None

    route_ele = info_ele.find('a')
    price_ele = info_ele.find('span', {'class': 'p-price js-get-minPrice'})
    imglink_ele = img_ele.find('img')

    if (route_ele == None or imglink_ele == None or price_ele == None):
        return None

    route = route_ele['href']
    link = domain + route 

    title = route_ele.get_text().strip()
    price = price_ele.get_text().strip()
    price = price[:-1]
    try:
        int(price.replace('.', ''))
    except:
        print("Gia khong phai so!")
        return None
    price = int(price.replace('.', ''))

    img_route = imglink_ele.get('data-src')
    img_link = img_route


    # if (route_ele == None or title_ele == None or price_ele == None):
    #     return None
    # route = route_ele.get('href')
    # link = domain + route

    # img_link = img_ele.get('src')
    # title = title_ele.get('title')
    # price = price_ele.get_text().strip()
    

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

        empty_divs = soup.find_all('div', {'class': 'css-447dxq'})
        if (len(empty_divs) != 0 or i > max_page):
            print("no more page")
            break

        product_divs = soup.find_all('div', {'class': 'p-component item loaded'})

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
            # if (product != None):
            #     products.append(product
        # print(error_product_cnt)
    # Close the webdriver
    # print(len(prod))
    

    # print(url, " errors count: ", error_product_cnt)
    # if (error_product_cnt > 0):
        # print(error_link)
    return products



def scrape_all(ggsheet):
    for cate in categories:
        for link in cate['links']:
            products = get_products_url(link)
            print(products)
            # ggsheet.update_with_data(products, cate["name"])
            # ggsheet.remove_duplicate(ggsheet.categories_id[cate["name"]])
            print(link, "successful!")

def get_list_cate_hacom(database, cate):
    #initialize webdriver
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(executable_path=driver_path, options = options)

    # driver = webdriver.Chrome()

    #get products of each category
    global product_list
    for link in cate['links']:
        product_list = get_products_url(driver, link)
    database.update_with_data(product_list, cate['name'])
    database.remove_duplicate(cate['name'])
    print('######################################' + 'hacom.vn' + ' ' + cate['name'] + ' FINISHED' + '-----' + str(len(product_list)))
    driver.quit()
    

# getProduct("thinkpad")
def get_list_hacom(database):
    return(_thread.run_multi_thread_cate(database, categories, get_list_cate_hacom))

# --------------------------- not updated --------------------------
def get_products_search(productName):
    url = domain + '/tim?q=' + productName + '&page='

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

        empty_divs = soup.find_all('div', {'class': 'css-447dxq'})
        if (len(empty_divs) != 0 or i > 3):
            break

        product_divs = soup.find_all('div', {'class': 'p-component item loaded'})

        # print("PAGE: ", i)
        # print("Url: ", cururl)
        for product_div in product_divs:
            # link = product_div.find('a', {'class': 'css-pxdb0j', 'target': '_self'}).get('href')
            link = product_div.find('div', class_='p-info').find('h3', class_='p-name').find('a')['href']

            driver.get(domain + link)
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