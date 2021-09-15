import schedule
import time
import requests
import ast
import pandas as pd
import os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import smtplib

velocityUrl='http://127.0.0.1:8000/api/'
headers = {'Authorization': "Token 658dd0395badb9fe407ea6a16763458a14accb87","user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"}

#get all Category details With id, name, label, category_slug
def get_All_category():
    res=requests(url=velocityUrl+"get_all_category",headers=headers)
    return res.categoryList

#get Number of empty products list in category child assortment onthe basic of category id
def get_no_Of_empty_assortment_in_categorychild(id):
    res=requests(url=velocityUrl+"get_empty_assortment_in_categorychild/"+id,headers=headers)
    return res.nullChildCategory

def create_Report_and_send_By_Email(categorylist):
     masterDataFrame = pd.DataFrame(categorylist)
     if os.path.exists("Report_Feedback"):
         print("Directory already exist..")
     else:
        os.mkdir("Report_Feedback")
        masterDataFrame.transpose()
        masterDataFrame.to_csv("Empty_AssortMent_Report_In_CategoryChild/Empty_AssortMent_Report_In_CategoryChild.csv",index=False,header=True, encoding='utf-8')

        if os.path.exists("Empty_AssortMent_Report_In_CategoryChild/Empty_AssortMent_Report_In_CategoryChild.csv"):
            print("Report created succesfully....")
            msg = MIMEMultipart()
            msg['From'] = "proscons12345@gmail.com"
            msg['To'] = "4b158cdb.shorthillstech.com@in.teams.ms"
            msg['Subject'] = "Auto Generated Empty Assortment From CategorChild"
            part = MIMEBase('application', "octet-stream")
            part.set_payload(open("Empty_AssortMent_Report_In_CategoryChild/Empty_AssortMent_Report_In_CategoryChild.csv", "rb").read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="Active_Report_In_Category/Active_Product_In_Category.csv"')
            msg.attach(part)
            s = smtplib.SMTP('smtp.gmail.com', 25) 
            s.connect("smtp.gmail.com",587)
            s.ehlo()
            s.starttls()
            s.ehlo()
            s.login("proscons12345@gmail.com", "A1234@...123")
            s.sendmail("proscons12345", "4b158cdb.shorthillstech.com@in.teams.ms",msg.as_string())
            s.quit()   
            print("Mail Send to BVR Teams Group")
            return "Empty_AssortMent_Report_In_CategoryChild/Empty_AssortMent_Report_In_CategoryChild.csv"
        else:
            return "Report not generated"             
           
def analyseEmptyAssortments():
    listOfEmptyAssortments=[]
    category_list=get_All_category()
    for category in category_list:
        noOfEmptyInCategory=get_no_Of_empty_assortment_in_categorychild(category['id'])
        if noOfEmptyInCategory>0:
            temp={
                'id':category['id'],
                'name':category['name'],
                'label':category['label'],
                'category_slug':category['category_slug']
                }
            listOfEmptyAssortments.append(temp)
    
    if listOfEmptyAssortments==[]:
        print("No any category in categoryChild whose assortemnet list is empty")
    else:
        create_Report_and_send_By_Email(listOfEmptyAssortments) 

schedule.every(10).hours.do(analyseEmptyAssortments)
while True:
    schedule.schedule.schedule.run_pending()
    time.sleep(1)













