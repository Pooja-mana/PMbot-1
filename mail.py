import smtplib,ssl
def mail(mail_id):
    context = ssl.create_default_context()
    server=smtplib.SMTP_SSL('smtp.gmail.com', 465,context=context)
    #server.ehlo()
    #server.starttls()
    server.login("crescent1070@gmail.com","Crescent")
    message="""<b>You have successfully booked appointment.</b>
<h1>Do well healthcare.</h1>"""
    try:
      server.sendmail("crescent1070@gmail.com",
       mail_id,
       message)
    except:
        print ('failed')
