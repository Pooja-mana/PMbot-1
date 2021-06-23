import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import doc_mail
import send
# cred = credentials.Certificate("firebase.json")

# firebase_admin.initialize_app(cred, {
#     'databaseURL' : 'https://test-yotq-default-rtdb.firebaseio.com/'
# })

# specialty='dermatology'
# id='-Mcn9WhQmBRKdJlZQh2q'
def generate(id,specialty):
      ref = db.reference('Appointments/'+specialty+'/'+id)
      # a=ref.get(specialty)
      a=ref.get()
      try:
       with open("message.txt", 'w') as f: 
        f.write('DOWELL HEALTHCARE PATIENT REPORT \n\n')
        for key, value in a.items(): 
            if key!='symptoms':
              f.write('\n%s : %s' % (key, value))
        for i in a["symptoms"]:    ### divide it
            print(i)
            for m,n in i.items():
              if m=='duration':
                  f.write('\n%s : ' % (m))
                  for x,y in n.items():
                    f.write('%s ' % (y))
              else:
                f.write('\n%s : %s' % (m,n))
                print(m,n)
      except:
              #### general
        with open("message.txt", 'w') as f: 
            f.write('DOWELL HEALTHCARE PATIENT REPORT \n\n')
            for key, value in a.items(): 
              if key!='symptoms':
               f.write('\n%s : %s' % (key, value))
            f.write('Symptoms :')
            for i in a["symptoms"]: 
                  if (type(i) is dict)==True:
                    f.write('\n%s: '% (i.key))
                    for x,y in i.items():
                        f.write('%s' % (y))
                  
                  else:
                   f.write('\n%s ' % (i))
              # print(key,value)  
              # f.write('%s : %s\n' % (key, value))
                
      from fpdf import FPDF

      pdf = FPDF()   

      pdf.add_page()

      pdf.set_font("Arial", size = 20)

      f = open("message.txt", "r")

      for x in f:
        pdf.cell(200, 10, txt = x, ln = 1, align = 'C')

      pdf.output("P_report.pdf")   
      ##### GENERAL, CARDIO, DERMO
      send.mail()




      
              #ORTHOPEDICS
      # with open("message.txt", 'w') as f: 
      #     for key, value in a.items(): 
      #         if key!='symptoms':
      #          f.write('%s : %s\n' % (key, value))
      #     for i,j in a["symptoms"].items():
      #         print (i,j)
      #         if i=='duration':
      #             f.write('%s: ' % (i))
      #             for x,y in j.items():
      #                 f.write(' %s' % (y))
      #         else:
      #             f.write('\n%s:%s' % (i,j))
