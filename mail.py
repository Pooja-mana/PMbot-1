import smtplib,ssl
import math,random
from email.message import EmailMessage
def mail(mail_id, date1,specialty, doctor_name, doctor_time):
    context = ssl.create_default_context()
    server=smtplib.SMTP_SSL('smtp.gmail.com', 465,context=context)
    #server.ehlo()
    #server.starttls()
    server.login("crescent1070@gmail.com","crescent@17")
    # msg="""Your appointment details 
    #         "Date : "+ date, 
    #         "Doctor : "+doctor_name,
    #          "Time : "+doctor_time """
    msg = EmailMessage()
    msg['Subject'] = 'Appointment Details'
    msg['From'] = 'Do well healthcare'
    msg['To'] = mail_id
    msg.set_content("""\
          <!DOCTYPE html>
          <html>
              <body>
                  <h3 style="color:SlateGray;">You have successfully booked appointment.
                  Do well healthcare
                  </h3>
                  <h5 id= 'docname'></h5>
                  <a href="url">Join with this link</a>

               
              </body>
               <script type="javascript"> 
              (function() {
                document.getElementById('docname').innerHTML = doctor_name;
              }());
              </script>
          </html>
          """, subtype='html')
    #message="""You have successfully booked appointment."""
    try:
      server.send_message(msg)
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
