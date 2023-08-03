# step 1: importing the library
import smtplib, ssl
# defining the variabel
# taking care of the port
port = 465
smtp_server = "smtp.gmail.com"
sender_email = "lucy.wang@soundofhope.org"
receiver_email = "lucy.wang@soundofhope.org"
password = input("Wang233579762")
message = """
Subject: Testing email

This message is sent from Python for testinf purpose.
"""

# Create a secure SSL context
context = ssl._create_unverified_context()

# Taking care of the server
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    # we are login the server
    server.login(sender_email, password)
    # TODO: Send email here
    server.sendmail(sender_email,receiver_email,message)
