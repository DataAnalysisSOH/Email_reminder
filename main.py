from google.oauth2 import service_account
from googleapiclient.discovery import build
# Create an variable to link to the client service file
SERVICE_ACCOUNT_FILE = 'Credential.json'
credentials=service_account.Credentials.from_service_account_file(
    filename = SERVICE_ACCOUNT_FILE,
    scopes = ['https://mail.google.com/'],
    subject = 'lucy.wang@soundofhope.org'
)

service_gmail = build('gmail','v1',credentials=credentials)
response=service_gmail.users().getProfile(userId='me').execute()
print(response)


# # Importing the require library
# import os
# from email.message import EmailMessage
# import ssl
# import smtplib
# # We are Initialized few variable for email senting
# email_sender = 'lucy.wang@soundofhope.org'
# email_password = os.environ.get("EMAIL_PASSWORD")
# email_receiver = 'lucy.wang@soundofhope.org'

# # defining the subject
# subject = 'Check out the email reminder'
# body = """
# Starting to test whether we are able to sent email successfully through python.
# """

# # declare EmailMessage object
# em = EmailMessage()
# em['From'] = email_sender
# em['To'] = email_receiver
# em['Subject'] = subject
# # We are taking care of the body
# em.set_content(body)

# # taking care of the security
# context = ssl.create_default_context()

# # using smtplib to sent the email
# with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
#     smtp.login(email_sender,email_password)
#     smtp.sentmail(email_sender,email_receiver,em.as_string())