import time
import smtplib
import logging
from email.message import EmailMessage

def send_heartbeat_email(subject, message, sender_email, sender_password, receiver_email):
    try:
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = ', '.join(receiver_email)
        msg.set_content(message)

        # Connect to the email server and send the email
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        
        print("Heartbeat email sent successfully.")
    except Exception as e:
        print("Error sending heartbeat email:", str(e))

if __name__ == "__main__":
    email_sender = input("Enter your email: ")
    email_password = input("Enter your email password: ")
    email_receiver = input("Enter receiver's email: ")
    
    subject = "Daily report checking"
    message = "This is a heartbeat email to confirm everything is running smoothly."
    
    heartbeat_interval = 3600
    
    try:
        while True:
            send_heartbeat_email(subject, message, email_sender, email_password, [email_receiver])
            time.sleep(heartbeat_interval)
    except KeyboardInterrupt:
        print("Heartbeat program stopped, attention needed")

    script_path = "Copy_car_donation.py"
    
    try:
        with open(script_path, "r") as script_file:
            script_code = script_file.read()
            exec(script_code)

        print("Script executed successfully")
    except Exception as e:
        error_message = f"Error in {script_path}: {str(e)}"
        logging.error(error_message)

        send_heartbeat_email("Error Notification", error_message, email_sender, email_password, [email_receiver])
