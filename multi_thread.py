import threading
import Scraper.tgdd_scraper as tgdd_scraper
import Scraper.fpt_scraper as fpt_scraper
import ggsheet_database
import pandas as pd

input_string = "laptop asus gaming"

df = []


def tgdd_crawler():
    tgdd_data = tgdd_scraper.get_list(input_string)
    global df 
    # df = pd.concat([df, pd.DataFrame(tgdd_data)], ignore_index=True)
    df.append(tgdd_data)
    print(df)


def fpt_crawler():
    fpt_data = fpt_scraper.get_list(input_string)
    global df
    # df = pd.concat([df, pd.DataFrame(fpt_data)], ignore_index=True)
    df.append(fpt_data)
    print(df)

# Create two threads for the two crawlers
tgdd_thread = threading.Thread(target=tgdd_crawler)
fpt_thread = threading.Thread(target=fpt_crawler)

# Start the threads
tgdd_thread.start()
fpt_thread.start()

# Wait for the threads to finish before proceeding
tgdd_thread.join()
fpt_thread.join()


ggsheet_database.store_in_db(df)