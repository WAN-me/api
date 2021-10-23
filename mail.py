import smtplib
import email.message
server = smtplib.SMTP('smtp.gmail.com:587')
 
email_content = """
"""
 
msg = email.message.Message()
msg.add_header('Content-Type', 'text/html')
msg.set_payload(email_content)
 
server = smtplib.SMTP('smtp.gmail.com: 587')
server.starttls()
 
# Login Credentials for sending the mail
server.login(msg['From'], password)
 

server.sendmail(msg['From'], [msg['To']], msg.as_string())