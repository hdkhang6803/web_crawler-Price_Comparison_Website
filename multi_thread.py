import threading
from DataStructures.GoogleSheet import GoogleSheet
import time
import Scraper.fpt_scraper as fpt
import Scraper.tgdd_scraper as tgdd
import Scraper.cellphones_scraper as cellp
import Scraper.tiki_scraper as tiki
import Scraper.hacom_scraper as hacom
import Scraper.phongvu_scraper as pvu

web_thread_func_list = [
    hacom.get_list_hacom,
    pvu.get_list_pvu,
    tiki.get_list_tiki,
    fpt.get_list_fpt, 
    tgdd.get_list_tgdd, 
    cellp.get_list_cellphones
]


def run_multi_thread_cate(database, categories, function):
    threads = []
    for cate in categories:
        t = threading.Thread(target=function, args=(database, cate))
        threads.append(t)

    return threads

# def run_multi_thread_web(web_func_list, database):
#     threads = []
#     for web_func in web_func_list:
#         t = threading.Thread(target=web_func, args=[database])
#         threads.append(t)

#     for t in threads:
#         t.start()

#     # Wait for all of the threads to finish
#     for t in threads:
#         t.join()

threads_status_dict = {}

def check_running_thread_add_new(waiting_threads, running_threads, next_running_index, max_thread_per_time):
    #Start the first 4 thread
    for i in range(min(max_thread_per_time, len(waiting_threads))):
        waiting_threads[i].start()
        running_threads.append(waiting_threads[i])
        next_running_index += 1

    while len(waiting_threads) > 0:
        print(len(waiting_threads))
        for thread in (running_threads):
            print('checked' + str(thread) + ' ******* ' + str(next_running_index))
            #If a running thread is finished, remove it and add in new thread
            if not thread.is_alive() and len(waiting_threads) > 0:

                running_threads.remove(thread)
                waiting_threads.remove(thread)
                next_running_index -= 1
                if next_running_index >= len(waiting_threads) or next_running_index < 0:
                    break

                next_thread =  waiting_threads[next_running_index]
                #If next thread is not runned, run the next thread
                if not next_thread.is_alive():
                    next_thread.start()
                    # print(str(len(running_threads)) + ' **** ' + str(len(waiting_threads)) + ' ---- ' + str(waiting_threads[next_running_index]))
                    running_threads.append(waiting_threads[next_running_index])
                
                next_running_index = (next_running_index + 1) % len(waiting_threads)

        time.sleep(2.5)

def run_threads(database, max_thread_per_time = 4):
    waiting_threads = []
    running_threads = []
    next_running_index = 0

    #Get all threads list
    for web_thread_func in web_thread_func_list:
        thread = web_thread_func(database)
        waiting_threads = waiting_threads + thread

    check_running_thread_add_new(waiting_threads, running_threads, next_running_index, max_thread_per_time)
    
    #Redo the thread terminated by exception
    print("################### EXCEPTION THREAD RESTART ###############")
    for thread, arg_list in threads_status_dict.items():
        if arg_list[0] == -1:
            thread = threading.Thread(target=arg_list[1], args=(database, arg_list[2]))
            waiting_threads = waiting_threads + [thread]
    if len(waiting_threads) > 0:
        check_running_thread_add_new(waiting_threads, running_threads, next_running_index, max_thread_per_time)
    else:
        print('No exception found in the process!')

