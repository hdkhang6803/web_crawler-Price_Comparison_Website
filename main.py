from GoogleSheet import GoogleSheet
import phongVuScrapper
import Scraper.fpt_scraper as fpt

spreadsheet_id = '1H5TTOdrTC_T7U7k_ejCUG8BZWn97NuaxD0t4F7LwH8g'
cred_file = 'client_secret.json'

ggsheet = GoogleSheet(spreadsheet_id, cred_file)

# phongvudata = phongVuScrapper.getProduct("thinkpad")
fptdata = fpt.get_list("laptop")

# print(phongvudata)
ggsheet.update_with_data(fptdata)
ggsheet.remove_duplicate()