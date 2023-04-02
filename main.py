from GoogleSheet import GoogleSheet
import phongVuScrapper

spreadsheet_id = '1H5TTOdrTC_T7U7k_ejCUG8BZWn97NuaxD0t4F7LwH8g'
cred_file = 'client_secret.json'

categories_id = {
    "Laptop" : 679621757,
    "Desktop": 885273009,
    "LinhKien": 1480180086,
    "PhuKien": 1048996747,
}

if __name__ == "__main__":
    ggsheet = GoogleSheet(spreadsheet_id, cred_file)
    training_data = ggsheet.get_data(10, 4, "Laptop")

    # phongvudata = phongVuScrapper.getProduct("thinkpad")
    # # print(phongvudata)

    # # change category to update different product type sheet
    # category = "Laptop"
    # ggsheet.update_with_data(phongvudata, category)
    # ggsheet.remove_duplicate(categories_id[category])