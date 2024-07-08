


from selenium.webdriver.common.by import By
from selenium import webdriver
import datetime
import time
import csv
import zipfile
import os
import extract

fields = ['DATE', 'TIME', 'FOUND']
options = webdriver.ChromeOptions()
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
        switcher = {0: "0", 1: "01", 2: "02", 3: "03", 4: "04", 5: "05", 6: "06", 7: "07", 8: "08", 9: "09", 11: '11'}
        return switcher.get(arg, "error")


file = "D:\summer 2023\Sanskar\AboutDataBPI.csv"
preferences = {"download.default_directory": "D:\\summer 2023\\Sanskar\\dataplace\\BPI"}
options.add_experimental_option("prefs", preferences)
driver = webdriver.Chrome(executable_path=r'D:\summer 2023\Sanskar\chromedriver.exe', chrome_options=options)
driver.get('http://srs2.cat.ernet.in:8100/servlet/Indus2BPIDataDownloadFormHA')

hours = driver.find_element(By.XPATH,
        '/html/body/center/table/tbody/tr/td/form/center[2]/table/tbody/tr[2]/td[4]/select')
hours.click()
hours.send_keys('0')
time.sleep(1)

min = driver.find_element(By.XPATH,
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
p_month = 6  # current_time.month - 1
day = 12  # current_time.day

    # from numeric to half month name using fxn above mmm
c_month = p_month
c_month = mmm(c_month)

sel_month = driver.find_element(By.XPATH,
        '/html/body/center/table/tbody/tr/td/form/center[2]/table/tbody/tr[2]/td[2]/select')
sel_month.click()
    sel_month.send_keys(c_month)
    time.sleep(1)

    t_day = day  # temp day is t_day
    hh = {0, 4, 8, 12, 16, 20}
    maxdays = ddd(p_month)
    while t_day <= maxdays:
        if t_day < 10:
            day1 = padding(t_day)
        else:
            day1 = str(t_day)
        date = day1 + c_month + '2023'
        if os.path.isfile('D:\\summer 2023\\Sanskar\\extracted\\BPI\\' + 'BPI' + date + '.csv'):
            t_day += 1
            continue
        if t_day == 22:
            t_day += 1
            day1 = '222'
        for h in hh:
            try:
                if h < 10:
                    hr = padding(h)
                else:
                    hr = str(h)
                hours = driver.find_element(By.XPATH,
                    '/html/body/center/table/tbody/tr/td/form/center[2]/table/tbody/tr[2]/td[4]/select')
                hours.click()
                hours.send_keys(hr)
                # time.sleep(1)


                sel_day = driver.find_element(By.XPATH,
                    '/html/body/center/table/tbody/tr/td/form/center[2]/table/tbody/tr[2]/td[1]/select')
                sel_day.click()
                sel_day.send_keys(day1)
                # time.sleep(1)
                time.sleep(2)

                driver.find_element(By.XPATH, '/html/body/center/table/tbody/tr/td/form/center[3]/input[1]').click()
                driver.find_element(By.XPATH, '/html/body/center/table/tbody/tr/td/form/center[3]/input[2]').click()
                csvData = [{'DATE': day1 + c_month + '2023', 'TIME': hr + '00 hrs', 'FOUND': 'YES'}]
                with open(file, 'a') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=fields)

                    writer.writerows(csvData)
                sel_month = driver.find_element(By.XPATH,
                    '/html/body/center/table/tbody/tr/td/form/center[2]/table/tbody/tr[2]/td[2]/select')
                sel_month.click()
                sel_month.send_keys(c_month)
                # time.sleep(1)

                timeduration = driver.find_element(By.XPATH,
                    '/html/body/center/table/tbody/tr/td/form/center[1]/table/tbody/tr/td[4]/select')
                timeduration.click()
                timeduration.send_keys('4 hrs')
                # time.sleep(1)

                min = driver.find_element(By.XPATH,
                    '/html/body/center/table/tbody/tr/td/form/center[2]/table/tbody/tr[2]/td[5]/select')
                min.click()
                min.send_keys('0')
                # time.sleep(1)
            except:
                driver.find_element(By.XPATH, '/html/body/center[2]/a/h2/b').click()
                csvData = [{'DATE': day1 + c_month + '2023', 'TIME': hr + '00 hrs', 'FOUND': 'NO'}]
                with open(file, 'a') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=fields)
                    writer.writerows(csvData)
        try:
            src = "D:\\summer 2023\\Sanskar\\dataplace\\BPI"
            save = "D:\\summer 2023\\Sanskar\\extracted\\temp5"

            extension = ".zip"

            os.chdir(src)
            for item in os.listdir(src):
                if item.endswith(extension):
                    file_name = os.path.abspath(item)  # to get full path
                    zip_ref = zipfile.ZipFile(file_name)
                    zip_ref.extractall(save)
                    zip_ref.close()
            if t_day < 10:
                day1 = padding(t_day)
            else:
                day1 = str(t_day)
            extract.ex(day1, c_month, save, index)
        except:
            print('no data')
        t_day = t_day + 1

    p_month = p_month + 1
    driver.find_element(By.XPATH, '/html/body/center/table/tbody/tr/td/form/center[3]/input[2]').click()  # refresh

    c_month = p_month
    c_month = mmm(c_month)

    sel_month = driver.find_element(By.XPATH,
        '/html/body/center/table/tbody/tr/td/form/center[2]/table/tbody/tr[2]/td[2]/select')
    sel_month.click()
    sel_month.send_keys(c_month)
    time.sleep(1)

    t_day = 1

    while t_day <= day:
        if t_day < 10:
            day1 = padding(t_day)
        else:
            day1 = str(t_day)
        date = day1 + c_month + '2023'
        if os.path.isfile('D:\\summer 2023\\Sanskar\\extracted\\BPI\\' + 'BPI' + date + '.csv'):
            t_day += 1
            continue
        if t_day == 22:
            t_day += 1
            continue
        for h in hh:

            try:
                if h < 10:
                    hr = padding(h)
                else:
                    hr = str(h)

                hours = driver.find_element(By.XPATH,
                    '/html/body/center/table/tbody/tr/td/form/center[2]/table/tbody/tr[2]/td[4]/select')
                hours.click()
                hours.send_keys(hr)
                # time.sleep(1)

                sel_day = driver.find_element(By.XPATH,
                    '/html/body/center/table/tbody/tr/td/form/center[2]/table/tbody/tr[2]/td[1]/select')
                sel_day.click()
                sel_day.send_keys(day1)
                # time.sleep(1)
                time.sleep(2)
                driver.find_element(By.XPATH,
                    '/html/body/center/table/tbody/tr/td/form/center[3]/input[1]').click()  # download
                driver.find_element(By.XPATH,
                    '/html/body/center/table/tbody/tr/td/form/center[3]/input[2]').click()  # refresh
                csvData = [{'DATE': day1 + c_month + '2023', 'TIME': hr + '00 hrs', 'FOUND': 'YES'}]
                with open(file, 'a') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=fields)
                    writer.writerows(csvData)

                sel_month = driver.find_element(By.XPATH,
                    '/html/body/center/table/tbody/tr/td/form/center[2]/table/tbody/tr[2]/td[2]/select')
                sel_month.click()
                sel_month.send_keys(c_month)
                # time.sleep(1)


                timeduration = driver.find_element(By.XPATH,
                    '/html/body/center/table/tbody/tr/td/form/center[1]/table/tbody/tr/td[4]/select')
                timeduration.click()
                timeduration.send_keys('4 hrs')
                # time.sleep(1)

                min = driver.find_element(By.XPATH,
                    '/html/body/center/table/tbody/tr/td/form/center[2]/table/tbody/tr[2]/td[5]/select')
                min.click()
                min.send_keys('0')
                # time.sleep(1)
            except:
                driver.find_element(By.XPATH, "/html/body/center[2]/a/h2/b ").click()
                csvData = [{'DATE': day1 + c_month + '2023', 'TIME': hr + '00 hrs', 'FOUND': 'NO'}]
                with open(file, 'a') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=fields)
                    writer.writerows(csvData)

        src = "D:\\summer 2023\\Sanskar\\dataplace\\BPI"
        save = "D:\\summer 2023\\Sanskar\\extracted\\temp5"
        extension = ".zip"
        try:
            os.chdir(src)
            for item in os.listdir(src):
                if item.endswith(extension):
                    file_name = os.path.abspath(item)  # to get full path
                    zip_ref = zipfile.ZipFile(file_name)
                    zip_ref.extractall(save)
                    zip_ref.close()

            if t_day < 10:
                day1 = padding(t_day)
            else:
                day1 = str(t_day)
            extract.ex(day1, c_month, save, index)
        except:
            print('no data')

        t_day = t_day + 1