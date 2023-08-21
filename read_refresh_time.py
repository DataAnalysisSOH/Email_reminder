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
EMAIL_SENDER = "lucy.wang@soundofhope.org"
EMAIL_PASSWORD = input("Enter your email password: ")
EMAIL_RECEIVER_NORMAL = "frank.lee@soundofhope.org"
EMAIL_RECEIVER_ERROR = "lucy.wang@soundofhope.org"
SUBJECT = "Heartbeat Check"
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
            print("The refresh datetime is within one day, sending normal heartbeat")
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
# we are reading the refresh datetime from an specific cells
#refresh_time_cell = get_specific_cell_value(sheet, "Direct_cost_withprofit!E2")

# We are Reading the refresh time from cell E2
#refresh_time_cell = sheet.values().get(spreadsheetId=spreadsheet_id, range="Direct_cost_withprofit!E2").execute()
#refresh_time_values = refresh_time_cell.get('value',[])
# turn the refresh time into string
#refresh_time_str = refresh_time_values[0][0] if refresh_time_values else None

# Defining the if block
# if refresh_time_cell:
#     refresh_time = datetime.datetime.strptime(refresh_time_cell, "%Y-%m-%d %H:%M:%S")
#     current_time = datetime.datetime.now()
#     time_until_refresh = (refresh_time - current_time).total_seconds()

#     # defining the if block
#     if current_time.date() > refresh_time.date():
#         print("Refresh time hasn't change for one day, sending the error Message")
#         # we are senting the heartbeat email
#         # defining the require variable
#         # Let the user input emai credentials and receiver's email
#         email_sender = input("Enter your email: ")
#         email_password = input("Enter your email password: ")
#         email_receiver = input("Enter receiver's email: ")
#         # taking care of subject
#         subject = "Heartbeat Check"
#         # taking care of the message
#         error_message = "This is a heartbeat email to show the report hasn't been refresh normally"
#         send_heartbeat_email("Error Notofication",error_message,email_sender,email_password,email_receiver)


#     #defining the else block
#     else:
#         print("The refresh datetime is within one day ")
# else:
#     print("No refresh datetime value is found")


# # getting the refresh time
# refresh_time = datetime.datetime.strptime(refresh_time_cell, "%Y-%m-%d %H:%M:%S")
# # defining the while loop
# while True:
#     current_time = datetime.datetime.now()
#     time_until_refresh = (refresh_time - current_time).total_seconds()

#     # checking whether the refresh date time is within one day
#     if current_time.date() > refresh_time.date():
#         print("Refresh time hasn't changed for one day. Sending the error message ")
#     else:
#         print("An error occured:")

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

