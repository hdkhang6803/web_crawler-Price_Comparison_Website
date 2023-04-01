from google.oauth2 import service_account
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

class GoogleSheet:
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
              "endColumnIndex": 3,
              "startRowIndex": 0,
              "endRowIndex": 100
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

  def update_with_data(self, data, sheet_id = 0):
    value_range_body = {
      "majorDimension": "DIMENSION_UNSPECIFIED",
      "values": data 
    }
    request = self.service.spreadsheets().values().append(spreadsheetId=self.id, range= "A1", valueInputOption="RAW", body=value_range_body)
    response = request.execute()



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
