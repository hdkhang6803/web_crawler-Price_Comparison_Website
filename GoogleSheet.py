from google.oauth2 import service_account
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

class GoogleSheet:
  categories_id = {
    "Laptop" : 679621757,
    "Desktop": 885273009,
    "LinhKien": 1480180086,
    "PhuKien": 1048996747,
  }

  def __init__(self, id, cred_file):
    self.id = id
    self.__creds = service_account.Credentials.from_service_account_file(cred_file, scopes= SCOPES)
    self.service = build('sheets', 'v4', credentials = self.__creds)

  def remove_duplicate(self, sheet_id = 0):
    batch_update_spreadsheet_request_body = {
      "requests": [
        {
          "deleteDuplicates": {
            "range": {
              "sheetId": sheet_id,
              "startColumnIndex": 0,
              "endColumnIndex": 4,
              "startRowIndex": 0,
              "endRowIndex": 5000
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

    request = self.service.spreadsheets().batchUpdate(spreadsheetId=self.id, body=batch_update_spreadsheet_request_body)
    response = request.execute()

  def update_with_data(self, data, sheetName = ""):
    value_range_body = {
      "majorDimension": "DIMENSION_UNSPECIFIED",
      "values": data 
    }
    request = self.service.spreadsheets().values().append(spreadsheetId=self.id, range= sheetName + "!A1", valueInputOption="RAW", body=value_range_body)
    response = request.execute()

  def get_data(self, rows_start, rows_end, cols, sheetName = ""):
    range = sheetName + "!R" + str(rows_start) + "C1:R" + str(rows_end) + "C" + str(cols)
    request = self.service.spreadsheets().values().get(spreadsheetId=self.id, range=range)
    response = request.execute()
    return response

  def get_data(self, rows_start, rows_end, cols, sheetName = ""):
    range = sheetName + "!R" + str(rows_start) + "C1:R" + str(rows_end) + "C" + str(cols)
    request = self.service.spreadsheets().values().get(spreadsheetId=self.id, range=range)
    response = request.execute()
    return response

  def sort_sheet_by_price(self, sheet_id, sheet_name):
    sheet_range = f"{sheet_name}!A2:A"
    result = self.service.spreadsheets().values().get(spreadsheetId=self.id, range=sheet_range).execute()
    end_row = len(result.get('values', []))

    # Create the sort request body
    sort_request_body = {
        "requests": [
            {
                "sortRange": {
                    "range": {
                        "sheetId": sheet_id,
                        "startRowIndex": 1,
                        "endRowIndex": end_row,
                        "startColumnIndex": 0,
                        "endColumnIndex": 4
                    },
                    "sortSpecs": [
                        {
                            "dimensionIndex": 1,  # Sort by the second column (price)
                            "sortOrder": "ASCENDING"
                        }
                    ]
                }
            }
        ]
    }

    # Execute the sort request
    request = self.service.spreadsheets().batchUpdate(spreadsheetId=self.id, body=sort_request_body)
    response = request.execute()
    print(f"Sheet '{sheet_name}' sorted by price.")


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
