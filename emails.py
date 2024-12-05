import os
from dotenv import load_dotenv
import yagmail
import re
import time

load_dotenv()

user = os.getenv('EMAIL')
password = os.getenv('PASSWORD')


def email_details(Cprice_amazon,Cprice_flipkart,amz,flip):
    print("You will receive emails at the provided address regarding any price changes.")
    ans=None
    receiver=" "  
    while ans is None:       
        receiver=input("Enter your email: ")
        ans=re.search(r'[a-z0-9]+@[a-z]+\.[a-z]+(\.[a-z]+)*',receiver)
             
    print("Current price of the product :")
    print(f"Amazon : {Cprice_amazon}")
    print(f"Flipkart: {Cprice_flipkart}")
    time.sleep(1)
    
    y=input("You want to receive notifications if the price reaches certain amount? :")
    while y.lower()!="y" and y.lower()!="n":
        y=input("You want to receive notifications if the price reaches certain amount? :")
    treshhold=0
    if y.lower=="y":
        try:
            treshhold=int(input("Enter threshold price: "))
        except:
            print("invalid input")   
    elif y.lower=="n":
        treshhold=0
    with open("Emails.csv","a") as f:
        f.write(f'{receiver},{y},{treshhold},{Cprice_amazon},{Cprice_flipkart},{amz},{flip}' + "\n")     
        f.close()
def thresld(x,y,z):
    if z>x or z>y:
        return 1
    elif z<x or z<y:
        return -1
    elif z>x and z>y:
        return 2
    elif z<x and z<y:
        return -2
    else:
        return 0
def price_change(old_amz,old_flip,new_amz,new_flip):
    x=new_amz-old_amz
    y=new_flip-old_flip
    if x!=0 and y!=0:
        return 2
    if x!=0:
        return 1
    elif y!=0:
       return 0
    else:
        return -1                                             
def email_sender():
    yag = yagmail.SMTP(user=user , password=password)
    subject="Price change alert! "
    content1="Price change in "
    content2="Amazon by "
    content3="Flipkart by "
    from main import prices
    with open("Emails.csv","r") as f:
        for g in f:
            vary=g.split(",")
            new_amz,new_flip,a,b= prices(vary[5],vary[1])
            x=new_amz-int(vary[3])
            y=new_flip-int(vary[4])
            flag=price_change(vary[3],vary[4],new_amz,new_flip)
            truce=thresld(vary[3],vary[4],vary[2])
            if truce==0:
                flag=-1
            if flag==2:
                content=content1+"\n"+content2+str(x)+f"\t {a}"+"and "+content3+str(y)+f'\t {b}'
            elif flag==1:
                content=content1+content2+str(x)+f"\t {a}"
            elif flag==0:
                content=content1+content3+str(y)+f'\t {b}'
            else:
                content="its working yooo"           
            if content is not None:    
                yag.send(to=vary[0],subject=subject,contents=content)
            
        