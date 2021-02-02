import sys
import os
import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import tarfile
import zipfile

print(len(sys.argv[2]))


_, os_name, password = sys.argv


folder_name = os.path.realpath('./dist/qmlview/')

# Build archives
if os_name == 'windows-latest':
    # zip file
    filename = 'qmlview.zip'
    with zipfile.ZipFile(filename, 'w') as my_zip:
        my_zip.write(folder_name)

else:
    filename = 'qmlview.tar.gz'
    with tarfile.open(filename, 'w:gz') as my_tar:
        my_tar.add(folder_name)

print(f'filename: {filename}')

subject = f"Qmlview built {os} application"
body = f"The attachment contains a built application for Qmlview"
sender_email = "amohgyebigodwin@gmail.com"
receiver_email = "deutworks@gmail.com"

# Create a multipart message and set headers
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject
message["Bcc"] = receiver_email  # Recommended for mass emails

# Add body to email
message.attach(MIMEText(body, "plain"))

# Open PDF file in binary mode
with open(filename, "rb") as attachment:
    # Add file as application/octet-stream
    # Email client can usually download this automatically as attachment
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())

# Encode file in ASCII characters to send by email    
encoders.encode_base64(part)

# Add header as key/value pair to attachment part
part.add_header(
    "Content-Disposition",
    f"attachment; filename= {filename}",
)

# Add attachment to message and convert message to string
message.attach(part)
text = message.as_string()

# Log in to server using secure context and send email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, text)
