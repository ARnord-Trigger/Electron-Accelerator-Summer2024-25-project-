from selenium import webdriver 
from selenium.webdriver.common.by import By
import datetime
import time
import csv
import zipfile
import os
# import extract

def download_data():
    fields = ['DATE', 'TIME', 'FOUND']

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
            11: "11"}
        return switcher.get(arg, "error")
    
    def tab_clicker(path = None , keys = None , sleep_time = 0 ):
        if path:
            tab = driver.find_element(By.XPATH , path)
            tab.click()
            tab.send_keys(keys)
            time.sleep(sleep_time)
        else:
            pass          
    folder_path_dic = {'BPI_zip' : 'D:\SummAR_24-25\Electron-Accelerator-Summer2024-25-project-\Project venv\Web scrape\Extracted\Zip_BPI'}
    
    options = webdriver.ChromeOptions()
    file = "D:\SummAR_24-25\Electron-Accelerator-Summer2024-25-project-\Project venv\Web scrape\BPI.csv"
    preferences = {"download.default_directory": "D:\\SummAR_24-25\\Electron-Accelerator-Summer2024-25-project-\\Project venv\\Web scrape\\DB\\BPI"}
    options.add_experimental_option("prefs", preferences)
    driver = webdriver.Chrome(executable_path=r'D:\SummAR_24-25\Electron-Accelerator-Summer2024-25-project-\Project venv\Web scrape\chromedriver.exe', chrome_options=options)
    driver.get('http://srs2.cat.ernet.in:8100/servlet/Indus2BPIDataDownloadFormHA')
    
    #All xpaths included here
    XPATH_dict = {'hour_tab' :'/html/body/center/table/tbody/tr/td/form/center[2]/table/tbody/tr[2]/td[4]/select',
                 'min_tab' : '/html/body/center/table/tbody/tr/td/form/center[2]/table/tbody/tr[2]/td[5]/select',
                 'time_duration_tab' : '/html/body/center/table/tbody/tr/td/form/center[1]/table/tbody/tr/td[4]/select',
                 'sample_rate_tab' : '/html/body/center/table/tbody/tr/td/form/center[1]/table/tbody/tr/td[2]/select',
                 'date_tab' : '/html/body/center/table/tbody/tr/td/form/center[2]/table/tbody/tr[2]/td[1]/select',
                 'month_tab' : '/html/body/center/table/tbody/tr/td/form/center[2]/table/tbody/tr[2]/td[2]/select',
                 'year_tab' : '/html/body/center/table/tbody/tr/td/form/center[2]/table/tbody/tr[2]/td[3]/select',
                 'refresh_tab' : '/html/body/center/table/tbody/tr/td/form/center[3]/input[2]',
                 'download_tab' : '/html/body/center/table/tbody/tr/td/form/center[3]/input[1]'}
    
    
    
    #click hour_tab
    tab_clicker(path = XPATH_dict['hour_tab'] , keys ='0' , sleep_time = 1)
    #click minute_tab
    tab_clicker(path = XPATH_dict['min_tab'] , keys ='0' , sleep_time = 1)
    #click time_duration
    tab_clicker(path = XPATH_dict['time_duration_tab'] , keys ='4 hrs' , sleep_time = 1)    
    
    #setting current day and prev month 
    #prev month is chosen because we need to terate from ith day of prv month to ith day of current month 
    current_time = datetime.datetime.now()
    prev_month_key = current_time.month - 1
    present_day =  current_time.day
    
    # from numeric to half month name using fxn above mmm
    prev_month_value = mmm(prev_month_key) 
    
    # selecting month
    tab_clicker(path = XPATH_dict['month_tab'] , keys = prev_month_value , sleep_time = 1)
    
    #t_day is temp day
    t_day = present_day
    hour_batch={0,4,8,12,16,20}
    maxdays = ddd(prev_month_value)
    while t_day <= maxdays:
        if t_day < 10 :
            day = padding(t_day)
        else:
            day = str(t_day)
        date = day + prev_month_value + '2024'
        if os.path.isfile()        
    