# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 12:22:43 2016

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
"""
driver = webdriver.PhantomJS()
driver.set_window_size(1124, 850)
driver.get("http://www.lh-st.com/")
time.sleep(8)
seen_div = driver.find_element_by_css_selector('a.month:nth-child(2)')
seen_div.click()
time.sleep(8)
html = driver.find_element_by_id('allShows').get_attribute('outerHTML')
soup = BeautifulSoup(html,'lxml')
print(soup)
################
"""
schubas_lh_show_dicts = []
def schubas_lh_events():
    driver = webdriver.PhantomJS()
    driver.set_window_size(1124, 850) #fake to convince python elements are visible
    driver.get("http://www.lh-st.com/")
    
    def schubas_lh_soup(page):
        time.sleep(8)
        seen_div = driver.find_element_by_css_selector('a.month:nth-child('+page+')')
        seen_div.click()
        time.sleep(8)
        html = driver.find_element_by_id('allShows').get_attribute('outerHTML')
        soup = BeautifulSoup(html,'lxml')
        
        schubas_sections = soup.findAll('section',class_='showItem Schubas') + soup.findAll('section',class_='showItem Schubas free')
        lh_sections = soup.findAll('section',class_='showItem LincolnHall') + soup.findAll('section',class_='showItem LincolnHall almost')
        sections = [schubas_sections,lh_sections]        
        return sections
        
    def schubas_lh_info(venue,section_list):
        for section in section_list:
            date = section.findAll('strong')[1].nextSibling
            
            artist = section.find('h3',class_='primBand').text
            
            ticket_info = section.find('p','ticketInfo')
            strong_tag = ticket_info.findAll('strong')
            #for free shows, price is None
            price = strong_tag[0].string
            time = strong_tag[1].string
            
            show_dict = {"venue":venue,"artist":artist,'date':date,'time':time,'price':price}
            schubas_lh_show_dicts.append(show_dict)

    schubas_sections, lh_sections = schubas_lh_soup('2')
    schubas_lh_info("Schubas",schubas_sections)
    schubas_lh_info("LincolnHall",lh_sections)
    
    schubas_sections, lh_sections = schubas_lh_soup('3')
    schubas_lh_info("Schubas",schubas_sections)
    schubas_lh_info("LincolnHall",lh_sections)
    
    driver.close()
    
schubas_lh_events()
print(schubas_lh_show_dicts)
