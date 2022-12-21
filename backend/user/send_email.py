import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.conf import settings

# port = 587
# smtp_server = "smtp.office365.com"
# sender = "owidikevin@outlook.com"
# sender_password = "@Letmein24/7."
# contentType="plain"

port = settings.EMAIL_PORT
smtp_server = settings.EMAIL_HOST
sender = settings.EMAIL_HOST_USER
sender_password = settings.EMAIL_HOST_PASSWORD
contentType= settings.CONTENT_TYPE


def send_mail(recipient,subject,message):

    print("Receipient")
    print(recipient)
    print("Subject")
    print(subject)
    print("Message")
    print(message)

    print("Connecting to server")

    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls()
        print("Loging in .....")
        server.login(sender, sender_password)
        print("Sending mail")

        mimemsg = MIMEMultipart()
        mimemsg["From"] = sender
        mimemsg["To"] = recipient
        mimemsg["Subject"] = subject
        mimemsg.attach(MIMEText(message, contentType))

        server.send_message(mimemsg)
        server.close()