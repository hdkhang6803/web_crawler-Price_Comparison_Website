import threading
# import Scraper.tgdd_scraper as tgdd_scraper
# import Scraper.fpt_scraper as fpt_scraper
import Scraper.phongVuScraper as phongVuScraper
import Scraper.hacomScraper as hacomScraper

from GoogleSheet import GoogleSheet
import pandas as pd

spreadsheet_id = '1H5TTOdrTC_T7U7k_ejCUG8BZWn97NuaxD0t4F7LwH8g'
cred_file = 'client_secret.json'
ggsheet = GoogleSheet(spreadsheet_id, cred_file)


# def tgdd_crawler():
#     tgdd_data = tgdd_scraper.get_list_tgdd(ggsheet)
   
def phongVu_crawler():
    phongVuScraper.scrape_all(ggsheet)
    
def hacom_crawler():
    hacomScraper.scrape_all(ggsheet)

# def fpt_crawler():
#     fpt_data = fpt_scraper.get_list_fpt(ggsheet)

def run_multi_thread_cate(categories, database, used_spreadsheet, function):
    threads = []
    for cate in categories:
        t = threading.Thread(target=function, args=(database, cate, used_spreadsheet))
        threads.append(t)

    for t in threads:
        t.start()

    # Wait for all of the threads to finish
    for t in threads:
        t.join()

def run_multi_thread_web(web_func_list, database, used_spreadsheet):
    threads = []
    for web_func in web_func_list:
        t = threading.Thread(target=web_func, args=[database, used_spreadsheet])
        threads.append(t)

    for t in threads:
        t.start()

    # Wait for all of the threads to finish
    for t in threads:
        t.join()
# # Create two threads for the two crawlers
# tgdd_thread = threading.Thread(target=tgdd_crawler)
# fpt_thread = threading.Thread(target=fpt_crawler)
phongVu_thread = threading.Thread(target=phongVu_crawler)
hacom_thread = threading.Thread(target=hacom_crawler)

# # Start the threads
# tgdd_thread.start()
# fpt_thread.start()

# # Wait for the threads to finish before proceeding
# tgdd_thread.join()
# fpt_thread.join()

def startCrawl():
    phongVu_thread.start()
    hacom_thread.start()

    phongVu_thread.join()
    hacom_thread.join()

startCrawl()

# ggsheet_database.store_in_db(df)