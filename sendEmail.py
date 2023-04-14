import smtplib,ssl
import os
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email import encoders
import pandas as pd


df = pd.read_csv('data.csv')
# print(df)

Sender = "******@gmail.com"
password = "*********"

filename = "attachment.pdf"
with open(filename,'rb') as attachement:
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachement.read())
    encoders.encode_base64(part)
        # file_attachement = MIMEApplication(attachement.read())
    part.add_header(
            "Content-Disposition",
            f"attachment; filename= {filename}",
        )
    print(encoders)
                
def send_mail(to, subject , body):
    msg = MIMEMultipart()
    msg['From'] = Sender
    msg['To'] = to
    msg['subject'] = subject
    msg.attach(MIMEText(body, "plain"))
    msg.attach(part)

    context = ssl.create_default_context()
    text = msg.as_string()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465,context=context) as server:
        server.login(Sender,password)
        server.sendmail(Sender,to,text)
Sent = 0

for index,row in df.iterrows():
    if Sent >4:
        break
  
    if type(row['Sent'])==float:
        to = row['Email']
        subject = "mail sent From csv"
        body = f"Hello {row['Name']} You Are Living At {row['Address']}"
        send_mail(to, subject,body)
        df.at[index, 'Sent'] = True
        print('mail sent')
        Sent+=1

    else:
        print("email already sent")
        Sent = 0

df.to_csv('data.csv' , index = False)

