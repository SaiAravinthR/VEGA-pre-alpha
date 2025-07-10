import smtplib
import os
from email.mime.text import MIMEText

msg = MIMEText("Hello from test script.")
msg['Subject'] = "Test Email"
msg['From'] = os.getenv("GMAIL_USER")
msg['To'] = "recipient@example.com"

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(os.getenv("GMAIL_USER"), os.getenv("GMAIL_APP_PASSWORD"))
server.sendmail(msg['From'], [msg['To']], msg.as_string())
server.quit()
