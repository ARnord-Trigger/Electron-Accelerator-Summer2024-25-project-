from selenium import webdriver 
from selenium.webdriver.common.by import By
import datetime
import time
import csv
import zipfile
import os
import pandas as pd
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
    
    def looping_over_time( *list  ):
        for lst in list:
            tab_clicker(path= lst[0] , keys= lst[1] , sleep_time= lst[2])
    # links to all infonet data
    RRCAT_infonet_dict = {'BPI_data':'http://srs2.cat.ernet.in:8100/servlet/Indus2BPIDataDownloadFormHA',
                          'Beam current & Beam energy' : 'http://srs2.cat.ernet.in/srsha/srs.htm'  }
    #essential folder used in scarping
    folder_path_dict = {'Extracted/Merged_BPI' : 'D:\SummAR_24-25\Electron-Accelerator-Summer2024-25-project-\Project venv\Web scrape\Extracted\Zip_BPI',
                        'Extracted/Extracted_BPI' : 'D:\\SummAR_24-25\\Electron-Accelerator-Summer2024-25-project-\\Project venv\\Web scrape\\Extracted\\Extracted_BPI',
                        'DB/BPI' : 'D:\\SummAR_24-25\\Electron-Accelerator-Summer2024-25-project-\\Project venv\\Web scrape\\DB\\BPI',
                        'DB/BC&BE' : 'D:\\SummAR_24-25\\Electron-Accelerator-Summer2024-25-project-\\Project venv\\Web scrape\\DB\\BC_BE'}
    
    # Chromedriver and other important files
    file_path_dict = {'BPI_data_status_csv'   : 'D:\SummAR_24-25\Electron-Accelerator-Summer2024-25-project-\Project venv\Web scrape\BPI_data_status.csv',
                      'Chromedriver_exe' : r'D:\SummAR_24-25\Electron-Accelerator-Summer2024-25-project-\Project venv\Web scrape\chromedriver.exe'}
    
    #All BPI_xpaths included here
    BPI_XPATH_dict = {'hour_tab' :'/html/body/center/table/tbody/tr/td/form/center[2]/table/tbody/tr[2]/td[4]/select',
                      'min_tab' : '/html/body/center/table/tbody/tr/td/form/center[2]/table/tbody/tr[2]/td[5]/select',
                      'time_duration_tab' : '/html/body/center/table/tbody/tr/td/form/center[1]/table/tbody/tr/td[4]/select',
                      'sample_rate_tab' : '/html/body/center/table/tbody/tr/td/form/center[1]/table/tbody/tr/td[2]/select',
                      'date_tab' : '/html/body/center/table/tbody/tr/td/form/center[2]/table/tbody/tr[2]/td[1]/select',
                      'month_tab' : '/html/body/center/table/tbody/tr/td/form/center[2]/table/tbody/tr[2]/td[2]/select',
                      'year_tab' : '/html/body/center/table/tbody/tr/td/form/center[2]/table/tbody/tr[2]/td[3]/select',
                      'refresh_tab' : '/html/body/center/table/tbody/tr/td/form/center[3]/input[2]',
                      'download_tab' : '/html/body/center/table/tbody/tr/td/form/center[3]/input[1]'}
    
    options = webdriver.ChromeOptions()
    file = file_path_dict['BPI_data_status_csv']
    preferences = {"download.default_directory": folder_path_dict['DB/BPI']}
    options.add_experimental_option("prefs", preferences)
    driver = webdriver.Chrome(executable_path=file_path_dict['Chromedriver_exe'], chrome_options=options)
    driver.get(RRCAT_infonet_dict['BPI_data'])
       
    
    #setting current day and prev month 
    #prev month is chosen because we need to iterate from ith day of prv month to ith day of current month 
    current_time = datetime.datetime.now()
    prev_month_key = current_time.month - 1
    present_day =  current_time.day
    
    # from numeric to half month name using fxn above mmm
    prev_month_value = mmm(prev_month_key) 
    present_month_value =mmm(current_time.month)
    # selecting month
    # tab_clicker(path = BPI_XPATH_dict['month_tab'] , keys = prev_month_value , sleep_time = 1)
    
    hour_batch={0,4,8,12,16,20}
    
    #t_day is temp day
    #this part runs from present day of prev month to last day of prev month 
    t_day = present_day
    maxdays = ddd(prev_month_value)
    while t_day <= maxdays:
        if t_day < 10 :
            day = padding(t_day)
        else:
            day = str(t_day)
        date = day + prev_month_value + '2024'
        
        if os.path.isfile(folder_path_dict['Extracted/Merged_BPI'] + 'BPI' + date + '.csv'):
            t_day += 1
            continue
        if t_day == 22:
            t_day += 1
            day = '222'
            
        for h in hour_batch:
            try:
                if h < 10:
                    hr = padding(h)
                else:
                    hr = str(h)
                looping_over_time([BPI_XPATH_dict['hour_tab'] , hr , 0],
                                  [BPI_XPATH_dict['min_tab'] ,'0', 1 ],
                                  [BPI_XPATH_dict['date_tab'] , day , 2 ],
                                  [BPI_XPATH_dict['month_tab'] , prev_month_value , 0],
                                  [BPI_XPATH_dict['time_duration_tab'] , '4 hrs' , 0],
                                  [BPI_XPATH_dict['download_tab'] , None , 0],
                                  [BPI_XPATH_dict['refresh_tab'] , None , 0])
                
                csvData = [{'DATE': day + prev_month_value + '2023', 'TIME': hr + '00 hrs', 'FOUND': 'YES'}]
                with open(file, 'a') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=fields)
                    writer.writerows(csvData)
            except:
                tab_clicker(path='/html/body/center[2]/a/h2/b')
                csvData = [{'DATE': day + prev_month_value + '2023', 'TIME': hr + '00 hrs', 'FOUND': 'NO'}]
                with open(file, 'a') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=fields)
                    writer.writerows(csvData)
        
        # Define the paths
        zip_folder = folder_path_dict['DB/BPI']
        extract_folder = folder_path_dict['Extracted/Extracted_BPI']
        output_folder = folder_path_dict['Extracted/Merged_BPI']
        merged_file = folder_path_dict['Extracted/Merged_BPI'] + 'BPI' + date + '.csv'
        # creating csv at location merged_file
        empty_df = pd.DataFrame()
        empty_df.to_csv(os.path.join(output_folder, merged_file), index=False)
        # Extract CSV files from the ZIP files
        for zip_file in os.listdir(zip_folder):
            if zip_file.endswith('.zip'):
                with zipfile.ZipFile(os.path.join(zip_folder, zip_file), 'r') as zip_ref:
                    zip_ref.extractall(extract_folder)
        # List all extracted CSV files
        csv_files = [os.path.join(extract_folder, f) for f in os.listdir(extract_folder) if f.endswith('.csv')]
        # Merge the CSV files along columns
        merged_df = pd.concat([pd.read_csv(f) for f in csv_files], axis=1)
        # Save the merged dataframe to the output folder
        merged_df.to_csv(os.path.join(output_folder, merged_file), index=False)
        print(f"Merged file saved to {os.path.join(output_folder, merged_file)}")
        t_day +=1
    
    t_day = 1
    maxdays = ddd(present_month_value)
    while t_day <= present_day:
        if t_day < 10 :
            day = padding(t_day)
        else:
            day = str(t_day)
        date = day + present_month_value + '2024'
        
        if os.path.isfile(folder_path_dict['Extracted/Merged_BPI'] + 'BPI' + date + '.csv'):
            t_day += 1
            continue
        if t_day == 22:
            t_day += 1
            day = '222'
            
        for h in hour_batch:
            try:
                if h < 10:
                    hr = padding(h)
                else:
                    hr = str(h)
                looping_over_time([BPI_XPATH_dict['hour_tab'] , hr , 0],
                                  [BPI_XPATH_dict['min_tab'] ,'0', ]
                                  [BPI_XPATH_dict['date_tab'] , day , 2 ],
                                  [BPI_XPATH_dict['month_tab'] , present_month_value , 0],
                                  [BPI_XPATH_dict['time_duration_tab'] , '4 hrs' , 0],
                                  [BPI_XPATH_dict['download_tab'] , None , 0],
                                  [BPI_XPATH_dict['refresh_tab'] , None , 0])
                
                csvData = [{'DATE': day + present_month_value + '2023', 'TIME': hr + '00 hrs', 'FOUND': 'YES'}]
                with open(file, 'a') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=fields)
                    writer.writerows(csvData)
            except:
                tab_clicker(path='/html/body/center[2]/a/h2/b')
                csvData = [{'DATE': day + present_month_value + '2023', 'TIME': hr + '00 hrs', 'FOUND': 'NO'}]
                with open(file, 'a') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=fields)
                    writer.writerows(csvData)
        
        # creating csv at location merged_file
        empty_df = pd.DataFrame()
        empty_df.to_csv(os.path.join(output_folder, merged_file), index=False)
        # Extract CSV files from the ZIP files
        for zip_file in os.listdir(zip_folder):
            if zip_file.endswith('.zip'):
                with zipfile.ZipFile(os.path.join(zip_folder, zip_file), 'r') as zip_ref:
                    zip_ref.extractall(extract_folder)
        # List all extracted CSV files
        csv_files = [os.path.join(extract_folder, f) for f in os.listdir(extract_folder) if f.endswith('.csv')]
        # Merge the CSV files along columns
        merged_df = pd.concat([pd.read_csv(f) for f in csv_files], axis=1)
        # Save the merged dataframe to the output folder
        merged_df.to_csv(os.path.join(output_folder, merged_file), index=False)
        print(f"Merged file saved to {os.path.join(output_folder, merged_file)}")    
        t_day +=1            
 
        
    
download_data()
        