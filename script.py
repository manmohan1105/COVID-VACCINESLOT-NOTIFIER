import requests
from datetime import datetime,timedelta
import time
import json
import smtplib
from email.message import EmailMessage
def emailalert(subject,body,to):
   msg=EmailMessage()
   msg.set_content(body)
   msg['subject']=subject
   msg['to']=to
   
   user="*******"
   password=""
   msg["from"]=user
   server=smtplib.SMTP("smtp.gmail.com",587)
   server.starttls()
   server.login(user,password)
   server.send_message(msg)
   server.quit()
print("hello")
age=50
pincodes=["452010","452011","452009","452006"]
days=2
print_flag = 'Y'
print("searching.....")
actualdate=datetime.today()
list_format=[actualdate +timedelta(days=i) for i in range(days)]
required_dates=[i.strftime("%d-%m-%Y") for i in list_format]
cnt=0
while True:
    cnt+=1
    counter=0
    for pincode in pincodes:
        for givendate in required_dates:
            URL="https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}".format(pincode, givendate)
            header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'} 
            result=requests.get(URL,headers=header)
            if result.ok:
                responce_json=result.json()
                flag=False
                if responce_json["centers"]:
                    if (print_flag.lower()=="y") :
                        for center in responce_json["centers"]:
                            for session in center["sessions"]:
                                if session["min_age_limit"]<=age and session["available_capacity"]>0:
                                    print("pincode:"+pincode)
                                    print("Available slot on:{}".format(givendate))
                                    print(center["name"])
                                    print(center["block_name"])
                                    print("price:",center["fee_type"])
                                    print("Availablity:",session["available_capacity"])
                                    centername=center["name"]
                                    blockname=center["block_name"]
                                    fees=center["fee_type"]
                                    vaccines=session["vaccine"]
                                    Availablity=session["available_capacity"]
                                    n1="\n"
                                    if (session["vaccine"]!=""):
                                        subject=f"pincode:{pincode}{n1} ----Available slots date:{givendate}{n1}--- center name:{centername}{n1} ---center block name:{blockname}{n1}---- price:{fees}{n1}---  vaccine:{vaccines}{n1}----,availablity of slots:{Availablity}"
                                        print("Vaccine type:",session["vaccine"])
                                        emailalert("covid vaccination slot available",subject,"")
                                    print("\n")   
                                    counter+=1
                                else:
                                    pass     
                    else:
                        pass                
                else:
                    pass
            else:
                print("No responce")
    if counter==0:
        print("NO slot available at your pincodes")
    else:
        print("search completed")
    if cnt==2:
        print("YOU may Check some other time")
        break    
    dt=datetime.now()+timedelta(minutes=3)
    while datetime.now()<dt:
        time.sleep(1)                
