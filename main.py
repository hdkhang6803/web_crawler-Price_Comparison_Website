import multi_thread as _thread
import threading
from GoogleSheet import GoogleSheet as ggs
import Scraper.fpt_scraper as fpt
import Scraper.tgdd_scraper as tgdd

spreadsheet_id = '1H5TTOdrTC_T7U7k_ejCUG8BZWn97NuaxD0t4F7LwH8g'
cred_file = 'client_secret.json'

ggsheet = ggs(id=spreadsheet_id, cred_file=cred_file)

web_func_list = [fpt.get_list_fpt, tgdd.get_list_tgdd]

try:
    _thread.run_multi_thread_web(web_func_list, ggsheet)
    print("Data fetching successfully")
except:
    print("Data fetching failed!")



