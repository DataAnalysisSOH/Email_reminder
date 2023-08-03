# Importing library
import smtplib, ssl

port =465
smtp_server = "smtp.gmail.com"
#smtp_server = "localhost"
sender_email = "lucy.wang@soundofhope.org"
receiver_email = "lucy.wang@soundofhope.org"
password = input("Type your password and press enter:")
message = """\
Subject: Hi there

This message is sent from Python."""

context = ssl.create_default_context()
with smtplib.SMTP(smtp_server, port) as server:
    server.ehlo()
    server.starttls(context=context)
    server.ehlo()
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email,message)