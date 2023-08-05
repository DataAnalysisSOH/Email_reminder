# Importing the require library
import logging
import ssl
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

# doing an logging
logging.basicConfig(filename='error_log.txt',level=logging.ERROR),
format = '%(asctime)s - %(levelname)s - %(message)s'

# defining an function to send email
def send_email(subject, body):
    # taking care of the try block
    try:
         # Email configuration
        email_sender = 'lucy.wang@soundofhope.org'
        email_password = 'Wang233579762'
        email_receiver = 'lucy.wang@soundofhope.org'

        # taking care of the message variables
        msg = MIMEText(error_message,'plain','utf-8')
        msg['From'] = email_sender
        msg['To'] = email_receiver
        msg['Subject'] = Header(subject, 'utf-8').encode()
        # we are attaching to the main body
        #message.attach(MIMEText(body, 'plain'))

        # Set the plain text content of the email
        # plain_text = error_message
        # text_part = MIMEMultipart(plain_text, 'plain', 'utf-8')

        # # We are Attach the text part to the message
        # msg.attach(text_part)

        # Create a secure SSL context
        context = ssl.create_default_context()

        # Send the error email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
             smtp.login(email_sender,email_password)
             smtp.sendmail(email_sender, email_receiver, msg.as_string())
        print("Email sent successfully")
    except Exception as e:
         print("Failed to send error email:",e)
             

    # # taking care of the first try block
    # try:
    #     # taking care of the server
    #     server = smtplib.SMTP('smtp.example.com',587)
    #     server.starttls()
    #     server.login(send_email, password)
    #     # sending the email
    #     server.sendmail(sender_email,receiver_email,message.as_string())
    #     # make sure to quit the server
    #     server.quit()
    #     print("Email sent successfully")
    # except Exception as e:
    #     print("Failed to send email", str(e))


# taking care of the entry point of the program
if __name__ == "__main__":
      # get the path of the python script
    script_path = 'division_error.py'

      # taking care of the second try block:
    try:
           # We are Reading the content of the script file
            with open(script_path,'r') as script_file:
                script_code = script_file.read()

                # we are executing the script
                exec(script_code)
            # print out the scripts are running successfully
            print("Script executed successfully")
        # taking care of the excpetion block
    except Exception as e:
         error_message = f"Error in {script_path}: {str(e)}"
         # we are logging the error
         logging.error(error_message)
         # then, we are senting the email with the error message
         send_email("Error Notification", error_message)