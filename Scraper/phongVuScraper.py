# Import necessary libraries
from selenium import webdriver
from bs4 import BeautifulSoup

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

def get_products_url(url, max_page = 100):
    # page number
    i = 0 
    # products array
    products = []
    # url of product page
    url = url + "?page="
    # error product count
    error_product_cnt = 0
    error_link = []

    # Initialize the webdriver
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(executable_path=driver_path, options = options)

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

        print("PAGE: ", i)
        print("Url: ", cururl)
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

        print(error_product_cnt)

    # Close the webdriver
    # print(len(prod))
    driver.quit()

    print(url, " errors count: ", error_product_cnt)
    if (error_product_cnt > 0):
        print(error_link)
    return products

def scrape_all(ggsheet):
    for cate in categories:
        cate_count = 0
        for link in cate['links']:
            products = get_products_url(link)
            cate_count += len(products)
            ggsheet.update_with_data(products, cate["name"])
            ggsheet.remove_duplicate(cate["name"])
            print(link, "successful!")
        with open("result.txt", "a+") as f:
            f.write("PHONG VU")
            f.write(cate["name"])
            f.write(str(cate_count))
            f.write("----")



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

