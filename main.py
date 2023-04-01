from GoogleSheet import GoogleSheet
import phongVuScrapper
import Scraper.fpt_scraper as fpt

spreadsheet_id = '1H5TTOdrTC_T7U7k_ejCUG8BZWn97NuaxD0t4F7LwH8g'
cred_file = 'client_secret.json'

categories_id = {
    "Laptop" : 679621757,
    "Desktop": 885273009,
    "LinhKien": 1480180086,
    "PhuKien": 1048996747,
}

ggsheet = GoogleSheet(spreadsheet_id, cred_file)

# phongvudata = phongVuScrapper.getProduct("thinkpad")
fptdata = fpt.get_list("laptop")

# print(phongvudata)
<<<<<<< HEAD

# change category to update different product type sheet
category = "Laptop"
ggsheet.update_with_data(phongvudata, category)
ggsheet.remove_duplicate(categories_id[category])
=======
ggsheet.update_with_data(fptdata)
ggsheet.remove_duplicate()
>>>>>>> 1bade77d0e98d1283c4585f5fb61df633d39c201
