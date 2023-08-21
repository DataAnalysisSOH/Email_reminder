# import the require library
from __future__ import print_function
import pickletools
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from auth import spreadsheet_service
from auth import drive_service
import datetime

SCOPES = [
'https://www.googleapis.com/auth/spreadsheets',
'https://www.googleapis.com/auth/drive'
]
credentials = None
# credentials = service_account.Credentials.from_service_account_file('/Users/zeyu/Desktop/credential.json', scopes=SCOPES)
credentials = service_account.Credentials.from_service_account_file('./credential.json', scopes=SCOPES)

# The ID spreadsheet.
spreadsheet_id = '1X_Tv7uoJodIrJ7r-7JpnMwew9-HrUxvFizAC4wXjf0w'
spreadsheet_service = build('sheets', 'v4', credentials=credentials)
# We are Calling the sheet API
sheet = spreadsheet_service.spreadsheets()
# We are Reading the refresh time from cell E2
refresh_time_cell = sheet.values().get(spreadsheetId=spreadsheet_id, range="Direct_cost_withprofit!E2").execute()

# getting the refresh time
refresh_time = datetime.datetime.strptime(refresh_time_cell, "%Y-%m-%d %H:%M:%S")
# defining the while loop
while True:
    current_time = datetime.datetime.now()
    time_until_refresh = (refresh_time - current_time).total_seconds()

    # checking whether the refresh date time is within one day
    if current_time.date() > refresh_time.date():
        print("Refresh time hasn't changed for one day. Sending the error message ")
    else:
        print("An error occured:", e)

# We are using getrequest to get infomration from the spreadsheet
# # Getting the specific cell values
# refresh_datetime= sheet.values().get(spreadsheetId=spreadsheet_id, range="Direct_cost_withprofit!E2").execute()
# # then we wish to Extracting the value from the result
# refresh_datetime_str = values[0][0] if values else None

# next, we are taking care of the if block
# if refresh_datetime:
#     refresh_datetime = datetime.datetime.strptime(refresh_datetime, '%Y-%m-%d %H:%M:%S')
#     # we are calculating the time difference between now and the refresh datetie
#     time_difference = datetime.datetime.now() - refresh_datetime
#     # next, we define another if block to check if the time difference is greater than 1
#     if time_difference.days > 1:
#         # we are sending an error message or perform necessary actions
#         print("Refresh datetime is not within one day. Sending error message...")
#         # sending the heartbeat email here
    
#     # defiing the else block
#     else:
#         print("The Refresh datetime is within one day.")

# otherwise
# else:
#     print("No refresh datetime value is found.")
#print(result)



#drive_service = build('drive', 'v3', credentials=credentials)

