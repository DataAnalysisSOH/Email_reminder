# Import the required libraries
# (Your previous imports here)
# Import the require library
from __future__ import print_function
import pickletools
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from auth import spreadsheet_service
from auth import drive_service
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
# define the SCOPES
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

credentials = None

credentials = service_account.Credentials.from_service_account_file('./credential.json', scopes=SCOPES)

# We are define the require variable
EMAIL_SENDER =  os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER_NORMAL = os.getenv("EMAIL_RECEIVER_NORMAL")
EMAIL_RECEIVER_ERROR = os.getenv("EMAIL_RECEIVER_ERROR")
SUBJECT = "Daily report checking"
# defining the error message
ERROR_MESSAGE = "This is a heartbeat email to show report hasn't been refreshed normally."
NORMAL_MESSAGE = "Report refresh Time"



# Define the spreadsheet IDs and cell ranges
spreadsheet_ids = {
    "Direct_cost_withprofit": {'id': '1X_Tv7uoJodIrJ7r-7JpnMwew9-HrUxvFizAC4wXjf0w', 'range': "Direct_cost_withprofit!E2"},
    "Executive Dashboard": {'id': '190WGCo1GDuXRbvXnsLdiLEuOVQGb1mpDFIdNLh7KQRU', 'range': "Revenues!B1"},
    "SOH Email": {'id': '16wtqJqEvLJC3SI-h7aBcI-ek9sl1aHdIBqrrlyMc8z0', 'range': "YTD_QB_Report1!B3"},
    "AB Score": {'id': '1JnmgCojqc6o4f3qA36mZefNTtxaNaZ0ICVpTCfvHG2A', 'range': "Revenue Report_AB/PSM!B1"}
}

# Function to get specific cell value
def get_specific_cell_value(spreadsheet_id, cell_range):
    try:
        service = build('sheets', 'v4', credentials=credentials)
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=spreadsheet_id, range=cell_range).execute()
        values = result.get('values', [])
        return values[0][0] if values else None
    except Exception as e:
        print("An error occurred:", e)
        return None
    
def send_heartbeat_email(subject, message, sender_email, sender_password, receiver_email, refresh_time=None):
    # starting an try block
    try:
        msg = EmailMessage()
        msg['Subject'] = subject + (f" - Refresh Time: {refresh_time}" if refresh_time else "")
        msg['From'] = sender_email
        msg['To'] = ' '.join(receiver_email)
        msg.set_content(message)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)

        print("Heartbeat email sent successfully")
    except Exception as e:
        print("Error sending heartbeat email:", str(e))


# Function to check refresh and send email
def check_refresh_and_send_email(report_name, spreadsheet_id, cell_range):
    refresh_time_cell = get_specific_cell_value(spreadsheet_id, cell_range)
    if refresh_time_cell is not None:
        try:
            if report_name == "Direct_cost_withprofit" or report_name == "Executive Dashboard":
                refresh_time = datetime.datetime.strptime(refresh_time_cell, "%Y-%m-%d %H:%M:%S")
            elif report_name == "SOH Email":
                refresh_time = datetime.datetime.strptime(refresh_time_cell, "%m%d%Y")
            else:
                refresh_time = datetime.datetime.strptime(refresh_time_cell, "%Y-%m-%d %H:%M:%S")
            current_time = datetime.datetime.now()
        # if report_name == "Direct_cost_withprofit" or report_name == "Executive Dashboard":
        #     refresh_time = datetime.datetime.strftime(refresh_time, "%Y-%m-%d %H:%M:%S")
        # refresh_time = datetime.datetime.strptime(refresh_time_cell, "%Y-%m-%d %H:%M:%S" if report_name == "Direct_cost_withprofit" or report_name == "Executive Dashboard" else "%m/%d/%Y")
        # current_time = datetime.datetime.now()

            if current_time.date() > refresh_time.date():
                print(f"Refresh time hasn't changed for {report_name} for one day, sending the error Message")
                send_heartbeat_email(SUBJECT, ERROR_MESSAGE, EMAIL_SENDER, EMAIL_PASSWORD, [EMAIL_RECEIVER_ERROR, EMAIL_RECEIVER_NORMAL])
            else:
                print(f"Refresh Time: {refresh_time}, {report_name} last updated: {refresh_time}")
                normal_message = f"{NORMAL_MESSAGE}\nRefresh time: {refresh_time}"
                send_heartbeat_email(SUBJECT, normal_message, EMAIL_SENDER, EMAIL_PASSWORD, [EMAIL_RECEIVER_NORMAL], refresh_time=refresh_time)
        except ValueError as e:
            print(f"Error parsing datetime: {e}")
    else:
        print(f"No refresh datetime value is found for {report_name}")

# Schedule the function to run for each report
for report_name, config in spreadsheet_ids.items():
    schedule.every(0.1).minutes.do(check_refresh_and_send_email, report_name, config['id'], config['range'])

# Run the main loop to execute the scheduled tasks
while True:
    schedule.run_pending()
    time.sleep(1)

