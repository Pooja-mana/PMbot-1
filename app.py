# import flask dependencies
from flask import Flask, request, make_response, jsonify
import requests
# initialize the flask app
app = Flask(__name__)
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("firebase.json")
firebase_admin.initialize_app(cred, {
    'databaseURL' : 'https://patient-management-314214-default-rtdb.firebaseio.com/'
})

symps = {
  "chest pain": 0,
  "high_Bp": 0,
  "pulse rate": 0,
  "shortness of breath": 0,
}
derm = {
  "hairfall": 0,
  "dry hair": 0,
  "itchy/oily scalp": 0,
  "dandruff": 0,
}
opthal = {
  "frequent squinting" : 0,
  "constant headache" : 0,
  "problems in vision" : 0,
  "eye injury" : 0,
  "watery eyes" : 0,
  "irritation in eye" : 0
}
gen1={
  "cold":0,
"cough":0,
"fever":0,
"soar throat":0,
"body pain":0,
"throat pain":0,

}
ques=[]
symptoms=[]

# default route
@app.route('/')
def index():
    return 'Hello World!'

#funtion for return
def message(m):
   return {
      "fulfillmentMessages": [
        {
      "text": {
        "text": [
           "do u also have "+ m +" ?",
        ]
      }
    },
      {
        "payload": {
          "richContent": [
            [
              {
                
                 "type": "chips",
                "options": [
                  {
                    "text": "yes I have " + m
                  },
                  {
                    "text": "no"
                  }
                ],
                "text": "do you also have "
              }
            ]
          ]
        }
      }
    ],
                      }  

# function for responses
def results():
    # build a request object
    req = request.get_json(force=True)

    # fetch action from json
    action = req.get('queryResult').get('action')

    # return a fulfillment response

    if action == 'cardio':                                                 ###### CARDIOLOGIST ######
      val = req.get('queryResult').get('parameters').get('symptom2') 
 
      for i in val:
        if (i=='chest pain') or (i=='high_Bp') or (i=='pulse rate')or (i=='shortness of breath') :
            symps[i] = 1
            symptoms.append(i)
        
      
      for x,y in symps.items():
            if y==0:
                symps[x] = 1
                #calling funtion
                
                return message(x)
                
      return { 'fulfillmentText': "Okay! let's fix your appointment with cardiologist"}
      
      #print(symps["high_Bp"])  
        #         ques.append(x)
        # for i in range (1,4):
        #     return { 'fulfillmentText': "do you have " + ques[i] + "?"}
        
    elif action== "Cardiology.Cardiology-no":
      for x,y in symps.items():
            if y==0:
                symps[x] = 1
                
                #print(symps.values()) 
               
                return message(x)
            
              # symptoms.append()
              # print symptoms

      return { 'fulfillmentText': "okay ...Thank you"}   
      # for x in range(len(symptoms)):
      #    print symptoms[x]       
               
    elif action=='derma':                                                  ###### DERMATOLIGIST ######
      val = req.get('queryResult').get('parameters').get('dermatology-s') 
 
      for i in val:
        if (i=='hairfall') or (i=='dry hair') or (i=='itchy/oily scalp')or (i=='dandruff') :
            derm[i] = 1
        #print(i)
      
      for x,y in derm.items():
            if y==0:
                symptoms.append(x)
                derm[x] = 1
                return message(x)
      return { 'fulfillmentText': "Okay! let's fix your appointment with dermatologist"}
    
    elif action== "dermatoligist.dermatoligist-no":
      for x,y in derm.items():
            if y==0:
                derm[x] = 1
                
                #print(symps.values())  
                return message(x)
      
      return { 'fulfillmentText': "Okay! let's fix your appointment with dermatologist"}
    
    elif action=='opthal':                                           ###### OPTHAL ######
      val = req.get('queryResult').get('parameters').get('opthal-s') 
 
      for i in val:
        if (i=='frequent squinting') or (i=='constant headache') or (i=='problems in vision')or (i=='eye injury') or (i=='watery eyes') or (i=='irritation in eye'):
            opthal[i] = 1
            symptoms.append(i)
      
      for x,y in opthal.items():
            if y==0:
                opthal[x] = 1
                return message(x)
                      
      return { 'fulfillmentText': "I'll fix your appointment with Opthalmologist"}
    
    elif action=='gen-1':                                             ###### GENERAL-1 ######
      val = req.get('queryResult').get('parameters').get('gen-1') 
      
      for i in val:
        if (i=='cold') or (i=='cough') or (i=='fever')or (i=='body pain') or (i=='soar throat') or (i=='throat pain'):
            gen1[i] = 1
            symptoms.append(i)
      
      for x,y in gen1.items():
            if y==0:
                gen1[x] = 1
                return message(x)
               
      return { 'fulfillmentText': "okay! let's fix your appointment with General Doctor"}
      
    elif action=="General-1.General-1-yes":
       for x,y in gen1.items():
            if y==0:
                gen1[x] = 1
                return message(x)
       return { 'fulfillmentText': "okay! let's fix your appointment with General Doctor"}
    
    elif action=='appointment': 
      global name, age, gender,loc                                       ###### GENERAL-1 ######
      name = req.get('queryResult').get('parameters').get('name')
      age = req.get('queryResult').get('parameters').get('age')
      gender = req.get('queryResult').get('parameters').get('gender')
      loc = req.get('queryResult').get('parameters').get('location')


ref = db.reference('Patients')
ref.push(
    { 
      'age' : age,
      'Name' : name,
      'gender' : gender,
      'location' : loc
    })

# create a route for webhook
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # return response
    return make_response(jsonify(results()))

# run the app
if __name__ == '__main__':
   app.run()


  