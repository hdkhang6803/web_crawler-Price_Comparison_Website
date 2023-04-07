import multi_thread as _thread
import threading
from GoogleSheet import GoogleSheet as ggs
import Scraper.fpt_scraper as fpt
import Scraper.tgdd_scraper as tgdd
import Scraper.cellphones_scraper as cellp
import Scraper.tiki_scraper as tiki
from datetime import datetime

spreadsheet_id = '1H5TTOdrTC_T7U7k_ejCUG8BZWn97NuaxD0t4F7LwH8g'
cred_file = 'client_secret.json'

ggsheet = ggs(id=spreadsheet_id, cred_file=cred_file)

file = open("active_spreadsheet.txt", "r+")
active_spreadsheet = file.read()
used_spreadsheet =  int(not(int(active_spreadsheet, base=2)))

ggsheet.clear_sheets(used_spreadsheet)

web_func_list_1 = [fpt.get_list_fpt]
web_func_list_2 = [tgdd.get_list_tgdd]
web_func_list_3 = [cellp.get_list_cellphones]
web_func_list_4 = [tiki.get_list_tiki]

try:
    # _thread.run_multi_thread_web(web_func_list_1, ggsheet, used_spreadsheet)
    # _thread.run_multi_thread_web(web_func_list_2, ggsheet, used_spreadsheet)
    # _thread.run_multi_thread_web(web_func_list_3, ggsheet, used_spreadsheet)
    _thread.run_multi_thread_web(web_func_list_4, ggsheet, used_spreadsheet)
    for cate in ['Laptop', 'Desktop', 'PhuKien', 'LinhKien']:
        ggsheet.sort_sheet_by_price(ggsheet.switch_spreadsheet_id(used_spreadsheet)[cate], cate, used_spreadsheet)
    print("Data fetching successfully")
    file.seek(0)
    file.truncate()
    file.write(str(used_spreadsheet))
    file.close()
except:
    print("Data fetching failed!")
    file.close()

#SWITCH ACTIVE SPREADSHEET TO NEWLY CRAWLED SPREADSHEET





