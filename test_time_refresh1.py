# importing the require library
import time
import smtplib
import logging
import gspread
from gspread.exceptions import APIError
from oauth2client.service_account import ServiceAccountCredentials
#defining another function to get the specific cell_value
def get_specific_cell_value(worksheet, cell_address):
    try:
        cell_value = worksheet.acell(cell_address).value
        return cell_value
    #defining the except block
    except APIError as e:
        print("Google Sheets API error:", e)
    except Exception as e:
        print("An eror occurred:", e)
        return None
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

    # Taking care of the try block
    try:
        while True:
            send_heartbeat_email(subject,message,email_sender,email_password,email_receiver)
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

        # taking care of the Google Sheets credentials
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_key_file_name('C:\\Users\\yuqia\\Documents\\GitHub\\Email-reminder\\Email_reminder\\credential.json')
        client = gspread.authorize(creds)
        # We are Loading the Google Sheet
        spreadsheet = client.open("Car_Donation_Version11")
        worksheet = spreadsheet.worksheet("Direct_cost_withprofit")
        # we are checking the specific cell's value
        cell_value = get_specific_cell_value(worksheet, "E2")
        print(cell_value)

        # We are Load the Google sheet
        spreadsheet = client.open("Car_Donation_Version11")

    # taking care of the except block
    except Exception as e:
        error_message = f"Error in {script_path}:{str(e)}"
        # Log the error
        logging.error(error_message)

        # We are sending email with error message
        send_heartbeat_email("Error Notofication",error_message,email_sender,email_password,email_receiver)