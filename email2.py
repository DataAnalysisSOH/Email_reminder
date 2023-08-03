# step 1: importing the library
import smtplib, ssl

# taking care of the port
port = 465
password = input("Wang233579762")
# Create a secure SSL context
context = ssl.create_unverified_context()

# Taking care of the server
with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    # we are login the server
    server.login("lucywang996688@gmail.com")
    # TODO: Send email here