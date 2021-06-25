# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 10:12:50 2021

@author: User
"""

from selenium import webdriver
driver = webdriver.Chrome()
driver.get("https://wms.firstbank.com.tw/ETFWeb/HTML/ETKMDJNEWS.DJHTM#TYPE=3&PAGE=1")
element = driver.find_element_by_xpath('//*[@id="datepickerS"]')
element2=driver.find_element_by_xpath('//*[@id="datepickerE"]')
element3=driver.find_element_by_xpath('//*[@id="selCount"]')
button = driver.find_element_by_xpath('//*[@id="SysJustIFRAMEDIV"]/form/input')
import time
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import numpy as np

news_list=[]

from datetime import datetime
from tqdm import tqdm

datelist = pd.Series(pd.bdate_range(start="2015-01-23",end="2019-12-31").date).astype(str).str.replace('-','/').to_list()

for d in tqdm(datelist):
    tag=0
    try:
        element2.clear()
    except:
        driver.switch_to_alert().accept() 
    time.sleep(1)
    while tag==0:
        try:
            element2.send_keys(str(d))
            tag=1
        except:
            pass
            
    try:
        element.clear()
    except:
        driver.switch_to_alert().accept()
    tag=0
    while tag==0:
        try:
            element.send_keys(str(d))
            tag=1
        except:
            pass
    element3.send_keys('50')
    time.sleep(1)
    action = ActionChains (driver)
    action.move_by_offset(0, 0).click().perform()
    button.click()
    
    #craw_table
    
    table=driver.find_element_by_xpath('//*[@id="dataTbl"]')
    l=table.text
    lista=l.split('\n')
    lista.pop(0)
    news_list.append(lista)
    


#news_list_to_dataframe and do the data cleaning
all_news=[]
for news in news_list:
    for n in news:
       all_news.append(n)
       
a=all_news.remove('處理中...')
data=pd.DataFrame(all_news,columns=['all_information'])
data['hot']=data['all_information'].str.rsplit(' ',1).str[-1]
data['date']=data['all_information'].str.split(' ',1).str[0]
data['time']=data['all_information'].str.split(' ',2).str[1]

def title(x):
     return str(x['all_information']).strip(str(x['hot'])).strip(str(x['date'])).strip(str(x['time']))
  
data['title']=data.apply(title,axis=1)
data['title']=data['title'].str.split(' ',2).str[2]  
data[['date','time','title','hot']].to_csv('news_data.csv',index=False,encoding='utf-8-sig')   
