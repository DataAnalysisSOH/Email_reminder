# import the reuiqre library
import subprocess
import smtplib
from email.message import EmailMessage
import os
# Coming up with an Error checking function
def check_for_errors():
    # make an try block
    try:
        result=print(2/0)

        # Check for error messages in the result
        if "error" in result.stderr.lower():
            return result.stderr
        return None
    # taking care of the except block
    except subprocess.TimeoutExpired:
        return 'Timeout: The program took too long to execute.'
    
# defining another function to do Email sending
def send_email(subject, body):
    email_sender = 'lucy.wang@soundofhope.org'
    email_password = 'Wang233579762'
    email_receiver = 'lucy.wang@soundofhope.org'

    # Intialized an object for EmailMessage
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    # taking care of the context
    context = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    context.login(email_sender,email_password)
    context.send_message(em)
    context.quit()

# defining the main function
def main():
    # Checking for errors
    error_message = check_for_errors()

    # checking if there is error
    if error_message:
        # then, we are sending email if errors are detected
        subject = "Error Detected in Program"
        body = f"Error message:\n{error_message}"
        send_email(subject, body)
        print("Error detected. Email sent.")
    else:
        print("No errors detected.")


if __name__ == "__error_checking":
    main()
