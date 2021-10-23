from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import email.message
import smtplib
def send(mail,content,subscription=""):
 
    msg = email.message.Message()
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(content)
    # setup the parameters of the message
    password = "Silniyparol1"
    msg['From'] = "ashcarev@gmail.com"
    msg['To'] = mail
    msg['Subject'] = subscription
    

    #create server
    server = smtplib.SMTP('smtp.gmail.com: 587')
    
    server.starttls()
    
    # Login Credentials for sending the mail
    server.login(msg['From'], password)
    
    
    # send the message via the server.
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    
    server.quit()
    
    return True
if __name__ == "__main__":
    send("wex335@yandex.ru",'''Hello, world''')