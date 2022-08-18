from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def jsReady(driver):
    wait(driver, 10).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    wait(driver, 10).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
