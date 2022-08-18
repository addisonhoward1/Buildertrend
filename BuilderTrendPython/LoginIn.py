import time
import os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def LoggingIn(driver):
    URLstring = os.getenv("URL")
    driver.get(URLstring)
    delay = 10
    username = os.getenv("BT_USERNAME")
    password = os.getenv("BT_PASSWORD")

    usernameField = wait(driver, delay).until(EC.presence_of_element_located((By.ID, 'username')))
    usernameField.send_keys(username)

    passwordField = wait(driver, delay).until(EC.presence_of_element_located((By.ID, 'password')))
    passwordField.send_keys(password)
    loginBtn = wait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="reactLoginListDiv"]/div/div/div/div/div/div[3]/div/div/div/form/button')))
    loginBtn.click()
    
    wait(driver, delay).until(EC.presence_of_element_located((By.ID, 'JobSearch')))