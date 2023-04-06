from GoogleSheet import GoogleSheet
import Scraper.phongVuScraper as phongVuScraper
import Scraper.hacomScraper as hacomScraper
import multi_thread as _thread
import threading
from GoogleSheet import GoogleSheet as ggs
import Scraper.fpt_scraper as fpt
import Scraper.tgdd_scraper as tgdd

spreadsheet_id = '1H5TTOdrTC_T7U7k_ejCUG8BZWn97NuaxD0t4F7LwH8g'
cred_file = 'client_secret.json'

ggsheet = ggs(id=spreadsheet_id, cred_file=cred_file)

if __name__ == "__main__":
    ggsheet = GoogleSheet(spreadsheet_id, cred_file)
    # hacomScraper.scrape_all(ggsheet)
    # hacomScraper.get_products_url('https://hacom.vn/linh-kien-may-tinh?page=25')
    # training_data = ggsheet.get_data(10, 4, "Laptop")

    # phongvudata = phongVuScraper.get_products_url("https://phongvu.vn/c/man-hinh-may-tinh?page=4", 1)
    # print(phongvudata)
    # print(phongvudata)
    # fptdata = fpt.get_list("laptop")

    # # print(phongvudata)

    # # change category to update different product type sheet
    # category = "Laptop"
    # ggsheet.update_with_data(phongvudata, category)
    # ggsheet.remove_duplicate(categories_id[category])
web_func_list = [fpt.get_list_fpt, tgdd.get_list_tgdd]

try:
    _thread.run_multi_thread_web(web_func_list, ggsheet)
    print("Data fetching successfully")
except:
    print("Data fetching failed!")



