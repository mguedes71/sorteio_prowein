import smtplib
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication



def send_mail (sender, password, receiver, smtp_server, smtp_port, email_message, subject, attachment = None):

    message = MIMEMultipart()
    message['To'] = Header(receiver)    
    message['From'] = Header(sender)    
    message['Subject'] = Header(subject)
    message.attach(MIMEText(email_message, 'plain', 'utf-8'))

    if attachment:
        att = MIMEApplication(attachment.read(), _subtype="txt")
        att.add_header('Content-Disposition', 'attachment', filename = attachment.name)
        message.attach(att)

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.ehlo()
    server.login(sender, password)
    text = message.as_string()
    server.sendmail(sender, receiver, text)
    server.quit()


extra_info = """"

---------------------------------------------
Email Address of sender {} \n

Sender Full Name {} \n

---------------------------------------------

""".format(email, fullname)

message = extra_info + text
st.write("SENDER_ADDRESS", SENDER_ADDRESS)
st.write("SMTP_SERVER_ADDRESS", SMTP_SERVER_ADDRESS)
st.write("SMTP_SERVER_PORT", SMTP_SERVER_PORT)

send_email(sender=SENDER_ADDRESS, password=SENDER_PASSWORD, receiver=email, smtp_server=SMTP_SERVER_ADDRESS, smtp_port=SMTP_SERVER_PORT, email_message=message, subject=subject, attachment=uploaded_file)