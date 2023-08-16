# -*- coding=utf8 -*-
#******************************************************************************
# Shows.py
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
                
class Shows(Scraper):
    
    def __init__(self):
        super(Shows, self).__init__()
       
    def shows_page_main(self, category):
        "Provides a list of shows"
        result = self._REGEX_shows_page_list.findall(self._get_all_shows_page(category))
        return result   
    
    def _get_all_shows_page(self, category):
        "Returns all the shows homepage in a string."
        url = self.CATEGORY_URL[category]
        return self.get_streams_page_in_a_string(url) 

class Scraper_Chapters:    
    def get_chapters_page_in_a_string(self, url):
        "Gets chapters list per serie"    
        headers = {"User-Agent": USER_AGENT}
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req)
        shows_page = response.read().decode("utf-8")
        return shows_page         
    
class Chapters(Scraper_Chapters):
    "Provides chapters list per serie (href page, poster)"    
    _REGEX_chapters_page_list = re.compile(r'<li class="list-2__item">[\s\S]*?<a class="list-2__link" href="(\/shows.*?)">[\s\S]*?<div class="list-2__media">[\s\S]*?<div class="list-2__img" style="background-image: url\(\'(.*?)\'\)',re.DOTALL)    
      
    def chapters_list(self, streams_page):
        chapters_list = self._REGEX_chapters_page_list.findall(streams_page)
        return chapters_list           
        
class Shows_MP4:    
    def get_chapter_player_page_in_a_string(self, url):
        "Gets video link from each chapters_player page"
        headers = {"User-Agent": USER_AGENT}
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req)
        chapter_page = response.read().decode("utf-8")
        return chapter_page    
    
class Chapters2(Shows_MP4):
    _REGEX_Video_link = re.compile(r"file:\s*'([^']+\.mp4)'", re.DOTALL)
    
    def mp4_url_link(self, chapters_page):
        mp4_url = self._REGEX_Video_link.findall(chapters_page)
        return mp4_url        
        
        
        
        
        