import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Authenticate with Google Drive API using a service account
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('sheet-auth.json', scope)
client = gspread.authorize(creds)

# Open the sheet and select the first worksheet
sheet_url = 'https://docs.google.com/spreadsheets/d/13X7JfitUrqihFo1SgibqGDOqgKbWNhsAGLv9sghCDeQ'
sheet = client.open_by_url(sheet_url).sheet1

# Get all the data in the sheet
data = sheet.get_all_records()

# for i in range(1, len(data)):
#     data[i][1] = int(data[i][1])

# sort the data by price in ascending order
# sorted_data = sorted(data, key=lambda x: int(''.join(filter(str.isdigit, x['price']))))
sorted_data = sorted(data, key=lambda x: x['price'])

# print out the data in the sorted order
for item in sorted_data:
    print('Name:', item['name'])
    print('Price:', item['price'])
    print('Link:', item['link'])
    print('-----------------------')
