import gspread
from oauth2client.service_account import ServiceAccountCredentials

def store_in_db(df):

    # Set up the Google Sheets API credentials
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('sheet-auth.json', scope)
    client = gspread.authorize(creds)

    # Open the spreadsheet and select the worksheet
    sheet = client.open('Product Information Sheet')
    sheet_instance = sheet.worksheet('Sheet1')

    # print(df)

    # Append the new rows to the Google Sheet
    sheet_instance.append_rows(df.values.tolist())
    print(sheet.url)
