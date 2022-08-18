from distutils.log import error
import time
import os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import re
from EmailTemplate import ErrorEmail
from ReadyState import jsReady


def GettingSuperInfo(driver, engine):
    try:
        URLstring = os.getenv("SUPER_URL")
        driver.get(URLstring)

        delay = 20
        pageLst = wait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="rc-tabs-0-panel-0"]/div/div[1]/div/div[2]/div/div/span/div/div/span[2]')))
        pageLst.click()
        time.sleep(1)
        for i in range(10):
            try:
                page250 = wait(driver, .25).until(EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="ctl00_ctl00_bodyTagControl"]/div[' + str(i) + ']/div/div/div/div/div[2]/div/div/div/div[5]')))
                page250.click()
                print(str(i) + " did work!")
                break
            except:
                print(str(i) + " didn't work.")
        time.sleep(5)
        jsReady(driver)

        curPage = wait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="rc-tabs-0-panel-0"]/div/div[1]/div/div[2]/div/ul/li[2]/input')))
        curPage = curPage.get_attribute('value')
        curPage = int(re.sub("[^0-9]", "", curPage))

        lastPage = wait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'ant-pagination-simple-pager')))
        lastPage = lastPage.text
        lastPage = int(re.sub("[^0-9]", "", lastPage))

        for i in range(lastPage):
            soup = BeautifulSoup(driver.page_source, 'lxml')
            htmltable = soup.find('table', {'class': 'k-grid-table'})
            df = pd.read_html(str(htmltable))
            df = df[0]
            df = df.astype(str)

            mapping = {
                df.columns[0]: "Job Color",
                df.columns[1]: "Job Name",
                df.columns[2]: "Street Address",
                df.columns[3]: "City",
                df.columns[4]: "State",
                df.columns[5]: "Zip Code",
                df.columns[6]: "Project Manager",
                df.columns[7]: "Owner",
                df.columns[8]: "Phone",
                df.columns[9]: "Cell",
                df.columns[10]: "Schedule Status",
                df.columns[11]: "Builders Risk Insurance",
                df.columns[12]: "Map Status",
                df.columns[13]: "Price/Sqft",
                df.columns[14]: "Total Sqft",
                df.columns[15]: "CC Limit",
                df.columns[16]: "ACH Limit",
                df.columns[17]: "Owner Email",
            }

            df = df.rename(columns=mapping)
            df['Lot Number'] = df['Job Name']
            df['Lot Number'] = df['Lot Number'].str.replace("(_).*", "")
            df['Lot Number'] = df['Lot Number'].str.replace("( ).*", "")

            df.to_sql('BTSuperRaw', con=engine,
                      if_exists='append', index=False)
            if curPage < lastPage:
                nextArrow = wait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'ant-pagination-next')))
                nextArrow.click()
                time.sleep(5)
                jsReady(driver)

    except Exception as error:
        error_string = "Here's the current page: " + \
            curPage+" Here's the error: "+str(error)
        ErrorEmail(error_string)
