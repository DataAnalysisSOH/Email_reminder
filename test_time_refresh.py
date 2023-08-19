# importing the require library
import time
import smtplib
import logging
# import the library for delaing google sheet
import gspread

from oauth2client.service_account import ServiceAccountCredentials

# Defining the Google Sheets credentials file path
credentials_file_path = 'C:\\Users\\yuqia\\Documents\\GitHub\\Email-reminder\\Email_reminder\\credential.json'


# Define the specific cell to check for refresh time
refresh_cell = 'C1:D1'

# We are Loading the Google Sheets credentials
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_file_path,scope)
client = gspread.authorize(credentials)

# We also need to define another function get the content of the specific cell
def get_cell_content(sheet_id, cell):
    sheet = client.open_by_key(sheet_id).sheet1
    # defining the cell value
    cell_value = sheet.acell(cell).value
    return cell_value

# creating an function to send_heartbeat_email
def send_heartbeat_email(subject, message, sender_email, sender_password, receiver_email):
    # taking care of the try block
    try:
        # taking care of the server connection
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            # we are login the server
            server.login(sender_email, sender_password)
            email_message = f"Subject {subject}\n\n{message}"
            server.sendmail(sender_email,receiver_email, email_message)
        print("Heartbeat email sent successfully.")
    # take care of the Exceptions
    except Exception as e:
        print("Error sending heartbeat email",str(e))



# the entry point of the function
if __name__ == "__main__":
    # We are Loading the Credentials from JSON keyfile
    with open(credentials_file_path, 'r') as credentials_file:
        credentials_data = json.load(credentials_file)

    credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_data, scope)
    # Let the user input emai credentials and receiver's email
    email_sender = input("Enter your email: ")
    email_password = input("Enter your email password: ")
    email_receiver = input("Enter receiver's email: ")
    # taking care of subject
    subject = "Heartbeat Check"
    # taking care of the message
    message = "This is a heartbeat email to confirm everything is running smoothly."

    # We are setting the interval (in seconds) between heartbeat emails
    heartbeat_interval = 3600 # we are checking whether senting it every hour

    # We are Initialize error message
    error_message = ""

    # Get the path of the Python script
    #script_path = "division_error.py"
    # checking the car donation report
    script_path = "Copy_car_donation.py"
    
    # defining the spreadsheet_id 
    spreadsheet_Id = "1X_Tv7uoJodIrJ7r-7JpnMwew9-HrUxvFizAC4wXjf0w"
    # Taking care of the try block
    try:
        while True:
            # We are Getting the refresh time from specificed cell
            refresh_time = get_cell_content(spreadsheet_Id, refresh_cell)
            # We are Compare the refresh time with the curent time
            current_time = time.strftime("%Y-%m-%dT%H:%M:%SZ")
            # we are starting the if block
            if refresh_time != current_time:
                # defining the error message
                error_message = f"Report not refreshed. Last refresh time: {refresh_time}"
                # if there is en error, we need to make sure to sent the heartbeat email
                send_heartbeat_email("Error Notification",subject,message,email_sender,email_password,email_receiver)
                # We are Logging the error
                logging.error(error_message)

            
            time.sleep(heartbeat_interval)
    # taking care of the excpet block
    except KeyboardInterrupt:
        print("Heartbeat program stopped, attention needed")

    # taking care of another try block
    try:
        # We are Readin the content of the scripts
        with open(script_path, "r") as script_file:
            script_code = script_file.read()

            # We are Execute the script
            exec(script_code)

        # Print a success message
        print("Script executed successfully")
    # taking care of the except block
    except Exception as e:
        error_message = f"Error in {script_path}:{str(e)}"
        # Log the error
        logging.error(error_message)

        # We are sending email with error message
        send_heartbeat_email("Error Notofication",error_message,email_sender,email_password,email_receiver)