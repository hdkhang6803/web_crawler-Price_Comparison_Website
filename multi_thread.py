import threading
import Scraper.tgdd_scraper as tgdd_scraper
import Scraper.fpt_scraper as fpt_scraper
from GoogleSheet import GoogleSheet
import pandas as pd

spreadsheet_id = '1H5TTOdrTC_T7U7k_ejCUG8BZWn97NuaxD0t4F7LwH8g'
cred_file = 'client_secret.json'
ggsheet = GoogleSheet(spreadsheet_id, cred_file)


def tgdd_crawler():
    tgdd_data = tgdd_scraper.get_list_tgdd(ggsheet)
   


def fpt_crawler():
    fpt_data = fpt_scraper.get_list_fpt(ggsheet)

# Create two threads for the two crawlers
tgdd_thread = threading.Thread(target=tgdd_crawler)
fpt_thread = threading.Thread(target=fpt_crawler)

# Start the threads
tgdd_thread.start()
fpt_thread.start()

# Wait for the threads to finish before proceeding
tgdd_thread.join()
fpt_thread.join()


# ggsheet_database.store_in_db(df)