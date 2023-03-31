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
    
    data_list = df.values.tolist()

    # Write the data to the sheet starting at cell A1
    sheet_instance.delete_rows(2, None)
    sheet_instance.update('A2', data_list)
    
    print(sheet.url)

