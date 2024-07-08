from selenium import webdriver 
from selenium.webdriver.common.by import By
import datetime
import time
import csv
import zipfile
import os
# import extract

def download_data():
    def mmm(mon):
        switcher = {
            1: "Jan",
            2: "Feb",
            3: "Mar",
            4: "Apr",
            5: "May",
            6: "Jun",
            7: "Jul",
            8: "Aug",
            9: "Sep",
            10: "Oct",
            11: "Nov",
            12: "Dec"
        }
        return switcher.get(mon, "error")

    def ddd(maxdays):
        switcher = {
            1: 31,
            2: 28,
            3: 31,
            4: 30,
            5: 31,
            6: 30,
            7: 31,
            8: 31,
            9: 30,
            10: 31,
            11: 30,
            12: 31
        }
        return switcher.get(maxdays, "error")
    # to pad no. with a 0 for appropriate i/p
    def padding(arg):
        switcher = {
            0: "0", 
            1: "01", 
            2: "02", 
            3: "03", 
            4: "04", 
            5: "05", 
            6: "06", 
            7: "07", 
            8: "08", 
            9: "09", 
            11: '11'}
        return switcher.get(arg, "error")
    
    
    file = "D:\SummAR_24-25\Electron-Accelerator-Summer2024-25-project-\Project venv\Web scrape\BPI.csv"
    preferences = {"download.default_directory": "D:\\SummAR_24-25\\Electron-Accelerator-Summer2024-25-project-\\Project venv\\Web scrape\\DB\\BPI"}
    options.add_experimental_option("prefs", preferences)
    driver = webdriver.Chrome(executable_path=r'D:\SummAR_24-25\Electron-Accelerator-Summer2024-25-project-\Project venv\Web scrape\chromedriver.exe', chrome_options=options)
    driver.get('http://srs2.cat.ernet.in:8100/servlet/Indus2BPIDataDownloadFormHA')
    
    hours = driver.find_element(By.XPATH ,
                                '/html/body/center/table/tbody/tr/td/form/center[2]/table/tbody/tr[2]/td[4]/select')
    hours.click()
    hours.send_keys('0')
    time.sleep(1)
    
    min = driver.find_element(By.XPATH , 
                              '/html/body/center/table/tbody/tr/td/form/center[2]/table/tbody/tr[2]/td[5]/select')
    min.click()
    min.send_keys('0')
    time.sleep(1)
    
    timeduration = driver.find_element(By.XPATH,
        '/html/body/center/table/tbody/tr/td/form/center[1]/table/tbody/tr/td[4]/select')
    timeduration.click()
    timeduration.send_keys('4 hrs')
    time.sleep(1)
    
    current_time = datetime.datetime.now()
    present_month_key = current_time.month - 1
    present_day =  current_time.day
    
    present_month_value = mmm(present_month_key) # from numeric to half month name using fxn above mmm
    
    selected_month = driver.find_element(By.XPATH,
        '/html/body/center/table/tbody/tr/td/form/center[3]/table/tbody/tr[2]/td[2]/select')
    selected_month.click()
    selected_month.send_keys(present_month_value)
    time.sleep(1)
    
    t_day = present_day
    hour_batch={0 , 4,8,12,16,20}
    maxdays = ddd(present_month_value)
    while t_day <= maxdays:
        if t_day < 10 :
            day = padding(t_day)
        else:
            day = str(t_day)
        date = day + present_month_value + '2024'
                
    