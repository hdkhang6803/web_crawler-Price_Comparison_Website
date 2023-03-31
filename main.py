from GoogleSheet import GoogleSheet
import phongVuScrapper

spreadsheet_id = '1H5TTOdrTC_T7U7k_ejCUG8BZWn97NuaxD0t4F7LwH8g'
cred_file = 'client_secret.json'

ggsheet = GoogleSheet(spreadsheet_id, cred_file)

phongvudata = phongVuScrapper.getProduct("thinkpad")
# print(phongvudata)
ggsheet.update_with_data(phongvudata)
# ggsheet.remove_duplicate()