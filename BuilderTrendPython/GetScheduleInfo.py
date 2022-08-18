from distutils.log import error
from turtle import down
from EmailTemplate import ErrorEmail
from ReadyState import jsReady
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
import os


def GettingScheduleInfo(driver, engine):
    try:
        delay = 10
        URLstring = os.getenv("SCHEDULE_URL")
        driver.get(URLstring)
        time.sleep(5)
        jsReady(driver)

        pageLst = wait(driver, .25).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="reactSchedulesListDiv"]/div/div/section/div[5]/div/div[2]/div/div/div/div/span/div')))
        pageLst.click()
        time.sleep(1)

        for i in range(15):
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

        curPage = wait(driver, delay).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="reactSchedulesListDiv"]/div/div/section/div[5]/div/div[2]/div/div/div/ul/li[2]/input')))
        curPage = curPage.get_attribute('value')
        curPage = int(re.sub("[^0-9]", "", curPage))

        lastPage = wait(driver, delay).until(EC.presence_of_element_located(
            (By.CLASS_NAME, 'ant-pagination-simple-pager')))
        lastPage = lastPage.text
        lastPage = int(re.sub("[^0-9]", "", lastPage))

        for i in range(lastPage):

            soup = BeautifulSoup(driver.page_source, 'lxml')
            htmltable = soup.find('div', {'class': 'ant-table-body'})
            df = pd.read_html(str(htmltable))
            df = df[0]
            df = df.astype(str)

            mapping = {
                df.columns[0]: "WTF is this column?",
                df.columns[1]: "Check Box",
                df.columns[2]: "Job",
                df.columns[3]: "Title",
                df.columns[4]: "Complete",
                df.columns[5]: "Phase",
                df.columns[6]: "Duration",
                df.columns[7]: "Start",
                df.columns[8]: "End",
                df.columns[9]: "Assignees",
                df.columns[10]: "Accepted",
                df.columns[11]: "Pending",
                df.columns[12]: "Declined",
                df.columns[13]: "Comments",
                df.columns[14]: "RFIs",
                df.columns[15]: "Home Symbol",
                df.columns[16]: "Predecessors"
            }

            df = df.rename(columns=mapping)

            df['Lot Number'] = df['Job']
            df['Lot Number'] = df['Lot Number'].str.replace("(_).*", "")
            df['Lot Number'] = df['Lot Number'].str.replace("( ).*", "")

            df.to_sql('BTScheduleRaw', con=engine,
                      if_exists='append', index=False)

            if curPage < lastPage:
                print("Page " + str((i + 1)) + "/" + str(lastPage))
                nextArrow = wait(driver, delay).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'ant-pagination-next')))
                nextArrow.click()
                time.sleep(5)
                jsReady(driver)
    except Exception as error:
        error_string = "Here's the page number: " + \
            curPage+" Here's the error: "+str(error)
        ErrorEmail(error_string)
