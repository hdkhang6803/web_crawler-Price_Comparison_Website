from google.oauth2 import service_account
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']





def get_used_spreadsheet_name(cate_name, used_spreadsheet):
    sheet_name = cate_name
    if used_spreadsheet == 0:
        sheet_name = sheet_name + '_0'
    else:
        sheet_name = sheet_name + '_1'
    return sheet_name


class GoogleSheet:
    def get_row_num(self, sheet_name):
        sheet_range = f"{sheet_name}!A1:A"
        result = self.service.spreadsheets().values().get(
            spreadsheetId=self.id, range=sheet_range).execute()
        end_row = len(result.get('values', []))
        return end_row
    
    def switch_spreadsheet_id(self, used_spreadsheet):
        global categories_id
        if used_spreadsheet == 1:
            categories_id = {
                "Laptop": 679621757,
                "Desktop": 885273009,
                "LinhKien": 1480180086,
                "PhuKien": 1048996747,
            }
        else:
            categories_id = {
                "Laptop": 1701054025,
                "Desktop": 0,
                "LinhKien": 732831781,
                "PhuKien": 1913667635,
            }
        return categories_id

    def __init__(self, id, cred_file):
        self.id = id
        self.__creds = service_account.Credentials.from_service_account_file(
            cred_file, scopes=SCOPES)
        self.service = build('sheets', 'v4', credentials=self.__creds)

    def remove_duplicate(self, sheet_id=0):
        batch_update_spreadsheet_request_body = {
            "requests": [
                {
                    "deleteDuplicates": {
                        "range": {
                            "sheetId": sheet_id,
                            "startColumnIndex": 0,
                            "endColumnIndex": 4,
                            "startRowIndex": 0,
                            "endRowIndex": 2000
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

    def update_with_data(self, data, cate_name, used_spreadsheet):
        value_range_body = {
            "majorDimension": "DIMENSION_UNSPECIFIED",
            "values": data
        }

        sheetName = get_used_spreadsheet_name(cate_name, used_spreadsheet)

        request = self.service.spreadsheets().values().append(spreadsheetId=self.id,
                                                              range=sheetName + "!A1", valueInputOption="RAW", body=value_range_body)
        response = request.execute()

    def sort_sheet_by_price(self, sheet_id, cate_name, used_spreadsheet):
        sheet_name = get_used_spreadsheet_name(cate_name, used_spreadsheet)

        end_row = self.get_row_num(sheet_name)
        # print(end_row)

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

    def clear_sheets(self, used_spreadsheet):
        # Get sheet properties
        sheet_metadata = self.service.spreadsheets().get(spreadsheetId=self.id).execute()
        sheet_properties = sheet_metadata['sheets']
        
        sheet_name_to_del_list = ["Laptop", "Desktop", "LinhKien", "PhuKien"]
        global suffix 
        suffix = ""
        if used_spreadsheet == 0:
            suffix = "_0"
        else:
            suffix = "_1"
        sheet_name_to_del_list = [sheet_name + suffix for sheet_name in sheet_name_to_del_list]

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
# The ID and range of a sample spreadsheet.
# RANGE_NAME = 'A1:A10'


# # Call the Sheets API
# sheet = service.spreadsheets()
# result = sheet.values().get(spreadsheetId=spreadsheet_id,
#                             range=RANGE_NAME).execute()
# values = result.get('values', [])
# print(values)
# print(result)


# DEAD CODE DONT WANT TO DELETE
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials

# use creds to create a client to interact with the Google Drive API
# scope = ['https://www.googleapis.com/auth/spreadsheets']
# scope = [
#     'https://www.googleapis.com/auth/spreadsheets',
#     'https://www.googleapis.com/auth/drive'
# ]

# creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)


# if not values:
#     print('No data found.')

# print('Name, Major:')
# for row in values:
#     # Print columns A and E, which correspond to indices 0 and 4.
#     print('%s, %s' % (row[0], row[4]))
# client = gspread.authorize(creds)

# sheet = client.open("Product database").sheet1

# row = ["We","LOVE","COUPLER"]
# index = 1
# sheet.insert_row(row, index)
# sheet.insert_row(row, index+1)
