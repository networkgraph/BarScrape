# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 17:10:40 2016

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

#First section is sites for which we don't need to execute JS
eb_show_dicts = []
schubas_lh_show_dicts = []

def empty_bottle_events():
    def eb_soup(url):   #Note that this function is not used for all bars
        html = urlopen(url).read()
        return BeautifulSoup(html,"lxml")
    soup = eb_soup("http://emptybottle.com/")

    def eb_span_info(span_class):
        infos = [info.string for info in soup.findAll("span",span_class)]
        return infos
        
    prices = eb_span_info("show_price")
    dates = eb_span_info("tw-event-date")
    times = eb_span_info("tw-event-time")
    
    #Note this pulls only the top artist for each night
    artist_lists = soup.findAll("span","show_artists")
    artists = [(artist_list.find("li")).string for artist_list in artist_lists]
    

    for index, price in enumerate(prices):
        show_dict = {"venue":"Empty Bottle","artist": artists[index],"date": dates[index],"time": times[index],"price": prices[index]}
        eb_show_dicts.append(show_dict)
    return eb_show_dicts




#This section is sites for which we need to execute JS - i.e., we need Selenium
def tfly_event_ids(url,list_name):
    html = urlopen(url).read()
    html_string = html.decode("utf-8")
    for m in re.finditer('one-event last-event',html_string):
        end = m.end()
        a = html_string[end:(end+25)]
        b = ''.join(ele for ele in a if ele.isdigit())
        list_name.append(b)
        
def tfly_event_info(event_id,driver,venue):
    seen_div = driver.find_element_by_id("tfly-event-id-"+event_id)
    seen_div.click()

    unseen_div = WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.CLASS_NAME,"richcal-event-info"))
    )

    inner_html = unseen_div.get_attribute('innerHTML')
    soup = BeautifulSoup(inner_html,'lxml')
    
    artist = soup.find("div",class_="richcal-headliners").text
    date = soup.find("div",class_="richcal-dates").text
    time = soup.find("div",class_="richcal-times").text
    price = soup.find("div",class_="richcal-ticket-price").text
    
    show_dict = {"venue":venue,"artist":artist,'date':date,'time':time,'price':price}
    return show_dict
    
def tfly_events(url,venue):
    driver = webdriver.PhantomJS()
    driver.get(url)
    
    event_ids = []
    tfly_event_ids(url,event_ids)
    
    event_dicts = []
    for event in event_ids:
        event_info = tfly_event_info(event,driver,venue)
        event_dicts.append(event_info)        
        
    driver.close()
    return event_dicts

event_dicts = tfly_events("http://www.beatkitchen.com/calendar/","Beat Kitchen") + tfly_events("http://www.subt.net/calendar/","Subterranean") +  empty_bottle_events() + schubas_lh_events()
print(event_dicts)