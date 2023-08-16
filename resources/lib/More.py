# -*- coding=utf8 -*-
#******************************************************************************
# More.py
#------------------------------------------------------------------------------
# RTD
#******************************************************************************              
import re
import os
import urllib.request
from urllib.request import urlopen
from urllib.parse import urlparse

from resources.lib.Config import Config
from resources.lib.Scraper import Scraper


USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"    
USER_AGENT2 = "Mozilla/5.0 (iPad; CPU OS 8_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B410 Safari/600.1.4"
USER_AGENT3 = "User-Agent=Mozilla/5.0 (iPad; CPU OS 8_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B410 Safari/600.1.4"
                
class More(Scraper):
    
    def __init__(self):
        super(More, self).__init__()
       
    def more_page_main(self, category):
        "Provides a list of more"
        result = self._REGEX_more_page_list.findall(self._get_all_more_page(category))
        return result   
    
    def _get_all_more_page(self, category):
        "Returns all the more homepage in a string."
        url = self.CATEGORY_URL[category]
        return self.get_streams_page_in_a_string(url) 

class Scraper_Events:    
    def get_events_page_in_a_string(self, url):
        "Gets events list per serie"    
        headers = {"User-Agent": USER_AGENT}
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req)
        more_page = response.read().decode("utf-8")
        return more_page         
    
class Events(Scraper_Events):
    "Provides events list per serie (poster url, show title,  and href page url)"    
    _REGEX_events_page_list = re.compile(r'noscript pattern --><noscript><img src="([^"]+)" class="media__item media__item_ratio " alt="([^"]+)" \/><\/noscript><\/a><\/div><\/div><\/div><strong class="card__header card__header_vertical_padding-to-low"><a class="link link_hover" href="([^"]+)" >',re.DOTALL)    
      
    def events_list(self, streams_page):
        events_list = self._REGEX_events_page_list.findall(streams_page)
        return events_list           
        
class More_MP4:    
    def get_event_player_page_in_a_string(self, url):
        "Gets video link from each events_player page"
        headers = {"User-Agent": USER_AGENT}
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req)
        event_page = response.read().decode("utf-8")
        return event_page    
    
class Events2(More_MP4):
    _REGEX_Video_link = re.compile(r'"og:video" content="(.*?)"\/>', re.DOTALL)
    
    def mp4_url_link(self, events_page):
        mp4_url = self._REGEX_Video_link.findall(events_page)
        return mp4_url        
        
        
        
        
        