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
        "Shows":        Config.RTD_URL_SHOWS,
        "More":         Config.RT_URL_MORE
    }
#    Extracts title, films poster and href page url     
    _REGEX_films_page_list = re.compile(r'for__name">(.*?)<[\s\S]*?<div class="film_data_container"[\s\S]*?image: url\(\'(.*?)\'\)[\s\S]*?href="(\/films.*?)">watch film<',re.DOTALL)

#    Extracts series poster, href page url and title  
    _REGEX_series_page_list = re.compile(r'<li class="list-2__item">[\s\S]*?url\(\'(.*?)\'\)"><\/div>[\s\S]*?href="(\/series.*?)">(.*?)<\/a>',re.DOTALL)
    
#    Extracts shows poster, href page url and title  
    _REGEX_shows_page_list = re.compile(r'<li class="list-2__item">[\s\S]*?url\(\'(.*?)\'\)"><\/div>[\s\S]*?href="(\/shows.*?)">(.*?)<\/a>',re.DOTALL)

#    Extracts more poster url, title, and href page url    
    _REGEX_more_page_list = re.compile(r'<noscript><img src="(.*?)" class="media__item media__item_ratio [^"]*" alt="([^"]*?)".*?><strong class="card__header card__header_effect-sadie"><a class="link link_hover" href="(.*?)">',re.DOTALL)    

    def get_streams_page_in_a_string(self, url):
        headers = {"User-Agent": USER_AGENT}
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req)
        streams_page = response.read().decode("utf-8")
        return streams_page                      
                                                   
                  


