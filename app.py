from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os

service = Service()
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

#example
load_dotenv()
user = os.getenv("USER")
psw = os.getenv("PASSWORD")
url = os.getenv("URL")

#example to login

driver.get(url)

wait = WebDriverWait(driver, 10)
user_input = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="frm-login"]/form/div[1]/input')))
user_input.send_keys(user)

pass_input = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="frm-login"]/form/div[2]/input')))
pass_input.send_keys(psw)

login_btn = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="frm-login"]/form/button')))
login_btn.click()

#-------- end example -------- 

driver.quit()
