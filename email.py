# import the require library
import pandas as pd
from sendmail import send_email
# creating an dataframe
df = pd.read_csv('data.csv',engine='python')
list = []
for email in df.email:
    list.append(email)
print(list)
for mail in list:
    send_email(
        subject = "testing the automation",
        name = "lucy",
        receiver_email = mail,
    )
    print(f"email successfully sent to: {mail}")