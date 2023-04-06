import multi_thread as _thread
import threading
from GoogleSheet import GoogleSheet as ggs
import Scraper.fpt_scraper as fpt
import Scraper.tgdd_scraper as tgdd

spreadsheet_id = '1H5TTOdrTC_T7U7k_ejCUG8BZWn97NuaxD0t4F7LwH8g'
cred_file = 'client_secret.json'

ggsheet = ggs(id=spreadsheet_id, cred_file=cred_file)

ggsheet.clear_sheets()
web_func_list_1 = [fpt.get_list_fpt]
web_func_list_2 = [tgdd.get_list_tgdd]

try:
    _thread.run_multi_thread_web(web_func_list_1, ggsheet)
    _thread.run_multi_thread_web(web_func_list_2, ggsheet)
    for cate in ['Laptop', 'Desktop', 'PhuKien', 'LinhKien']:
        ggsheet.sort_sheet_by_price(ggsheet.switch_spreadsheet_id()[cate], cate)
    print("Data fetching successfully")
except:
    print("Data fetching failed!")



