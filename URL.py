import re
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException

def gett_driver(url):
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
#def url_accessible(url):
#    try:
#        response = requests.get(url, timeout=5)
#        if response.status_code == 200:
#            return True
#        else:
#            return False
#    except requests.RequestException:
#         return False
#driver = webdriver.Chrome()  
def url_accessible(url):
         try:
           driver=gett_driver(url)
           print(f"URL is accessible: {url}")
           driver.quit()
           return True
         except (TimeoutException, WebDriverException):
           print(f"URL is not accessible: {url}")         
           return False
  
#https://amzn.in/d/5f2W2FS
#https://www.amazon.in/MI-inches-Smart-Google-L43M8-5AIN/dp/B0CH31V44H
def link_valid(url):
    amazon1=re.search(r"https://amzn\.in/[a-z]/[A-Za-z0-9]+",url)
    amazon2=re.search(r"https://www\.amazon\.in/.*/[a-z][a-z]/[A-Za-z0-9]+",url)   
    flipkart1=re.search(r"https://flipkart\.com/[a-zA-z-]+/[^ ]+",url)
    if amazon1:
        return 1
    elif amazon2:
        return 2  
    elif flipkart1:
        return 0
    else:
        return -1

