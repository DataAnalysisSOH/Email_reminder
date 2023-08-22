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
from datetime import date, timedelta
import time
import schedule
from heartbeat_email1 import send_heartbeat_email
from dotenv import load_dotenv
import os

load_dotenv()
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
# We are defining an function to get the specific cell value

# We are define the require variable
EMAIL_SENDER =  os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER_NORMAL = os.getenv("EMAIL_RECEIVER_NORMAL")
EMAIL_RECEIVER_ERROR = os.getenv("EMAIL_RECEIVER_ERROR")
SUBJECT = "Daily report checking"
# defining the error message
ERROR_MESSAGE = "This is a heartbeat email to show report hasn't been refreshed normally."
NORMAL_MESSAGE = "Everything is running smoothly"

def get_specific_cell_value(worksheet, cell_address):
    try:
        result = worksheet.values().get(spreadsheetId=spreadsheet_id, range=cell_address).execute()
        values = result.get('values', [])
        return values[0][0] if values else None
    except Exception as e:
        print("An error occurred:", e)
        return None

# We wish to check the refresh datetime through functions
def check_refresh_and_send_email():
    refresh_time_cell = get_specific_cell_value(sheet, "Direct_cost_withprofit!E2")
     
    # defining the if block
    if refresh_time_cell:
        refresh_time = datetime.datetime.strptime(refresh_time_cell, "%Y-%m-%d %H:%M:%S")
        # getting the current time
        current_time = datetime.datetime.now()

        if current_time.date() > refresh_time.date():
            print("Refresh time hasn't changed for one day, sending the error Message")
            send_heartbeat_email(SUBJECT,ERROR_MESSAGE, EMAIL_SENDER,EMAIL_PASSWORD, [EMAIL_RECEIVER_ERROR, EMAIL_RECEIVER_NORMAL])
        #defining the else block
        else:
            #print("The refresh datetime is within one day, sending normal heartbeat")
            print("Car Donation Report last updated:",refresh_time)
            send_heartbeat_email(SUBJECT, NORMAL_MESSAGE, EMAIL_SENDER, EMAIL_PASSWORD, [EMAIL_RECEIVER_NORMAL])
    # defining the else block
    else:
        print("No refresh datetime value is found")

# then we are schedule the function to run daily at 12:20
#schedule.every().day.at("12:20").do(check_refresh_and_send_email)
# However, for testing purpose, need to do using one seconds
schedule.every(0.1).minutes.do(check_refresh_and_send_email)


# then we are defining the Main loop to run the scheduled tasks
while True:
    schedule.run_pending()
    time.sleep(1)

