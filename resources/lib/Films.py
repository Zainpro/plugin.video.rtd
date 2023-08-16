# -*- coding=utf8 -*-
#******************************************************************************
# Films.py
#------------------------------------------------------------------------------
# RTD
#******************************************************************************             
import re
import urllib.request
from urllib.request import urlopen
from urllib.parse import urlparse

from resources.lib.Config import Config
from resources.lib.Scraper import Scraper

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"    
USER_AGENT2 = "Mozilla/5.0 (iPad; CPU OS 8_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B410 Safari/600.1.4"
USER_AGENT3 = "User-Agent=Mozilla/5.0 (iPad; CPU OS 8_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B410 Safari/600.1.4"
       
class Films(Scraper):
    
    def __init__(self):
        super(Films, self).__init__()

    def films_page_list(self, category):
        "Provides a list of films title, poster and href"
        result = self._REGEX_films_page_list.findall(self._get_all_films_page(category))
        return result  
    
    def _get_all_films_page(self, category):
        "Returns all the films homepage in a string."
        url = self.CATEGORY_URL[category]
        return self.get_streams_page_in_a_string(url) 
            
class Scraper2:    
    def get_film_page_in_a_string(self, url):
        headers = {"User-Agent": USER_AGENT}
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req)
        film_page = response.read().decode("utf-8")
        return film_page 
     
class Films2(Scraper2):
    _REGEX_Video_link = re.compile(r"file:\s*'([^']+\.mp4)'", re.DOTALL)
    
    def mp4_url_link(self, film_page):
        mp4_url = self._REGEX_Video_link.findall(film_page)
        return mp4_url

           
        