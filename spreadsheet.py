from google.oauth2 import service_account
import gspread

# We are Loading the credentials from JSON keyfile
credentials = service_account.Credentials.from_service_account_file('C:\Users\yuqia\Documents\GitHub\Email-reminder\Email_reminder\credential.json')
client = gspread.authorize(credentials)

# We are Open a spreadsheet by its title
spreadsheet = client.open('Car_Donation_Version11')

# We are Access a specific worksheet within the spreadsheet
worksheet = spreadsheet.get_worksheet(0)

print(worksheet)