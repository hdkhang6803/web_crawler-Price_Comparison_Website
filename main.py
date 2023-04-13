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

if __name__ == "__main__":
    ggsheet = GoogleSheet(spreadsheet_id, cred_file)
    classifier = ProductClassifier(spreadsheet_id, cred_file)
    if (classifier.load_model()):
        print("model loaded succesfully yay")
        # print(classifier.predict("Laptop ASUS"))
    else:
        classifier.train_classifier()
        classifier.get_accuracy()
        # print(classifier.predict("Laptop ASUS"))
        classifier.save_model()
    searchEngine = SearchEngine(classifier= classifier, spreadsheet_id= spreadsheet_id, cred_file= cred_file,
                                brand_file= "brand_names.txt")
    result = searchEngine.search_product("laptop lenovo")
    for x in result:
        print(x)
    
    # hacomScraper.scrape_all(ggsheet)
    # hacomScraper.get_products_url('https://hacom.vn/linh-kien-may-tinh?page=25')
    # training_data = ggsheet.get_data(10, 4, "Laptop")

is_success = thread_.run_threads(ggsheet)
print('success: ' + str(is_success))
for cate in ['Laptop', 'Desktop', 'PhuKien', 'LinhKien']:
    ggsheet.sort_sheet_by_price(ggsheet.categories_id[cate], cate)

#Switch active status to the new crawled spreadsheet
# with open("active_spreadsheet.txt", "w") as file:
#     print('open f')
    # file.seek(0)
    # file.truncate()
    # file.write(str(ggsheet.spreadsheet_for_scrape))

if is_success == 1:
    print("Data fetching successfully")
else:
    print("Data failed")

# #SWITCH ACTIVE SPREADSHEET TO NEWLY CRAWLED SPREADSHEET HERE
print("Execute time: --- %s seconds ---" % (time.time() - start_time))




