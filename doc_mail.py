import smtplib,ssl
import math,random
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
def mail():
    #context = ssl.create_default_context()
    msg = MIMEMultipart() 
  
    server=smtplib.SMTP_SSL('smtp.gmail.com', 465)
   
    server.login("crescent1070@gmail.com","crescent@17")

    #msg = EmailMessage()
    msg['Subject'] = 'Appointment Details'
    msg['From'] = 'Do well healthcare'
    msg['To'] = 'heyimpoojar@gmail.com'

    #msg.set_content("Patient Appointment Details")
    msg.add_attachment(open("report.pdf", "r").read())
    #msg.attach(MIMEText(open("report.pdf").read()))

    try:
      server.sendmail(msg,subtype='pdf')
    except:
        print ('failed')

def otp(mail_id):
    context = ssl.create_default_context()
    server=smtplib.SMTP_SSL('smtp.gmail.com', 465,context=context)
    server.login("crescent1070@gmail.com","crescent@17")
    string = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    otp = ""
    length = len(string)
    for i in range(5) :
        otp += string[math.floor(random.random() * length)]
    # otp = random.randint(1000, 9999)
    # otp = str(otp)
    msg = EmailMessage()
    msg['Subject'] = 'OTP'
    msg['From'] = 'Do well healthcare'
    msg['To'] = mail_id
    msg.set_content(otp)
    try:
      server.send_message(msg)
    except:
        print ('failed')
    return otp
