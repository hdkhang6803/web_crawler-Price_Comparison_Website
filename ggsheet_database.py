import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread.exceptions import SpreadsheetNotFound
import pandas as pd
import tgdd_scraper
import fpt_scraper

input_string = "laptop lenovo 3 ideapad"

# Set up the Google Sheets API credentials
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('sheet-auth.json', scope)
client = gspread.authorize(creds)

# Open the spreadsheet and select the worksheet
try:
    sheet = client.open('Product Information Sheet')
    sheet_instance = sheet.worksheet('Sheet1')
except SpreadsheetNotFound:
    sheet = client.create('Product Information Sheet') 



# Create a pandas DataFrame to store the product information
data = fpt_scraper.get_list(input_string)
df = pd.DataFrame(data)
print(df)

# Write the DataFrame to the Google Sheet
sheet_instance.update([df.columns.values.tolist()] + df.values.tolist())
