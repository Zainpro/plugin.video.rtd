# -*- coding=utf8 -*-
#******************************************************************************
# Scraper.py
#------------------------------------------------------------------------------
# RTD
#******************************************************************************
import re
import urllib.request
from urllib.request import urlopen

from resources.lib.Config import Config

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3" 

class Scraper(object):

    CATEGORY_URL = {
        "On-air":       Config.RTD_URL_ON_AIR,
        "Films":        Config.RTD_URL_FILMS,
        "Series":       Config.RTD_URL_SERIES,
        "Shows":        Config.RTD_URL_SHOWS
    }
#    Extracts film title, poster url and href page url     
    _REGEX_films_page_list = re.compile(r'for__name">(.*?)<[\s\S]*?<div class="film_data_container"[\s\S]*?image: url\(\'(.*?)\'\)[\s\S]*?href="(.*?)">watch film<',re.DOTALL)

    def get_streams_page_in_a_string(self, url):
#        print("URL:", url)  # Add this line for debugging
        headers = {"User-Agent": USER_AGENT}
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req)
        streams_page = response.read().decode("utf-8")
        return streams_page                      
                                                   
                  


