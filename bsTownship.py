# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 23:28:32 2016

@author: Al
"""
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import datetime
import calendar
import time

driver = webdriver.PhantomJS()
driver.set_window_size(1124, 850) #fake to convince python elements are visible
#Note that line below needs to be updated to something dynamic
driver.get("http://www.townshipchicago.com/events/?view=calendar&month=February-2016")
time.sleep(5)

html1 = driver.find_element_by_class_name('yui3-calendar-grid').get_attribute('outerHTML')
soup1 = BeautifulSoup(html1,'lxml')

driver.get("http://www.townshipchicago.com/events/?view=calendar&month=March-2016")
time.sleep(5)

html2 = driver.find_element_by_class_name('yui3-calendar-grid').get_attribute('outerHTML')
soup2 = BeautifulSoup(html2,'lxml')

driver.close()

##################
links1 = soup1.findAll('a',class_='background-image-link')
links2 = soup1.findAll('a',class_='item-link')

links3 = soup2.findAll('a',class_='background-image-link')
links4 = soup2.findAll('a',class_='item-link')

links = links1 + links2 + links3 + links4
for link in links:
    page = "http://www.townshipchicago.com"+link['href']
    page_html = urlopen(page).read()
    page_soup = BeautifulSoup(page_html,"lxml")
    artist_and_time = page_soup.find('div',class_ = 'sqs-block-content')
    print(artist_and_time)
    time.sleep(5)
