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
import smtplib
from email.message import EmailMessage

load_dotenv()
SCOPES = [
'https://www.googleapis.com/auth/spreadsheets',
'https://www.googleapis.com/auth/drive'
]
credentials = None
# credentials = service_account.Credentials.from_service_account_file('/Users/zeyu/Desktop/credential.json', scopes=SCOPES)
credentials = service_account.Credentials.from_service_account_file('./credential.json', scopes=SCOPES)

# The ID spreadsheet.
spreadsheet_id = '190WGCo1GDuXRbvXnsLdiLEuOVQGb1mpDFIdNLh7KQRU'
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
NORMAL_MESSAGE = "Executive dashboard refresh Time"

def get_specific_cell_value(worksheet, cell_address):
    try:
        result = worksheet.values().get(spreadsheetId=spreadsheet_id, range=cell_address).execute()
        values = result.get('values', [])
        return values[0][0] if values else None
    except Exception as e:
        print("An error occurred:", e)
        return None

def send_heartbeat_email(subject, message, sender_email, sender_password, receiver_email,refresh_time=None):
    try:
        msg = EmailMessage()
        msg['Subject'] = subject + (f" - Refresh Time: {refresh_time}" if refresh_time else "")
        msg['From'] = sender_email
        msg['To'] = ', '.join(receiver_email)
        msg.set_content(message)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)

        print("Heartbeat email sent successfully")
    except Exception as e:
        print("Error sending heartbeat email:", str(e))

# Define a list of dictionaries with sheet id
sheet_info_list = [
    {"id": ""}
]

# We wish to check the refresh datetime through functions
# report_cells = [
#     {"worksheet": "Direct_cost_withprofit", "cell_address": "E2", "receiver": [EMAIL_RECEIVER_ERROR, EMAIL_RECEIVER_NORMAL]},
#     {"worksheet": "Revenue Report_AB", "cell_address": "B1", "receiver": [EMAIL_RECEIVER_ERROR, EMAIL_RECEIVER_NORMAL]},
#     {"worksheet": "Direct_cost_withprofit", "cell_address": "E2", "receiver":[EMAIL_RECEIVER_ERROR, EMAIL_RECEIVER_NORMAL]}
# ]
sheet_info_list = [
    {"id": "1X_Tv7uoJodIrJ7r-7JpnMwew9-HrUxvFizAC4wXjf0w", "worksheet": "Operation Summary", "cell_address": "C1", "receiver": [EMAIL_RECEIVER_ERROR, EMAIL_RECEIVER_NORMAL],"Report_name":"Car_Donation_Report"},
    {"id": "190WGCo1GDuXRbvXnsLdiLEuOVQGb1mpDFIdNLh7KQRU", "worksheet": "Revenues", "cell_address": "B1", "receiver": [EMAIL_RECEIVER_ERROR, EMAIL_RECEIVER_NORMAL],"Report_name":"Executive Dashboard"},
    {"id": "1MgQAUtQ64SXZXHg1CGdmo-uoHqWitHzynXCKCpB1RkQ","worksheet": "Revenue Report_AB", "cell_address": "B1", "receiver": [EMAIL_RECEIVER_ERROR, EMAIL_RECEIVER_NORMAL],"Report_name":"ScoreCard_AB_n_PSM"},
    {"id": "1KcuyAWpf4z5KilEOUNmr0g9KbHn5PnV1JCSy12cImhY","worksheet": "Email List", "cell_address": "A1", "receiver": [EMAIL_RECEIVER_ERROR, EMAIL_RECEIVER_NORMAL],"Report_name": "SOH-email-subscribers"}

    # Add more sheet information here
]

    

def check_refresh_and_send_email(sheet_id, worksheet_name, cell_address, receiver, Report_name):
    # Use the provided sheet_id to access the specific spreadsheet
    spreadsheet_service = build('sheets', 'v4', credentials=credentials)
    sheet = spreadsheet_service.spreadsheets()
    
    refresh_time_cell = get_specific_cell_value(sheet, f"{worksheet_name}!{cell_address}")
    
    if refresh_time_cell:
        refresh_time = datetime.datetime.strptime(refresh_time_cell, "%Y-%m-%d %H:%M:%S")
        current_time = datetime.datetime.now()
        
        if current_time.date() > refresh_time.date():
            print(f"Refresh time for {worksheet_name} hasn't changed for one day, sending the error message")
            send_heartbeat_email(SUBJECT, ERROR_MESSAGE, EMAIL_SENDER, EMAIL_PASSWORD, receiver)
        else:
            print(f"Refresh Time for {worksheet_name}: {refresh_time}, {Report_name} last updated: {refresh_time}")
            normal_message = f"{NORMAL_MESSAGE} for {worksheet_name}\nRefresh time: {refresh_time}"
            send_heartbeat_email(SUBJECT, normal_message, EMAIL_SENDER, EMAIL_PASSWORD, receiver, refresh_time=refresh_time)
    else:
        print(f"No refresh datetime value is found for {worksheet_name}")

    


    # refresh_time_cell = get_specific_cell_value(sheet, "Direct_cost_withprofit!E2")
    
     
    # # defining the if block
    # if refresh_time_cell:
    #     refresh_time = datetime.datetime.strptime(refresh_time_cell, "%Y-%m-%d %H:%M:%S")
    #     # getting the current time
    #     current_time = datetime.datetime.now()

    #     if current_time.date() > refresh_time.date():
    #         print("Refresh time hasn't changed for one day, sending the error Message")
    #         send_heartbeat_email(SUBJECT,ERROR_MESSAGE, EMAIL_SENDER,EMAIL_PASSWORD, [EMAIL_RECEIVER_ERROR, EMAIL_RECEIVER_NORMAL])
    #     #defining the else block
    #     else:
    #         #print("The refresh datetime is within one day, sending normal heartbeat")
    #         print("Refresh Time:",refresh_time,"Executive Dashboard last updated:",refresh_time)
    #         normal_message = f"{NORMAL_MESSAGE}\nRefresh time: {refresh_time}"
    #         send_heartbeat_email(SUBJECT, normal_message, EMAIL_SENDER, EMAIL_PASSWORD, [EMAIL_RECEIVER_NORMAL], refresh_time=refresh_time)
    # # defining the else block
    # else:
    #     print("No refresh datetime value is found")

# then we are schedule the function to run daily at 12:20
#schedule.every().day.at("12:20").do(check_refresh_and_send_email)
# However, for testing purpose, need to do using one seconds

# We are Iterate through the list of sheet information
for sheet_info in sheet_info_list:
    check_refresh_and_send_email(
        sheet_info["id"],
        sheet_info["worksheet"],
        sheet_info["cell_address"],
        sheet_info["receiver"],
        sheet_info["Report_name"]

    )
schedule.every(0.1).minutes.do(check_refresh_and_send_email)


# then we are defining the Main loop to run the scheduled tasks
while True:
    schedule.run_pending()
    time.sleep(1)
