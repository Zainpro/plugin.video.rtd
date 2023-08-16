# -*- coding=utf8 -*-
#******************************************************************************
# Series.py
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
       
class Series(Scraper):
    
    def __init__(self):
        super(Series, self).__init__()
       
    def series_page_main(self, category):
        "Provides a list of series"
        result = self._REGEX_series_page_list.findall(self._get_all_series_page(category))
        return result   
    
    def _get_all_series_page(self, category):
        "Returns all the series homepage in a string."
        url = self.CATEGORY_URL[category]
        return self.get_streams_page_in_a_string(url) 

class Scraper_Episodes:    
    def get_episodes_page_in_a_string(self, url):
        "Gets episodes list per serie"    
        headers = {"User-Agent": USER_AGENT}
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req)
        series_page = response.read().decode("utf-8")
        return series_page         
    
class Episodes(Scraper_Episodes):
    "Provides episodes list per serie (href page, poster)"        
    _REGEX_episodes_page_list = re.compile(r'<li class="list-2__item">\s*<a class="list-2__link" href="(\/series.*?)">[\s\S]*?<div class="list-2__media">\s*<div class="list-2__img" style="background-image: url\(\'(.*?.jpg)\'\)',re.DOTALL)     
      
    def episodes_list(self, streams_page):
        episodes_list = self._REGEX_episodes_page_list.findall(streams_page)
        return episodes_list           
        
class Series_MP4:    
    def get_episode_player_page_in_a_string(self, url):
        "Gets video link from each episode_player page"
        headers = {"User-Agent": USER_AGENT}
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req)
        episode_page = response.read().decode("utf-8")
        return episode_page    
    
class Episodes2(Series_MP4):
    _REGEX_Video_link = re.compile(r"file:\s*'([^']+\.mp4)'", re.DOTALL)
    
    def mp4_url_link(self, episode_page):
        mp4_url = self._REGEX_Video_link.findall(episode_page)
        return mp4_url        
        
        
        
        
        