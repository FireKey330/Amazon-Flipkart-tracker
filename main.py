

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from URL import *
from emails import email_details, email_sender
import schedule
import time
from selenium.webdriver.common.by import By


def get_driver(url):
  options = webdriver.ChromeOptions()
  options.add_argument("disable-infobars")
  options.add_argument("start-maximized")
  options.add_argument("disable-dev-shm-usage")
  options.add_argument("no-sandbox")
  options.add_experimental_option("excludeSwitches", ["enable-automation"])
  options.add_argument("disable-blink-features=AutomationControlled")
  headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"
}
  driver = webdriver.Chrome(options=options)
  driver.get(url)
  
  return driver

def google(text,flag):
  driver=get_driver("https://google.com")
  driver.find_element(By.NAME, "q").send_keys(text+Keys.RETURN)
  turn,x=0,0
  if flag==0:
      s="fl"
  else:
      s="am"    
  while turn==0:
    result = driver.find_element(By.XPATH, f'(//h3/parent::a)[{x}]')
    link = result.get_attribute("href")
    if str(link)[8:10]==s:
        return str(link)
    x+=1
  
  
def comma(text):
   toxt=text.split(",")
   return int("".join(toxt))
  
def text_fromamazon(url):
  driver=get_driver(url)
  product_title=driver.find_element(by="id",value="productTitle").text
  driver.quit 
  return google(product_title+" flipkart",0) 
  
def text_fromflipkart(url):
  driver=get_driver(url)
  product_title=driver.find_element(by="xpath",value='//*[@id="container"]/div/div[3]/div[1]/div[2]/div[3]/div/div[1]/h1/span').text  
  driver.quit
  return google(product_title+" amazon",1)

def amazon_price(url):
  driver=get_driver(url)
  commas=driver.find_element(by="xpath", value='//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span[3]/span[2]/span[2]').text
  driver.quit
  return int(comma(commas)),url
  
  
def flipkart_price(url):                      #    //*[@id="container"]/div/div[3]/div[1]/div[2]/div[2]/div/div[3]/div[1]/div/div[1]
  driver=get_driver(url)                       #  //*[@id="container"]/div/div[3]/div[1]/div[2]/div[2]/div/div[4]/div[1]/div/div[1]
  commas=driver.find_element(by="xpath", value='//*[@id="container"]/div/div[3]/div[1]/div[2]/div[2]/div/div[3]/div[1]/div/div[1]').text
  driver.quit
  return int(comma(commas[1:])),url                 

def amz_urlCON(url):
     driver=get_driver(url)
     time.sleep(7)
     ASIN=driver.find_element(by="xpath",value='//*[@id="productDetails_detailBullets_sections1"]/tbody/tr[1]/td').text
     new_url=f'https://www.amazon.in/dp/{ASIN}'
     return new_url
def prices(url,x):
  if x>0:
    amazon,amz_url=amazon_price(url)
    if x==1:  
       amz_url=amz_urlCON(url)    
    flipkart,flip_url=flipkart_price(text_fromamazon(url))
  elif x==0:
    amazon,amz_url=amazon_price(text_fromflipkart(url))
    amz_url=amz_urlCON(amz_url)
    flipkart,flip_url=flipkart_price(url)
  else:
    amazon,flipkart,amz_url,flip_url=0,0,0,0 
  return amazon,flipkart,amz_url,flip_url
#https://amzn.in/d/9Xy478
      
def sub_main():
  inputt = input("URL: ")
  ans=link_valid(inputt)
  while url_accessible(inputt)==False or ans==-1:
    print("Invalid URL: ")
    inputt = input("URL: ")
    ans=link_valid(inputt)  
  print(f'{ans} is the variable <----')
  a,b,c,d=prices(inputt,ans)
  email_details(a,b,c,d)
  
  
def main():
     email_sender()
         
sub_main()
main()
schedule.every(12).hours.do(main)
while True:
    schedule.run_pending()
    time.sleep(1)  
      
    
    
 

