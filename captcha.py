from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import requests


url = 'https://www.google.com/recaptcha/api2/demo'

def get_driver():
  chrome_options = Options()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--headless')
  chrome_options.add_argument('--disable-dev-shm-usage')
  chrome_options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/59.0.3071.115 Safari/537.36")
  driver = webdriver.Chrome(options=chrome_options)
  return driver


if __name__ == "__main__":
  print('Creating driver...')
  driver = get_driver()

  try:
    
    captcha_key = WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"//iframe[@id='main-iframe']"))).get_attribute("data-sitekey")

    url = "https://2captcha.com/in.php?"
    url += "key=" + open('./api_key.txt').readline().strip()
    url += "&method=userrecaptcha"
    url += "&googlekey=" + captcha_key
    url += "&pageurl=" + url
    url += "&json=0"
  
    print(url)
  
    response = requests.get(url)
  
    captcha_service_key = response.text
  
    print(captcha_service_key)
   
    captcha_service_key = captcha_service_key.split('|')[-1]
  
  
    url_resp = "https://2captcha.com/res.php?"
    url_resp += "key=" + "f300d3f245f9820efaced256a2b5c942"
    url_resp += "&action=get"
    url_resp += "&id=" + captcha_service_key 
    url_resp += "&json=0"
  
    print(url_resp)
  
    sleep(25)
  
    while True:
      solver = requests.get(url_resp)
      solver = solver.text
      print (solver)
  
      if solver == "CAPTCHA_NOT_READY":
        sleep(5)
      else: 
        break
  
    solver = solver.split('|')[-1]
    print ()
  
    result = 'document.getElementById("g-recaptcha-response").innerHTML="' + solver + '";'
    print (result)
  
    driver.execute_script(result)
  
    submit_button = driver.find_element(By.XPATH,'//input[@id="recaptcha-demo-submit"]')
    submit_button.click()
  except Exception as e:
    print (e) 
  
    print ("Something is missing...")
  
    content = driver.find_elements(By.CLASS_NAME,'recaptcha-success')
    print (content.text)
