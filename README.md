# PRICE COMPARISON WEBSITE WITH DATA CRAWLER
## **I. About the project:**
The increasing popularity of online shopping has created a demand for reliable price comparison tools, as customers often find it challenging to compare prices across different e-commerce platforms manually. By aggregating data from various e-commerce websites, a price comparison website can help customers save time and money by providing up-to-date pricing information.
The project’s objective is to create a price comparison website that offers a user-friendly interface that enables customers to search for specific products, and filter results by price, brand, or other relevant factors. Additionally, the website will provide links to the retailers' websites, allowing customers to complete their purchases on the retailer's platform.
The development of the website will involve several key components, including a web crawler that can scrape data from e-commerce websites, a database for storing the collected data, and a front-end interface for customers to access the data. The web crawler will be programmed to extract product information from multiple retailers, including product names, product links, prices, and images. The data will be organized and stored in a Google spreadsheet, which will be optimized for fast and efficient retrieval.

## **II. Architecture:**
* **Selenium** is used for web browsing.  It provides a set of tools and libraries that allow developers and testers to create automated tests, simulate user interactions, and scrape web content. Selenium works with a variety of web browsers, including Chrome, Firefox, Safari, Edge, and Internet Explorer.
* **BeautifulSoup** is used for parsing HTML and XML documents. It provides a simple and intuitive way to navigate, search, and modify the elements of an HTML or XML document, making it a popular tool for web scraping and data extraction.
* **Google Sheet** is used to store the scraped data. Two tabs are being used alternatively and synchronically: one tab is used for storing newly scraped data while the other is used for users' queries.
* **Window Task Scheduler** is used to automatically start the crawling task when the project is run. Users can set the time the task starts every day.
* **`threading` Python library** is used to implement multiple threads for the crawling task. When a thread meets an error, the task is stored in a temporary storage to rerun when other tasks finish.

## **III. How to run:**
To run the website and schedule the task, the following steps must be followed:
1. Clone the source code to the local workspace.
2. In the source code, run the scheduler.py file and enter the wanted time at which the crawler task will start. If the success message appears, the task is scheduled in Windows Task Scheduler.
3. Accessing the URL: http://shopaholic.pythonanywhere.com/ to access the price comparison website and experience the web.
4. To run the crawler immediately without waiting for the scheduled time to come, open Windows Task Scheduler, navigate to the CrawlerTask, and click Run. Another way is to run the main.py file.

View a detailed report of this project: [link](https://drive.google.com/file/d/1KwHLfAKvSE0aGaQuGen1eF8jEUFUcN3t/view?usp=sharing)
