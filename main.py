from flask import Flask, request, make_response, jsonify, render_template
from os import environ
# initialize the flask app
app = Flask(__name__)
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import pymysql
import sqlconnect
import mail
import json
import report
from datetime import datetime, timedelta
today = datetime.now()
cred = credentials.Certificate("firebase.json")

firebase_admin.initialize_app(cred, {
    'databaseURL' : 'https://test-yotq-default-rtdb.firebaseio.com/'
})

cardio = {
  
  "high BP": 0,
  #"shortness of breath": 0,
  "tightness around chest":0
}

derm = {
  "hairfall": 0,
  "dry hair": 0,
  "itchy/oily scalp": 0,
  "dandruff": 0,
}

opthal = {
  "frequent squinting" : 0,
  "problems in vision" : 0,
  "eye injury" : 0,
  "watery eyes" : 0,
  "irritation in eye" : 0
}
gen1={
  "cold":0,
  "cough":0,
  "fever":0,
  "sore throat":0,
  "throat pain":0,
}

gen3={
  "stomach pain":0,
  "vomiting":0,
  "Stool problems":0,
  "dizziness":0,
  "Acidity":0
}

pulmono={
  "shortness of breath": 0,
  "asthma":0,
  "wheezing":0,
  "fast breathing":0,
}

symps_json = '{}'
symps = json.loads(symps_json)

symptoms=[]
doc_list=[]
strn = []
doc_avail = ''

# default route
@app.route('/')
def index():
    return render_template('index.html')

def fetchDoc():
    ref = db.reference('Doctors/Dermatology')
    print(ref.get())

def accordion(docs):    ###  NOT IN USE
  return {
    "fulfillmentMessages": [
        {
          "payload": {
            "richContent": [
              [
                {
                  "icon": {
          "type": "chevron_right",
          "color": "#FF9800"
        },
               "type": "button",
                  "text": docs[0],
                  "link": "https://example.com",},
                # {
                #   "text": "text",
                #   "subtitle": "Accordion subtitle",
                #   "type": "button",
                #   "title": docs[1],
                  #   },
                   ] ]            
          }, }] }
def message(m):                                #funtion for return
   return { "fulfillmentMessages": [
           {
      "text": {
        "text": [
           "Do you also have "+ m +" ?",
        ]
      }
    },
      { "payload": {
          "richContent": [
            [
              { "type": "chips",
                "options": [
                  {
                    "text": "yes I have " + m
                  },
                  {
                    "text": "no"
                  }
                ],
                }
            ]]}}],
               }  

def message_G():
   return {
          "fulfillmentMessages": [
            {
              "text": {
                "text": [
                  " ", ] }
            },
              { "payload": {
                  "richContent": [
                    [
                      { "type": "chips",
                        "options": [
                          {
                            "text": "Confirm"
                          },
                          {
                            "text": "Cancel"
                          }
                        ],
                        } ] ] } } ],
               }  

def fix_appointment(s):
  return {
    "fulfillmentMessages": [
      {
      "text": {
        "text": [
           "Okay! let's fix your appointment with "+ s,
        ]
      }
    },
      { "payload": {
          "richContent": [
            [
              { "type": "chips",
               "options": [
          {
            "text": "Proceed"           
          },
          {
            "text": "Cancel"
          }
        ],} ] ] } } ], 
      }  
