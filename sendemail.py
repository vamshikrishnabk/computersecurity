import smtplib
from email.message import EmailMessage
from email.utils import make_msgid
from pathlib import Path

smtp_server = 'smtp.gmail.com'  
smtp_port = 587  
smtp_username = 'untsegroup@gmail.com'  
smtp_password = 'rhwv dptm mxpi lriz' 



recipient_email = input("Enter email address ")

attachment_path = r'/home/sn1318/Downloads/unnamed.png'

email_message = EmailMessage()
email_message['From'] = smtp_username
email_message['To'] = recipient_email
email_message['Subject'] = 'Free Gift!!'
email_message.set_content('Thank you for participating in our monthly lottery. Please find the attached gift to claim your gift. You will need to click on the link to access the gift. \n https://drive.google.com/file/d/1Ij0U4cxOeuhhHXe0A3hd4quoJYsyjXFc/view') 

def attach_file_to_email(email_message, file_path):
    file_name = Path(file_path).name
    ctype = 'application/octet-stream'  
    maintype, subtype = ctype.split('/', 1)
    with open(file_path, 'rb') as fp:
        email_message.add_attachment(fp.read(), maintype=maintype, subtype=subtype, filename=file_name)

attach_file_to_email(email_message, attachment_path)

try:
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()  
        server.login(smtp_username, smtp_password)  
        server.send_message(email_message) 
        print('Email sent successfully!')
except Exception as e:
    print(f'An error occurred: {e}')
