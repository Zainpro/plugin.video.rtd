# -*- coding=utf8 -*-
#******************************************************************************
# Main.py
#------------------------------------------------------------------------------
# RTD
#******************************************************************************
# This is the "plugin.video.rtd/resources/lib/Main.py"   
             
import re
import urllib.request
from urllib.request import urlopen
from urllib.parse import urlparse

from resources.lib.Config import Config
from resources.lib.Scraper import Scraper


USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"    
        
class Films(Scraper):
    
    def __init__(self):
        super(Films, self).__init__()

    def films_page_list(self, category):
        "Provides a list of films title, poster and href"
        result = self._REGEX_films_page_list.findall(self._get_all_films_page(category))
        return result 

    @staticmethod 
    def get_thumbnail_base_url():   #No required
        "Provides the current base URL of the thumbnails"
        url = Films().films_page_list("Featured", 1)[0][1]
        return url[0:url.rfind("/")]    
    
    def _get_all_films_page(self, category):
        "Returns all the films homepage in a string."
        url = self.CATEGORY_URL[category]
        return self.get_streams_page_in_a_string(url) 
            
class Scraper2:    
    def get_film_page_in_a_string(self, url):
        headers = {"User-Agent": "Mozilla/5.0"}
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req)
        film_page = response.read().decode("utf-8")
        return film_page 
     
class Films2(Scraper2):
    _REGEX_Video_link = re.compile(r"file:\s*'([^']+\.mp4)'", re.DOTALL)
    
    def mp4_url_link(self, film_page):
        mp4_url = self._REGEX_Video_link.findall(film_page)
        return mp4_url

           
        