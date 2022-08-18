import chromedriver_autoinstaller
from selenium import webdriver

def GettingDriver():
    chromedriver_autoinstaller.install()
    driver = webdriver.Chrome()
    driver.maximize_window()
    return driver