from GoogleSheet import GoogleSheet
import phongVuScrapper
import cellphonesScraper

# spreadsheet_id = '1hLWC7ZgIkdN6JFHlzGCJrHEqmPnFUYugwFxx32sbb0o'

# cred_file = 'client_secret.json'

# categories_id = {
#     "Laptop" : 0,
#     "Desktop": 2008175367,
#     "LinhKien": 12846980,
#     "PhuKien": 398039562,
# }

spreadsheet_id = '1H5TTOdrTC_T7U7k_ejCUG8BZWn97NuaxD0t4F7LwH8g'
cred_file = 'client_secret.json'

categories_id = {
    "Laptop" : 679621757,
    "Desktop": 885273009,
    "LinhKien": 1480180086,
    "PhuKien": 1048996747,
}

ggsheet = GoogleSheet(spreadsheet_id, cred_file)
cellphonesScraper.scrape_all(ggsheet, categories_id)
print('Cellphones.com.vn has been scraped successfully!')