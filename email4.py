# Importing the require library
import smtplib
import ssl
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

# doing an email configuration
email_sender = 'lucy.wang@soundofhope.org'
email_password = 'Wang233579762'
email_receiver = 'lucy.wang@soundofhope.org'
# We are Opening a plain text file for reading.
# the text file continas only ASCII characters

# # We are reading the content from the file
# file_path= 'C:/Users/yuqia/Documents/GitHub/Email-reminder/Email_reminder/textfile.txt'
# with open(file_path, 'rb') as fp:
#     # Adjust encoding
#     file_content = fp.read().decode('utf-8')
    

# We are Creating a MIMEText object
msg = MIMEMultipart()
msg['From'] = email_sender
msg['To'] = email_receiver
msg['Subject'] = Header('Subject of the Email','utf-8').encode()

# Set the plain text content of the email
plain_text = ' This is an testing email'
text_part = MIMEText(plain_text, 'plain','utf-8')
# Then, we are Attach file content
# body = MIMEMultipart(file_content, 'plain','utf-8')

# Attach the text part to the message
msg.attach(text_part)

# We are Creating a secure SSL context
context = ssl.create_default_context()

# Then, we are sending the email
with smtplib.SMTP_SSL('smtp.gmail.com', 465,context=context) as smtp:
    smtp.login(email_sender, email_password)
    smtp.sendmail(email_sender, email_receiver,msg.as_string())


# printing ot an message to show email are senting successfully
print("Email sent successfully")
# # We are senting the message using the own SMTP server, but don't include envelope header
# s = smtplib.SMTP('localhost')
# s.sendmail('lucy.wang@soundofhope.org','lucy.wang@soundofhope.org', msg.as_string())
# s.quit()