from GoogleSheet import GoogleSheet
import multi_thread as _thread
import threading
from GoogleSheet import GoogleSheet as ggs
import Scraper.fpt_scraper as fpt
import Scraper.tgdd_scraper as tgdd
import Scraper.cellphones_scraper as cellp
import Scraper.tiki_scraper as tiki
import Scraper.hacom_scraper as hacom
import Scraper.phongvu_scraper as pvu
import time

spreadsheet_id = '1H5TTOdrTC_T7U7k_ejCUG8BZWn97NuaxD0t4F7LwH8g'
cred_file = 'client_secret.json'

ggsheet = ggs(id=spreadsheet_id, cred_file=cred_file)


file = open("active_spreadsheet.txt", "r+")
active_spreadsheet = file.read()
used_spreadsheet =  int(not(int(active_spreadsheet, base=2)))

ggsheet.clear_sheets(used_spreadsheet)


web_thread_func_list = [
    # hacom.get_list_hacom,
    # pvu.get_list_pvu,
    # tiki.get_list_tiki,
    # fpt.get_list_fpt, 
    tgdd.get_list_tgdd, 
    # cellp.get_list_cellphones
]

waiting_threads = []
for web_thread_func in web_thread_func_list:
    thread = web_thread_func(ggsheet, used_spreadsheet)
    waiting_threads = waiting_threads + thread
# print(threads)
max_thread_per_time = 4
# start first 4 threads
running_threads = []
next_running_index = 0
for i in range(min(max_thread_per_time, len(waiting_threads))):
    t = waiting_threads[i].start()
    running_threads.append(waiting_threads[i])
    next_running_index += 1


while len(waiting_threads) > 0:
    print(len(waiting_threads))
    for thread in (running_threads):
        print('checked' + str(thread) + ' ******* ' + str(next_running_index))
        #if a running thread is finished, remove it and add in new thread
        if not thread.is_alive() and len(waiting_threads) > 0:
            running_threads.remove(thread)
            waiting_threads.remove(thread)
            next_running_index -= 1
            if next_running_index >= len(waiting_threads):
                break
            next_thread =  waiting_threads[next_running_index]
            if not next_thread.is_alive():
                next_thread.start()
                print(str(len(running_threads)) + ' **** ' + str(len(waiting_threads)) + ' ---- ' + str(waiting_threads[next_running_index]))
                running_threads.append(waiting_threads[next_running_index])
            next_running_index = (next_running_index + 1) % len(waiting_threads)
    time.sleep(2.5)


for cate in ['Laptop', 'Desktop', 'PhuKien', 'LinhKien']:
    ggsheet.sort_sheet_by_price(ggsheet.switch_spreadsheet_id(used_spreadsheet)[cate], cate, used_spreadsheet)

try:
    


        # # check which threads have finished
        # for thread in threads:
        #     if thread.is_alive():
        #         print('waiting for ' + str(thread))
        #         thread.join()
        #     if not thread.is_alive():
        #         threads.remove(thread)
        #         print("Thread joined")

        #         # start a new thread if there are still threads waiting
        #         if threads:
        #             threads[0].start()
        #         break


    print("Data fetching successfully")
    # file.seek(0)
    # file.truncate()
    # file.write(str(used_spreadsheet))
    file.close()
except:
    print("Data fetching failed!")
    file.close()

# #SWITCH ACTIVE SPREADSHEET TO NEWLY CRAWLED SPREADSHEET





