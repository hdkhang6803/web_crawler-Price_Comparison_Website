from DataStructures.GoogleSheet import GoogleSheet
import multi_thread as thread_
import time


start_time = time.time()

spreadsheet_id = '1H5TTOdrTC_T7U7k_ejCUG8BZWn97NuaxD0t4F7LwH8g'
cred_file = 'client_secret.json'
ggsheet = GoogleSheet(spreadsheet_id, cred_file)

ggsheet.clear_sheets(ggsheet.spreadsheet_for_scrape)

is_success = thread_.run_threads(ggsheet)
for cate in ['Laptop', 'Desktop', 'PhuKien', 'LinhKien']:
    ggsheet.remove_duplicate(cate)
    ggsheet.sort_sheet_by_price(ggsheet.categories_id[cate], cate)

    training_data = ggsheet.get_data(10, 4, "Laptop")

is_success = thread_.run_threads(ggsheet)
print('success: ' + str(is_success))
for cate in ['Laptop', 'Desktop', 'PhuKien', 'LinhKien']:
    ggsheet.sort_sheet_by_price(ggsheet.categories_id[cate], cate)

# Switch active status to the new crawled spreadsheet
with open("active_spreadsheet.txt", "w") as file:
    print('open f')
    file.seek(0)
    file.truncate()
    file.write(str(ggsheet.spreadsheet_for_scrape))

if is_success == 1:
    print("Data fetching successfully")
else:
    print("Data failed")

# #SWITCH ACTIVE SPREADSHEET TO NEWLY CRAWLED SPREADSHEET HERE
print("Execute time: --- %s seconds ---" % (time.time() - start_time))




