from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import smtplib
import os

def ErrorEmail(error):
    load_dotenv()

    server = smtplib.SMTP(os.environ.get("SMTP_SERVER"))
    server.connect(os.environ.get("SMTP_SERVER"))
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(os.environ.get("SEND_FROM"), os.environ.get("EMAIL_PASSWORD"))
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Builder Trend Error"
    msg['From'] = os.environ.get("SEND_FROM")

    recipients = ['ahoward@visionaryhomes.com']
    msg['To'] = ",".join(recipients)

    html = '<p>' + error + '</p>'
    attatchableHTML = MIMEText(html, 'html')

    msg.attach(attatchableHTML)
    
    server.sendmail(os.environ.get("SEND_FROM"), recipients, msg.as_string())
    server.quit()