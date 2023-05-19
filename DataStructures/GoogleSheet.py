from google.oauth2 import service_account
# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def get_sheet_for_scrape():
    with open("active_spreadsheet.txt", "r+") as file:
        active_spreadsheet = file.read()
        used_spreadsheet =  int(not(int(active_spreadsheet, base=2)))
        return used_spreadsheet      
    
def get_active_sheet():
    with open("active_spreadsheet.txt", "r+") as file:
        active_spreadsheet = file.read()
        active_spreadsheet =  int(active_spreadsheet, base=2)
        return active_spreadsheet

class GoogleSheet:
    
    categories_id = {
        "Laptop": 679621757,
        "Desktop": 885273009,
        "LinhKien": 1480180086,
        "PhuKien": 1048996747,
    }

    def __init__(self, id, cred_file):
        self.id = id
        self.__creds = service_account.Credentials.from_service_account_file(
            cred_file, scopes=SCOPES)
        self.service = build('sheets', 'v4', credentials=self.__creds)

        self.spreadsheet_for_scrape = get_sheet_for_scrape()
        self.switch_sheet_id(self.spreadsheet_for_scrape)

    def get_row_num(self, sheet_name):
        sheet_range = f"{sheet_name}!A1:A"
        result = self.service.spreadsheets().values().get(
            spreadsheetId=self.id, range=sheet_range).execute()
        end_row = len(result.get('values', []))
        return end_row
    
    def get_used_spreadsheet_name(self, category):
        self.spreadsheet_for_scrape = get_sheet_for_scrape()
        sheet_name = category
        if self.spreadsheet_for_scrape == 0:
            sheet_name = sheet_name + '_0'
        else:
            sheet_name = sheet_name + '_1'
        return sheet_name
            
    def switch_sheet_id(self, used_spreadsheet):
        if used_spreadsheet == 1:
            self.categories_id = {
                "Laptop": 679621757,
                "Desktop": 885273009,
                "LinhKien": 1480180086,
                "PhuKien": 1048996747,
            }
        else:
            self.categories_id = {
                "Laptop": 1701054025,
                "Desktop": 0,
                "LinhKien": 732831781,
                "PhuKien": 1913667635,
            }
        return self.categories_id

    def get_id_of_cate(self, category):
        return self.categories_id[category]

    def remove_duplicate(self, category):
        end_row = self.get_row_num(self.get_used_spreadsheet_name(category))
        # print(end_row)
        sheet_id = self.get_id_of_cate(category)
        batch_update_spreadsheet_request_body = {
            "requests": [
                {
                    "deleteDuplicates": {
                        "range": {
                            "sheetId": sheet_id,
                            "startColumnIndex": 0,
                            "endColumnIndex": 4,
                            "startRowIndex": 0,
                            "endRowIndex": end_row
                        },
                        "comparisonColumns": [
                            {
                                "sheetId": sheet_id,
                                "dimension": "COLUMNS",
                                "startIndex": 0,
                                "endIndex": 3
                            }
                        ]
                    }
                }
            ]
        }

        request = self.service.spreadsheets().batchUpdate(
            spreadsheetId=self.id, body=batch_update_spreadsheet_request_body)
        response = request.execute()

    def update_with_data(self, data, category):
        value_range_body = {
            "majorDimension": "ROWS",
            "values": data
        }

        sheetName = self.get_used_spreadsheet_name(category)

        request = self.service.spreadsheets().values().append(spreadsheetId=self.id,
                                                              range=sheetName + "!A1", valueInputOption="RAW", body=value_range_body)
        response = request.execute()

    def get_data(self, rows_start, rows_end, cols, category = ""):
        sheetName = self.get_used_spreadsheet_name(category)

        range = sheetName + "!R" + str(rows_start) + "C1:R" + str(rows_end) + "C" + str(cols)
        request = self.service.spreadsheets().values().get(spreadsheetId=self.id, range=range)
        response = request.execute()
        return response

    def sort_sheet_by_price(self, sheet_id, category):
        sheet_name = self.get_used_spreadsheet_name(category)
        sheet_range = f"{sheet_name}!A1:A"
        result = self.service.spreadsheets().values().get(spreadsheetId=self.id, range=sheet_range).execute()
        end_row = len(result.get('values', []))

        # Create the sort request body
        sort_request_body = {
            "requests": [
                {
                    "sortRange": {
                        "range": {
                            "sheetId": sheet_id,
                            "startRowIndex": 0,
                            "endRowIndex": end_row,
                            "startColumnIndex": 0,
                            "endColumnIndex": 4
                        },
                        "sortSpecs": [
                            {
                                # Sort by the second column (price)
                                "dimensionIndex": 1,
                                "sortOrder": "ASCENDING"
                            }
                        ]
                    }
                }
            ]
        }

        # Execute the sort request
        request = self.service.spreadsheets().batchUpdate(
            spreadsheetId=self.id, body=sort_request_body)
        response = request.execute()
        print(f"Sheet '{sheet_name}' sorted by price.")

    def clear_sheets(self):
        # Get sheet properties
        sheet_metadata = self.service.spreadsheets().get(spreadsheetId=self.id).execute()
        sheet_properties = sheet_metadata['sheets']
        
        sheet_name_to_del_list = list(self.categories_id.keys())
        
        sheet_name_to_del_list = [self.get_used_spreadsheet_name(sheet_name) for sheet_name in sheet_name_to_del_list]

        # Loop through all sheets and clear values
        for sheet in sheet_properties:
            sheet_id = sheet['properties']['sheetId']
            sheet_name = sheet['properties']['title']

            # Skip sheets that are not named Laptop, Desktop, LinhKien, or PhuKien
            if sheet_name not in sheet_name_to_del_list:
                continue

            try:
                self.service.spreadsheets().values().clear(
                    spreadsheetId=self.id,
                    range=sheet_name
                ).execute()
                print(f"Cleared values in sheet {sheet_name} (id {sheet_id})")
            except HttpError as e:
                print(
                    f"Error clearing values in sheet {sheet_name} (id {sheet_id}): {e}")