# function for responses
def results():  # build a request object
    global name, age, gender, location  
    global specialty
    global derma_skin, skin_type, other_skin, new_product

    req = request.get_json(force=True)

    # fetch action from json
    action = req.get('queryResult').get('action')
    print (symptoms) 
    # cardio = cardio.fromkeys(cardio, 0)
    # derm= derm.fromkeys(derm, 0)    
    if action=='appointment':                                                                                   ###### Basic info ######
      symptoms.clear() 
      derm.update({}.fromkeys(derm,0))
      cardio.update({}.fromkeys(cardio,0))
      opthal.update({}.fromkeys(opthal,0))
      gen1.update({}.fromkeys(gen1,0))
      gen3.update({}.fromkeys(gen3,0))
      pulmono.update({}.fromkeys(pulmono,0))


      name = req.get('queryResult').get('parameters').get('name')
      age = req.get('queryResult').get('parameters').get('age')
      gender = req.get('queryResult').get('parameters').get('gender')
      location = req.get('queryResult').get('parameters').get('location')
      
    elif action == 'cardio': 
      specialty='cardiology'                                                                                  ##### 1. CARDIOLOGIST ######
      val = req.get('queryResult').get('parameters').get('symptom2') 
      for i in val:
        if (i=='high BP') or (i=='tightness around chest') :
            cardio[i] = 1
            symptoms.append(i)
        
      for x,y in cardio.items():
            if y==0:
                cardio[x] = 1
                return message(x)
      return fix_appointment('Cardiologist')
        
    elif action== "Cardiology.Cardiology-no":
      specialty='cardiology'
      for x,y in cardio.items():
            if y==0:
                cardio[x] = 1
                return message(x)
      return fix_appointment('Cardiologist')          
               
    elif action=='derma':                                                                                     ###### 2. DERMATOLOGY ######
      val = req.get('queryResult').get('parameters').get('dermatology-s') 
      for i in val:
        if (i=='hairfall') or (i=='dry hair') or (i=='itchy/oily scalp')or (i=='dandruff') :
            derm[i] = 1
            symptoms.append(i)
      for x,y in derm.items():
        if y==0:
          derm[x] = 1
          return message(x)
      #fetchDoc()
      specialty='dermatology'
      
      return fix_appointment('Dermatoligist')
        
    elif action== "dermatoligist.dermatoligist-no":
      specialty='dermatology'
      for x,y in derm.items():
            if y==0:
                derm[x] = 1
                return message(x)
      
      return fix_appointment('Dermatoligist')
    
    elif action=='opthal':                                                                           ##### 3. OPHTHALMOLOGY ######
      specialty='ophthalmology'
      val = req.get('queryResult').get('parameters').get('symptoms') 
      for i in val:
        if (i=='frequent squinting') or (i=='problems in vision')or (i=='eye injury') or (i=='watery eyes') or (i=='irritation in eye'):
            opthal[i] = 1
            symptoms.append(i)
      
      for x,y in opthal.items():
            if y==0:
                opthal[x] = 1
                return message(x)
      return fix_appointment('Opthalmologist')             
      
    elif action== "Opthalmology.Opthalmology-no":
      specialty='ophthalmology'
      for x,y in opthal.items():
            if y==0:
                opthal[x] = 1
                return message(x)
      return fix_appointment('Ophthalmologist') 
    
    elif action=='gen-1':                                                                        ###### 4.1.GENERAL-1 ######
      val = req.get('queryResult').get('parameters').get('gen-1')    
      for i in val:
        if (i=='cold') or (i=='cough') or (i=='fever') or (i=='sore throat') or (i=='throat pain'):
            gen1[i] = 1
            symptoms.append(i)
      
      for x,y in gen1.items():
            if y==0:
                gen1[x] = 1
                return message(x)
      if age<=15: 
        specialty = 'paediatrics'
        print(specialty)
        return fix_appointment('Pediatrician')                     
      else:
        specialty = 'general'
        print(specialty)
        return fix_appointment('General Physician')

      gen_sym = {"symptoms_list":symptoms}
      symps.update(gen_sym)
      print(symps)

    elif action=="General-1.General-1-no":
       for x,y in gen1.items():
            if y==0:
                gen1[x] = 1
                return message(x)
       if age<=15: 
        specialty = 'paediatrics'
        print(specialty)
        return fix_appointment('Pediatrician')                     
       else:
        specialty = 'general'
        print(specialty)
        return fix_appointment('General Physician')

    elif action=='General-2':                                                                        ###### 4.2.GENERAL-2 ######
       val = req.get('queryResult').get('parameters')
       print(val)
       symptoms.append(val)
       if age<=15: 
        specialty = 'paediatrics'
        print(specialty)
        return fix_appointment('Pediatrician')                     
       else:
        specialty = 'general'
        print(specialty)
        return fix_appointment('General Physician')
    
    
    elif action=='General-3':                                                                       #####4.3.GENERAL-3 ######
      val = req.get('queryResult').get('parameters').get('gen-3')
      for i in val:
          if (i=='stomach pain') or (i=='vomiting') or (i=='Stool problems') or (i=='dizziness') or (i=='Acidity'):
            gen3[i] = 1
            symptoms.append(i)
      
      for x,y in gen3.items():
            if y==0:
                gen3[x] = 1
                return message(x)
      if age<=15: 
        specialty = 'paediatrics'
        print(specialty)
        return fix_appointment('Pediatrician')                     
      else:
        specialty = 'general'
        print(specialty)
        return fix_appointment('General Physician')
    
    elif action=="General-3.General-3-no":
       for x,y in gen3.items():
            if y==0:
                gen3[x] = 1
                return message(x)
       if age<=15: 
        specialty = 'paediatrics'
        print(specialty)
        return fix_appointment('Pediatrician')                     
       else:
        specialty = 'general'
        print(specialty)
        return fix_appointment('General Physician')
                                                                                                              ###### 4. 4. GENERAL ######   
    elif action=='gen-4':                                                        
      gen_4 = req.get('queryResult').get('parameters')
      symptoms.append(gen_4)
      if age<=15: 
       specialty = 'paediatrics'
       print(specialty)
       return fix_appointment('Pediatrician')                     
      else:
       specialty = 'general'
       print(specialty)
       return fix_appointment('General Physician')
      

    elif action=='Pulmonologist':                                                          ###### 5. PULMONOLOGIST ######
       specialty='pulmonology'
       val = req.get('queryResult').get('parameters').get('pulmo')
       for i in val:
          if (i=='shortness of breath') or (i=='asthma') or (i=='wheezing') or (i=='fast breathing'):
            pulmono[i] = 1
            symptoms.append(i)
      
       for x,y in pulmono.items():
            if y==0:
                pulmono[x] = 1
                return message(x)
       return fix_appointment("Pulmonologist")
      
    elif action=="Pulmonologist.Pulmonologist-no":
       specialty='pulmonology'
       for x,y in pulmono.items():
            if y==0:
                pulmono[x] = 1
                return message(x)
       return fix_appointment('Pulmonologist')
    
    elif action=='derma-skin':   
      specialty = 'dermatology'                
      derma_skin = req.get('queryResult').get('parameters')
      symptoms.append(derma_skin)
      return fix_appointment('Dermatoligist')
                                                                                                              ###### 6. ENT ######
    elif action=='ENT':                                                                                       
      specialty = 'ent'                
      ENT = req.get('queryResult').get('parameters')
      symptoms.append(ENT)
      return fix_appointment('ENT')
                                                                                                              ###### 7. GYNECOLOGY ######
    elif action=='gyno':   
      specialty = 'gynecology'                
      gyno = req.get('queryResult').get('parameters')
      symptoms.append(gyno)
      return fix_appointment('Gynecologist')
                                                                                                              ###### 8. PSYCHOLOGY ######
    elif action=='psycho':   
      specialty = 'psychology'                
      psych = req.get('queryResult').get('parameters')
      symptoms.append(psych)
      return {
        "fulfillmentMessages": [
          {
          "text": {
            "text": [
              "Okay! We'll fix your appointment with a psychologist ",
            ]
          }
        },
          { "payload": {
              "richContent": [
                [
                  { "type": "chips",
                  "options": [
              {
                "text": "Proceed"           
              },
              {
                "text": "Cancel"
              }
            ],} ] ] } } ], 
          }
                                                                                                              ###### 9. ORTHOLOGY ######
    elif action=='ortho':   
      specialty = 'orthopedics'                
      ortho = req.get('queryResult').get('parameters')
      symptoms.append(ortho)

      movt = req.get('queryResult').get('parameters').get('restricted-movement')
      dur = req.get('queryResult').get('parameters').get('duration')
      orth_sym = {"restricted_movements":movt , "duration":dur ,"problem":ortho}
      symps.update(orth_sym)
      print(symps)

      return fix_appointment('Orthologist')
                                                                                                              ###### 10. NEUROLOGY ######
    elif action=='neuro':   
      specialty = 'neurology'                
      neuro = req.get('queryResult').get('parameters')
      symptoms.append(neuro)
      return fix_appointment('Neurologist')
                                                                                                              ###### 11. UROLOGY ######
    elif action=='uro':   
      specialty = 'urology'                
      uro = req.get('queryResult').get('parameters')
      symptoms.append(uro)
      return fix_appointment('Urologist')
                                                                                                              ###### 12. OBSTETRICS ######
    elif action=='obstetrics':   
      specialty = 'obstetrics'                
      obst = req.get('queryResult').get('parameters')
      symptoms.append(obst)
      return fix_appointment('Obstetrician')
                                                                                                              ###### 12. DENTISTRY ######
    elif action=='dental':   
      specialty = 'dental'                
      dent = req.get('queryResult').get('parameters')
      symptoms.append(dent)
      return fix_appointment('Dentist')
                                                     
                                                      ###### CHEST PAIN ######
    elif action=='chestpain-both':
       duration=req.get('queryResult').get('parameters')
       symptoms.append(duration)
       symptoms.append("Both side chest pain")                                                                                                       
    elif action=='chestpain.chestpain-right':
       duration=req.get('queryResult').get('parameters')
       symptoms.append(duration)
       symptoms.append("right chest pain")
    
    elif action=='chestpain-right-wheezing':
       symptoms.append("wheezing")
       res = req.get('queryResult').get('parameters').get('cough')
       if res=='yes':
         symptoms.append("Coughing out mucus")
    
    elif action=='chestpain-right-wheezing-sb':   # CP pulmonologist
       specialty='pulmonology'
       symptoms.append("Shortness of breath")
    
    elif action=='chestpain-right.General':       # CP General Physician
       specialty='general'
    
    elif action=='chestpain.chestpain-right.general':       # CP General Physician
       specialty='general'
       other_problem=req.get('queryResult').get('parameters')
       symptoms.append(other_problem)
    
    elif action=='chestpain.chestpain-left':
       symptoms.append("left chest pain")
    
    elif action=='chestpain-left-arm':            # CP Cardiologist
       specialty='cardiology'
       symptoms.append("left arm pain")
   
    elif action=='chestpain-left.General':             #CP General Physician
       specialty='general'
    
    elif action=='chestpain-both':                     #CP General Physician
       specialty='general'
       duration=req.get('queryResult').get('parameters')
       symptoms.append(duration)
       return fix_appointment('General Physician')

    elif action=='head':                               # head
       head=req.get('queryResult').get('parameters')
       symptoms.append(head)
       #ask for pain around eyes

    elif action=='Headache-yes':                              
       symptoms.append("Pain around eyes")
       #ask for vision problems

    elif action=='Headache-yes-yes':                               # head ophthal
       specialty = 'ophthalmology'
       symptoms.append("Vision problem")
       return fix_appointment('Ophthalmologist')

    elif action=='Headache-yes-no-yes':                            # head neuro
       specialty = 'neurology'
       symptoms.append("Sensitivity to light and sound")
       return fix_appointment('Neurologist')

    elif action=='Headache-yes-no-no': 
       specialty = 'general'                                      # head General
       return fix_appointment('General Physician')

    elif action=='Headache-no-yes':                               # head ophthal
       specialty = 'ophthalmology'
       symptoms.append("Vision problem")
       return fix_appointment('Ophthalmologist')

    elif action=='Headache-no-no': 
       specialty = 'general'                                      # head general
       return fix_appointment('General Physician')

    elif action == "final":                  ##  TESTING
      print("thankyou")
    
    elif action == "doc.list":  
       name = req.get('queryResult').get('parameters').get('name')
       age = req.get('queryResult').get('parameters').get('age')
       gender = req.get('queryResult').get('parameters').get('gender')
       location = req.get('queryResult').get('parameters').get('location')               ## Doctors list
       val = req.get('queryResult').get('parameters').get('specialty')
       specialty=val
       return fix_appointment(val)
    
    elif (action=='fix.appointment') or (action=='date_error'):             ## Fix appointment
       global date,mail_id,otp
       
       d = req.get('queryResult').get('parameters').get('date')
       #specialty=req.get('queryResult').get('parameters').get('specialty')
       date=d[0:10]
       print (date)
       check = sqlconnect.checkdate(specialty,date)
       if (check==None):
         return{
     
              "followupEventInput": {
                "name": "date_error",
                "parameters": { },
                "languageCode": "en"
               }
 
             }  
       print(specialty)
       doctor_data=sqlconnect.mysqlconnect(date,specialty)
       print(doctor_data)
      
       #return { "fulfillmentText":  doctor_data}  
       return{"fulfillmentMessages": [
        {
          "payload": {
            "richContent": [
              [ { "type": "description",
                  "title": "Available slots on "+ date ,

                  "text":
                   [ "Reply with ID",
                     doctor_data],
                  }
                ]
            ]} }]
          }
    
    elif action=="FixAppointment-SlotNumber":                                                  #  APPOINTMENT CONFIRMATION
      global id_num,doctor_name,doctor_time
      id_num= req.get('queryResult').get('parameters').get('number')
      doctor_name=sqlconnect.name(int(id_num),specialty)
      doctor_time=sqlconnect.time(int(id_num),specialty)
      return {"fulfillmentMessages": [
      {   "payload": {
            "richContent": [
            [
              { "type": "description",
              "title": "Your appointment details ",
                "text":[ "Date : "+ date, "Doctor : "+doctor_name, "Time : "+doctor_time, ]
              },
              { "type": "chips",
                          "options": [
                            {
                              "text": "Confirm"
                            },
                            {
                              "text": "Cancel"
                            }
                          ],
                          }
              ]]} }] }
    
    elif action=="FixAppointment-SlotNumber.confirm":
       mail_id=req.get('queryResult').get('parameters').get('email_id')
       otp=mail.otp(mail_id)
       return { "fulfillmentText":"Enter the otp sent to your mail"}
   
    elif action=='FixAppointment-confirm-otp':
       print("Im in otp")
       num=req.get('queryResult').get('parameters').get('otp')
       try:
          if num==otp:
              sqlconnect.book_appointment(int(id_num),specialty,mail_id)
              #ref = db.reference('Patients')
              ref = db.reference('Appointments/'+specialty)
              pushID = ref.push(
              { 
                  'PatientName' : name,
                  'age' : int(age),
                  'gender' : gender,
                  'location' : location,
                  'symptoms': symptoms,
                  'specialty': specialty,
                  'Date': date,
                  'Doctor':doctor_name,
                  'Time':doctor_time

                })

              print(pushID.key)
              mail.mail(mail_id, date,specialty, doctor_name, doctor_time)
              report.generate(pushID.key,specialty)
              return{
                  "followupEventInput": {
                    "name": "final",
                    "parameters": { },
                    "languageCode": "en"
                  }
                } 
       except:
          print ("failed otp") 
          return {
            "fulfillmentMessages": [
              {
                "text": {
                  "text": [
                    " Sorry, Your otp verification failed. Retype it or click on below button", ] }
              },
                { "payload": {
                  "richContent": [
              [
                {
                  "type": "list",
                  "title": "Resend Otp",
                  "event": {
                    "name": "verify",
                    "languageCode": "",
                    "parameters": {}
                  }
                }] 
          ]} } ],
                      }  
    elif action=='cancel-intent':
      symptoms.clear()
    
    elif action=='cancel_appointment-specialty':
      global table
      mail_id=req.get('queryResult').get('parameters').get('email_id')
      table = req.get('queryResult').get('parameters').get('specialty')
      print(mail_id)
      
      print(table)
      otp=mail.otp(mail_id)
      return { "fulfillmentText":"Enter the otp sent to your mail"}
      
    elif action=='cancel_appointment-otp':
      num=req.get('queryResult').get('parameters').get('otp')
      try:
        if num==otp:
          sqlconnect.cancel_appointment(mail_id,table)
          return{"fulfillmentText": "You have successfully cancelled your appointment"}
      except:
         return{"fulfillmentText": "sorry verification failed, try after some time"}
# create a route for webhook
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # return response
    return make_response(jsonify(results()))


# run the app
if __name__ == '__main__':
   app.run(host='0.0.0.0', port=environ.get("PORT", 5000))
   


  
