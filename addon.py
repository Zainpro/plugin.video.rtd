# -*- coding=utf8 -*-
#******************************************************************************
# addon.py
#------------------------------------------------------------------------------
# RTD
#******************************************************************************
#This is 'addon.py':=>
import re
import os
import sys
import xbmc
import xbmcvfs
import xbmcgui
import xbmcaddon
import xbmcplugin
import urllib.parse
import urllib.request
import urllib.error
import sqlite3

from urllib.request import urlopen
from urllib.parse import unquote

from resources.lib.Config import Config
from resources.lib.Main import Films
from resources.lib.Main import Scraper2
from resources.lib.Main import Films2
from resources.lib.Texture13DB import Texture13DB

def get_test_viewer(s=''):### ADDON PATH TEST_VIEWER ###
	import xbmcgui
	xbmcgui.Dialog().textviewer('TEST_VIEWER',str(s))

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
PLUGIN_NAME = "plugin.video.rtd"
DB_FILMS_FILE = "rtd_films.db"
DB_FILMS = xbmcvfs.translatePath("special://profile/addon_data/%s/%s" % (PLUGIN_NAME, DB_FILMS_FILE))

class RTD(object):
    "XBMC-AddOn to access the main page of https://rtd.rt.com"

    _plugin_id = None
    _addon = None
    _streams = None
    icon = "icon.png"

    def __init__(self):
        "Initialize AddOn."
        self._register_addon()
        self._process_request()              
        
    def _register_addon(self):
        "Register AddOn."
        self._plugin_id = int(sys.argv[1])
        self._addon = xbmcaddon.Addon(id = Config.PLUGIN_NAME)    
        self._create_settings_file()

    def _process_request(self):
        "Identify and execute the user request."
        if sys.argv[2]:
            urlparam = sys.argv[2]
            if "film=" in urlparam:
                self._play_stream(urlparam)
            elif "category=" in urlparam:
                self._create_submenu_films(urlparam)
        else:
            self._create_submenu_category()                               
                              
    def _create_submenu_category(self):
        categories = [            
            (30130, "On-air"), 
            (30135, "Films"),
            (30140, "Series"),
            (30145, "Shows")
        ]
        items = []
        for (i18n, category) in categories:        
            url = sys.argv[0] + "?" + urllib.parse.urlencode({'category': category})
            item = xbmcgui.ListItem(category)
            items.append((url, item, True))
        xbmcplugin.addDirectoryItems(self._plugin_id, items)
        xbmcplugin.endOfDirectory(self._plugin_id)                                   
               
    def connect_films_db(self):
        """Connect to films database and create one if it does not exist."""
        db_con = sqlite3.connect(DB_FILMS)
        c = db_con.cursor()

        try:
            c.execute("SELECT * FROM films;")
        except sqlite3.OperationalError:
            c.execute("""CREATE TABLE films (
                            id INTEGER PRIMARY KEY,
                            title TEXT,
                            poster TEXT,
                            player_link TEXT
                         );""")
            db_con.commit()

        return db_con                                           
                             
    def _create_submenu_films(self, urlparam):
        Texture13DB.clean_database()    
        category = urlparam.split("=")[1]
        with self.connect_films_db() as db_con:
            c = db_con.cursor()        
            self._create_films_list(category, c, db_con)

    def _create_films_list(self, category, c, db_con):
        items = []
        for title, poster, href in Films().films_page_list(category):
            player_link = Config.RTD_URL + href

            c.execute("INSERT INTO films (title, poster, player_link) VALUES (?, ?, ?)", (title, poster, player_link))        
            db_con.commit()

            url = sys.argv[0] + "?" + urllib.parse.urlencode({'film': title})
            item = xbmcgui.ListItem(title)
            item.setArt({'icon': poster, 'poster': poster, 'banner': poster, 'fanart': ''})
            items.append((url, item, True))

        xbmcplugin.addDirectoryItems(self._plugin_id, items, len(items))
        xbmcplugin.endOfDirectory(self._plugin_id, cacheToDisc=True)
        xbmc.executebuiltin("Container.SetViewMode(500)")                                                                    
            
    def _play_stream(self, urlparam):
        "Play the stream corresponding to title."
        film = urlparam.split("=")[1]
        film = unquote(film) # decode the film title
        xbmc.log("Playing stream for film: {}".format(film), xbmc.LOGINFO)

        # connect to the database
        with self.connect_films_db() as db_con:
            xbmc.log("Connected to database", xbmc.LOGINFO)
            c = db_con.cursor()

            # execute the query to fetch the 'player_link' for the selected_title
            query = "SELECT player_link FROM films WHERE title = ?"
            c.execute(query, (film,))
            result = c.fetchone()
            xbmc.log("Executed query: {}".format(query), xbmc.LOGINFO)

        if result is not None and len(result) > 0:
            player_link = result[0]
            xbmc.log("Player link for {}: {}".format(film, player_link), xbmc.LOGINFO)
            scraper = Scraper2()
            film_page = scraper.get_film_page_in_a_string(player_link)
            xbmc.log("Fetched film page", xbmc.LOGINFO)

            films2 = Films2()
            mp4_url = films2.mp4_url_link(film_page)
            xbmc.log("Extracted MP4 URL: {}".format(mp4_url), xbmc.LOGINFO)

            if mp4_url:
                path = mp4_url[0]
                xbmc.log("MP4 URL for {}: {}".format(film, path), xbmc.LOGINFO)
                listitem = xbmcgui.ListItem(path=path)
                xbmc.log("Set path for listitem", xbmc.LOGINFO)
                xbmc.log("Resolved URL: {}".format(listitem.getPath()), xbmc.LOGINFO)
                xbmcplugin.setResolvedUrl(self._plugin_id, True, listitem)
            else:
                xbmc.log("Unable to find MP4 URL for {}".format(film), xbmc.LOGINFO)
        else:
            xbmc.log("No player link found for {}".format(film), xbmc.LOGINFO)
            
    def _cmd_settings(self):
        return "XBMC.RunScript(%s)" % (
            "%s/%s" % (self._get_base_dir(), Config.SCRIPT_SETTINGS)
        )                                                                                                                         

    def _create_settings_file(self):
        self._addon.setSetting("","")                                                                                                                         
                                                                                                                         
    def _get_base_dir(self):
        return os.path.dirname(__file__) 
                                                                                                                         

if __name__ == '__main__':
    plugin = RTD()
