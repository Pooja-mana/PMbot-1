from flask import Flask, request, make_response, jsonify
# initialize the flask app
app = Flask(__name__)
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import pymysql
import sqlconnect
import mail
import json
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

symptoms=[]
doc_list=[]
strn = []
doc_avail = ''

# default route
@app.route('/')
def index():
    return 'Patient Management!'

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
def message(m):                                           #funtion for return
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
            "text": "No,thanks"
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
    
    if action=='appointment':                                                                                  ###### Basic info ######
                      
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
    
    elif action=='opthal':                                                                                    ##### 3. OPHTHALMOLOGY ######
      specialty='ophthalmology'
      val = req.get('queryResult').get('parameters').get('opthal-s') 
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
      return fix_appointment('Opthalmologist') 
    
    elif action=='gen-1':                                                                                     ###### 4.1.GENERAL-1 ######
      specialty='general'
      val = req.get('queryResult').get('parameters').get('gen-1')    
      for i in val:
        if (i=='cold') or (i=='cough') or (i=='fever') or (i=='sore throat') or (i=='throat pain'):
            gen1[i] = 1
            symptoms.append(i)
      
      for x,y in gen1.items():
            if y==0:
                gen1[x] = 1
                return message(x)
      return fix_appointment('General Physician')
   
    elif action=="General-1.General-1-no":
       specialty='general'
       for x,y in gen1.items():
            if y==0:
                gen1[x] = 1
                return message(x)
       return fix_appointment('General Physician')

    elif action=='General-2':                                                                                 ###### 4.2.GENERAL-2 ######
       specialty='general'
       val = req.get('queryResult').get('parameters')
       print(val)
       symptoms.append(val)
    
    elif action=='General-3':                                                                                 ###### 4.3.GENERAL-3 ######
      specialty='general'
      val = req.get('queryResult').get('parameters').get('gen-3')
      for i in val:
          if (i=='stomach pain') or (i=='vomiting') or (i=='Stool problems') or (i=='dizziness') or (i=='Acidity'):
            gen3[i] = 1
            symptoms.append(i)
      
      for x,y in gen3.items():
            if y==0:
                gen3[x] = 1
                return message(x)
      return fix_appointment('General Physician')
    
    elif action=="General-3.General-3-no":
       specialty='general'
       for x,y in gen3.items():
            if y==0:
                gen3[x] = 1
                return message(x)
       return fix_appointment('General Physician')
                                                                                                              ###### 4. 4. GENERAL ######   
    elif action=='gen-4':                                                                                              
      specialty = 'general'                
      gen_4 = req.get('queryResult').get('parameters')
      symptoms.append(gen_4)
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
      specialty = 'ENT'                
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
      return fix_appointment('Psychologist')
                                                                                                              ###### 9. ORTHOLOGY ######
    elif action=='ortho':   
      specialty = 'orthopedics'                
      ortho = req.get('queryResult').get('parameters')
      symptoms.append(ortho)
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

    elif action == "testing":                  ##  TESTING
      ref = db.reference('Doctors/Dermatology')
      snapshot = ref.get()
      return accordion(snapshot)
    
    elif action == "doc.list":                 ## Doctors list
      val = req.get('queryResult').get('parameters').get('specialty')
      print(val)
    
    
    elif (action=='fix.appointment') or (action=='date_error'):             ## Fix appointment
       global date,mail_id
       mail_id=req.get('queryResult').get('parameters').get('email_id')
       d = req.get('queryResult').get('parameters').get('date')
       #specialty=req.get('queryResult').get('parameters').get('specialty')
       date=d[0:10]
       print (date)
       print (mail_id)
       check = sqlconnect.checkdate(specialty,date)
       if (check==None):
         return{
     
              "followupEventInput": {
                "name": "date_error",
                "parameters": { },
                "languageCode": "en"
               }
 
             }  
      #return { "fulfillmentText": "Sorry, That date is not available"}  
       
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
    
    elif action=="FixAppointment-SlotNumber":                                                            #  APPOINTMENT CONFIRMATION
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
       sqlconnect.book_appointment(int(id_num),specialty)
       #ref = db.reference('Patients')
       ref = db.reference('Appointments/'+specialty)
       ref.push(
       { 
          'Patient Name' : name,
          'age' : age,
          'gender' : gender,
          'location' : location,
          'symptoms': symptoms,
          'specialty': specialty,
          'Date': date,
          'Doctor':doctor_name,
          'Time':doctor_time

        })
       symptoms.clear()
       mail.mail(mail_id)
       return { "fulfillmentText": "Thankyou! You have successfully booked an appointment"}  
   
# create a route for webhook
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # return response
    return make_response(jsonify(results()))


# run the app
if __name__ == '__main__':
   port = process.env.PORT || 8080;
   app.run(host='0.0.0.0', port)
   


  
