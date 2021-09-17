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

bvrUrl='http://127.0.0.1:8000/api/'
headers = {'Authorization': "Token 658dd0395badb9fe407ea6a16763458a14accb87","user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"}

#get all Category details With id, name, label, category_slug
def get_All_category():
    print("Enter")
    try:
        res=requests(url=bvrUrl+"all_categories_url",headers=headers)
        print(res)
        all_categories=res['all_categories']
        return all_categories
    except Exception as e:
        print(e)

def get_non_empty_assortment_in_categorychild(id):
    res=requests(url=bvrUrl+"get_non_empty_assortment_in_categorychild/"+id,headers=headers)


#get Number of empty products list in category child assortment onthe basic of category id
def get_non_active_product_asin_codes(child):
    res=requests(url=bvrUrl+"get_non_active_product_asin_codes/"+child,headers=headers)
    return res.data

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
            msg['From'] = "Sushilprasad60649@gmail.com"
            msg['To'] = "Sushilprasad60649@gmail.com"
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
    print("1st called")
    listOfEmptyAssortments=[]
    category_list=get_All_category()
    print(category_list)
    for category in category_list:
        childs=get_non_empty_assortment_in_categorychild(category['id'])
        for child in childs:
            results=get_non_active_product_asin_codes(child['result'])
            if results==False:
                listOfEmptyAssortments.append({'category_child':child})

    if listOfEmptyAssortments==[]:
        print("No any non live categoryChild accordig to asin codes")
    else:
        print("Send")
        create_Report_and_send_By_Email(listOfEmptyAssortments) 

analyseEmptyAssortments()
# schedule.every(10).minutes.do(analyseEmptyAssortments)
# while True:
#     schedule.run_pending()
#     time.sleep(1)













