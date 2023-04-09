from DataStructures.GoogleSheet import GoogleSheet
from DataStructures.GoogleSheet import GoogleSheet as ggs
import time
from DataStructures.ProductClassifier import ProductClassifier
from DataStructures.SearchEngine import SearchEngine
from datetime import datetime
import multi_thread as thread_
import time
start_time = time.time()
spreadsheet_id = '1H5TTOdrTC_T7U7k_ejCUG8BZWn97NuaxD0t4F7LwH8g'
cred_file = 'client_secret.json'

ggsheet = GoogleSheet(spreadsheet_id, cred_file)
ggsheet.clear_sheets(ggsheet.spreadsheet_for_scrape)

try:
    thread_.run_threads()
    for cate in ['Laptop', 'Desktop', 'PhuKien', 'LinhKien']:
        ggsheet.sort_sheet_by_price(ggsheet.categories_id[cate], cate)
    print("Data fetching successfully")
    # file.seek(0)
    # file.truncate()
    # file.write(str(used_spreadsheet))
except:
    print("Data fetching failed!")

# #SWITCH ACTIVE SPREADSHEET TO NEWLY CRAWLED SPREADSHEET
print("Execute time: --- %s seconds ---" % (time.time() - start_time))




