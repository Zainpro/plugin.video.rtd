# -*- coding=utf8 -*-
#******************************************************************************
# addon.py
#------------------------------------------------------------------------------
# RTD
#******************************************************************************
# Copyright (c) 2023-2027 Zainpro, El zipa <zainpro@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#******************************************************************************
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

from urllib.request import urlopen
from urllib.parse import unquote

from resources.lib.Onair import Onair

from resources.lib.Config import Config
from resources.lib.Films import Films
from resources.lib.Films import Scraper2
from resources.lib.Films import Films2

from resources.lib.Series import Series
from resources.lib.Series import Scraper_Episodes
from resources.lib.Series import Episodes
from resources.lib.Series import Series_MP4
from resources.lib.Series import Episodes2

from resources.lib.Shows import Shows
from resources.lib.Shows import Scraper_Chapters
from resources.lib.Shows import Chapters
from resources.lib.Shows import Shows_MP4
from resources.lib.Shows import Chapters2

from resources.lib.More import More
from resources.lib.More import Scraper_Events
from resources.lib.More import Events
from resources.lib.More import More_MP4
from resources.lib.More import Events2

from resources.lib.Texture13DB import Texture13DB

def get_test_viewer(s=''):### ADDON PATH TEST_VIEWER ###
	import xbmcgui
	xbmcgui.Dialog().textviewer('TEST_VIEWER',str(s))

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"    
USER_AGENT2 = "Mozilla/5.0 (iPad; CPU OS 8_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B410 Safari/600.1.4"
USER_AGENT3 = "User-Agent=Mozilla/5.0 (iPad; CPU OS 8_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B410 Safari/600.1.4"

try:
    from sqlite3 import dbapi2 as sqlite3
except:
    from pysqlite2 import dbapi2 as sqlite3


PLUGIN_NAME = "plugin.video.rtd"

db_path = os.path.join(xbmcvfs.translatePath("special://profile/addon_data/"), PLUGIN_NAME)
if not xbmcvfs.exists(db_path):
    xbmcvfs.mkdirs(db_path)

db_films_file = "rtd_series.db"
db_films = xbmcvfs.translatePath("special://profile/addon_data/%s/%s" % (PLUGIN_NAME, db_films_file))

db_series_file = "rtd_series.db"
db_series = xbmcvfs.translatePath("special://profile/addon_data/%s/%s" % (PLUGIN_NAME, db_series_file))

db_episodes_file = "rtd_episodes.db"
db_episodes = xbmcvfs.translatePath("special://profile/addon_data/%s/%s" % (PLUGIN_NAME, db_episodes_file))

db_shows_file = "rtd_shows.db"
db_shows = xbmcvfs.translatePath("special://profile/addon_data/%s/%s" % (PLUGIN_NAME, db_shows_file))

db_chapters_file = "rtd_chapters.db"
db_chapters = xbmcvfs.translatePath("special://profile/addon_data/%s/%s" % (PLUGIN_NAME, db_chapters_file))

db_more_file = "rt_more.db"
db_more = xbmcvfs.translatePath("special://profile/addon_data/%s/%s" % (PLUGIN_NAME, db_more_file))

db_events_file = "rt_events.db"
db_events = xbmcvfs.translatePath("special://profile/addon_data/%s/%s" % (PLUGIN_NAME, db_events_file))

class RTD(object):
    "XBMC-AddOn to access the page of https://rtd.rt.com"

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
        """Identify and execute the user request."""
        if sys.argv[2]:
            urlparam = sys.argv[2]            
            if "air=" in urlparam:
                self._play_air(urlparam)            
            elif "film=" in urlparam:
                self._play_film(urlparam)
            elif "episode=" in urlparam:
                self._play_episode(urlparam)
            elif "chapter=" in urlparam:
                self._play_chapter(urlparam)
            elif "event=" in urlparam:
                self._play_event(urlparam)                
            elif "serie=" in urlparam:
                self._create_submenu_episodes(urlparam)                  
            elif "show=" in urlparam:
                self._create_submenu_chapters(urlparam)
            elif "more=" in urlparam:
                self._create_submenu_events(urlparam)                
            elif "category=On_air" in urlparam:
                self._create_submenu_on_air(urlparam)             
            elif "category=Films" in urlparam:
                self._create_submenu_films(urlparam) 
            elif "category=Series" in urlparam:
                self._create_submenu_series(urlparam)            
            elif "category=Shows" in urlparam:
                self._create_submenu_shows(urlparam)
            elif "category=More" in urlparam:
                self._create_submenu_more(urlparam)                                           
        else:
            self._create_menu_category()                               
                              
    def _create_menu_category(self):
        categories = [            
            (30130, "On_air"), 
            (30135, "Films"),
            (30140, "Series"),
            (30145, "Shows"),
            (30150, "More")            
        ]
        items = []
        for (i18n, category) in categories:        
            url = sys.argv[0] + "?" + urllib.parse.urlencode({'category': category})
            item = xbmcgui.ListItem(category)
            items.append((url, item, True))
        xbmcplugin.addDirectoryItems(self._plugin_id, items)
        xbmcplugin.endOfDirectory(self._plugin_id) 

    def _create_submenu_on_air(self, urlparam):
        Texture13DB.clean_database()
        category = urlparam.split("=")[1]
        self._create_on_air_list(category)

    def _create_on_air_list(self, category):
        items = []
        for media in Onair.media_list(self):
            name = media['name']
            thumb = media['thumb']
            video_url = media['video'] 
            url = sys.argv[0] + "?" + urllib.parse.urlencode({'air': name})
            item = xbmcgui.ListItem(name)
            item.setArt({'icon': thumb, 'poster': thumb, 'banner': thumb, 'fanart': ''})
            item.setProperty('path', video_url)
            xbmcplugin.addDirectoryItem(self._plugin_id, url, item, len(items))

        xbmcplugin.endOfDirectory(self._plugin_id, cacheToDisc=True)

    def _play_air(self, urlparam):
        air = urlparam.split("=")[1]
        air = unquote(air)
        video_url = Onair.media_list(self)    
        path = xbmc.getInfoLabel('ListItem.Property(path)')

        listitem = xbmcgui.ListItem(path=path)
        listitem.setProperty('IsPlayable', 'true')
                
        req = urllib.request.Request(path)
        req.add_header('User-Agent', USER_AGENT)        
    
        dialog = xbmcgui.DialogProgress()
        dialog.create('Loading Video', 'Playing from direct link')

        with urllib.request.urlopen(req) as response:
            dialog.close()
        xbmc.Player().play(path, listitem)               
                                                                                                                                                          
    def _create_submenu_films(self, urlparam):
        Texture13DB.clean_database()    
        category = urlparam.split("=")[1]      
        self._create_films_list(category)

    def _create_films_list(self, category):
        items = []
        for title, poster, href in Films().films_page_list(category):
            player_link = Config.RTD_URL + href

            url = sys.argv[0] + "?" + urllib.parse.urlencode({'film': title})
            item = xbmcgui.ListItem(title)
            item.setArt({'icon': poster, 'poster': poster, 'banner': poster, 'fanart': ''})
            item.setProperty('path', player_link)
            xbmcplugin.addDirectoryItem(self._plugin_id, url, item, len(items))
                                    
        xbmcplugin.endOfDirectory(self._plugin_id, cacheToDisc=True)

    def _play_film(self, urlparam):
        "Play the stream corresponding to title."
        film = urlparam.split("=")[1]
        film = unquote(film) 

        player_link = xbmc.getInfoLabel('ListItem.Property(path)') 
        scraper = Scraper2()
        film_page = scraper.get_film_page_in_a_string(player_link)

        films2 = Films2()
        mp4_url = films2.mp4_url_link(film_page)
        
        path = mp4_url[0]
        listitem = xbmcgui.ListItem(path=path)
        listitem.setProperty('IsPlayable', 'true')
        
        req = urllib.request.Request(path)
        req.add_header('User-Agent', USER_AGENT)

        dialog = xbmcgui.DialogProgress()
        dialog.create('Loading Video', 'Playing from direct link')

        with urllib.request.urlopen(req) as response:
            dialog.close()        
        xbmc.Player().play(response.url)                                                                                                                                        
        
    def connect_series_db(self):
        """Connect to series database and create one if it does not exist."""
        db_exists = os.path.exists(db_series)
        db_con = sqlite3.connect(db_series)
        c = db_con.cursor()
        if not db_exists:
            c.execute("""CREATE TABLE series (
                            serie TEXT PRIMARY KEY,
                            poster TEXT,
                            series_page TEXT
                         );""")
            db_con.commit()
        return db_con               

    def connect_episodes_db(self):
        """Connect to episodes database and create one if it does not exist."""
        db_con = sqlite3.connect(db_episodes)
        c = db_con.cursor()
        try:
            c.execute("SELECT * FROM episodes;")
        except sqlite3.OperationalError:    
            c.execute("""CREATE TABLE IF NOT EXISTS rtd_episodes(
                            series text,
                            episode text PRIMARY KEY,
                            poster text,
                            episode_player text)""")                                                             
            db_con.commit()
        return db_con
               
    def _create_submenu_series(self, urlparam):
        Texture13DB.clean_database()
        category = urlparam.split("=")[1]        
        with self.connect_series_db() as db_con:
            c = db_con.cursor()        
            self._create_series_list(category, c, db_con)            

    def _create_series_list(self, category, c, db_con):
        items = []
        with self.connect_series_db() as db_con:
            c = db_con.cursor() 
            for poster, href, serie in Series().series_page_main(category):
                series_page = Config.RTD_URL + href
                        
                c.execute("INSERT OR REPLACE INTO series (serie, poster, series_page) VALUES (?, ?, ?)", (serie, poster, series_page))
                xbmc.log("Data inserted into series table: Serie={}, Poster={}, Series Page={}".format(serie, poster, series_page))
            
                db_con.commit()
                                    
                url = sys.argv[0] + "?" + urllib.parse.urlencode({'serie': serie})
                item = xbmcgui.ListItem(serie)
                item.setArt({'icon': poster, 'poster': poster, 'banner': poster, 'fanart': ''})         
                xbmcplugin.addDirectoryItem(self._plugin_id, url, item, True, len(items))
                
            xbmcplugin.endOfDirectory(self._plugin_id, cacheToDisc=True)
                                                                     
    def _create_submenu_episodes(self, urlparam):       
        """Call series page corresponding to serie."""
        
        serie = urlparam.split("=")[1]
        serie = unquote(serie)
        
        with self.connect_series_db() as db_con:
            c = db_con.cursor()                       
            query = "SELECT series_page FROM series WHERE serie = ?"
            c.execute(query, (serie,))
            result = c.fetchone()           
        
            if result is not None and len(result) > 0:                
                series_page = result[0]
                
                scraper = Scraper_Episodes()
                episodes_page = scraper.get_episodes_page_in_a_string(series_page) 
        
                episode = Episodes()
                eps_list = episode.episodes_list(episodes_page)
                                    
                with self.connect_episodes_db() as db_con:
                    c = db_con.cursor()
                    c.execute("BEGIN TRANSACTION")
                    
                    items = []
                    for item in eps_list:
                        href = item[0]
                        episode_player = Config.RTD_URL + href
                        poster = item[1]
            
                        episode = os.path.basename(episode_player[:-1])
                        episode = episode.replace('-', ' ').capitalize()
                           
                        if 'series' in episode_player:
                            series = episode_player.split('/')[4].replace('-', ' ').title()
                            
                            c.execute("SELECT EXISTS(SELECT 1 FROM rtd_episodes WHERE episode=?)", (episode,))
                                                
                            exists = c.fetchone()[0]
                            if exists:
                                c.execute("UPDATE rtd_episodes SET series=?, poster=?, episode_player=? WHERE episode=?", (series, poster, episode_player, episode))
                            else:
                                c.execute("INSERT INTO rtd_episodes VALUES (?, ?, ?, ?)", (series, episode, poster, episode_player))

                            db_con.commit()
                    
                            url = sys.argv[0] + "?" + urllib.parse.urlencode({'episode': episode})
                            item = xbmcgui.ListItem(episode)
                            item.setArt({'icon': poster, 'poster': poster, 'banner': poster, 'fanart': ''})
                            items.append((url, item, True))
                            xbmc.log("Added item to list")

                    xbmcplugin.addDirectoryItems(self._plugin_id, items, len(items))
                    xbmc.log("Added film directory items")
                    xbmcplugin.endOfDirectory(self._plugin_id, cacheToDisc=True)
                    xbmc.log("Ended film directory listing")            

    def _play_episode(self, urlparam):
        "Play the stream corresponding to episode."
        episode = urlparam.split("=")[1]
        episode = unquote(episode) 

        with self.connect_episodes_db() as db_con:
            c = db_con.cursor()
            query = "SELECT episode_player FROM rtd_episodes WHERE episode = ?"

            c.execute(query, (episode,))
            result = c.fetchone()

            if result is not None and len(result) > 0:      
                episode_player = result[0]
                             
                scraper = Series_MP4()
                episode_page = scraper.get_episode_player_page_in_a_string(episode_player)            
                
                episodes2 = Episodes2()
                mp4_url = episodes2.mp4_url_link(episode_page)                                              
    
                path = mp4_url[0]
                listitem = xbmcgui.ListItem(path=path)
                listitem.setProperty('IsPlayable', 'true')
    
                req = urllib.request.Request(path)
                req.add_header('User-Agent', USER_AGENT)
                
                dialog = xbmcgui.DialogProgress()
                dialog.create('Loading Video', 'Playing from direct link')
                    
                with urllib.request.urlopen(req) as response:
                    dialog.close()
                xbmc.Player().play(response.url)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
        
    def connect_shows_db(self):
        """Connect to shows database and create one if it does not exist."""
        db_exists = os.path.exists(db_shows)
        db_con = sqlite3.connect(db_shows)
        c = db_con.cursor()
        if not db_exists:
            c.execute("""CREATE TABLE shows (
                            show TEXT PRIMARY KEY,
                            poster TEXT,
                            shows_page TEXT
                         );""")
            db_con.commit()
        return db_con              

    def connect_chapters_db(self):
        """Connect to chapters database and create one if it does not exist."""
        db_con = sqlite3.connect(db_chapters)
        c = db_con.cursor()
        try:
            c.execute("SELECT * FROM chapters;")
        except sqlite3.OperationalError:   
            c.execute("""CREATE TABLE IF NOT EXISTS rtd_chapters(
                            shows text,
                            chapter text PRIMARY KEY,
                            poster text,
                            chapter_player text)""")                                                             
            db_con.commit()
        return db_con
                 
    def _create_submenu_shows(self, urlparam):
        Texture13DB.clean_database()
        category = urlparam.split("=")[1]
        
        with self.connect_shows_db() as db_con:
            c = db_con.cursor()        
            self._create_shows_list(category, c, db_con)            

    def _create_shows_list(self, category, c, db_con):
        items = []
        for poster, href, show in Shows().shows_page_main(category):
            shows_page = Config.RTD_URL + href                        
            c.execute("INSERT OR REPLACE INTO shows (show, poster, shows_page) VALUES (?, ?, ?)", (show, poster, shows_page))            
            db_con.commit()
                                    
            url = sys.argv[0] + "?" + urllib.parse.urlencode({'show': show})
            item = xbmcgui.ListItem(show)
            item.setArt({'icon': poster, 'poster': poster, 'banner': poster, 'fanart': ''})
            items.append((url, item, True))           
           
        xbmcplugin.addDirectoryItems(self._plugin_id, items)
        xbmcplugin.endOfDirectory(self._plugin_id, cacheToDisc=True)
                                  

    def _create_submenu_chapters(self, urlparam):       
        """Call shows page corresponding to show."""
        
        show = urlparam.split("=")[1]
        show = unquote(show)
        
        with self.connect_shows_db() as db_con:
            c = db_con.cursor()                       
            query = "SELECT shows_page FROM shows WHERE show = ?"
            c.execute(query, (show,))
            result = c.fetchone()            
        
            if result is not None and len(result) > 0:
                shows_page = result[0]
                   
                scraper = Scraper_Chapters()
                chapters_page = scraper.get_chapters_page_in_a_string(shows_page)
           
                chapter = Chapters()
                eps_list = chapter.chapters_list(chapters_page)                                      

                with self.connect_chapters_db() as db_con:
                    c = db_con.cursor()
                    c.execute("BEGIN TRANSACTION")
                    
                    items = []
                    for item in eps_list:
                        href = item[0]
                        chapter_player = Config.RTD_URL + href
                        poster = item[1]
            
                        chapter = os.path.basename(chapter_player[:-1])
                        chapter = chapter.replace('-', ' ').capitalize()
                           
                        if 'shows' in chapter_player:
                            shows = chapter_player.split('/')[4].replace('-', ' ').title()

                            c.execute("SELECT EXISTS(SELECT 1 FROM rtd_chapters WHERE chapter=?)", (chapter,))
                                                 
                            exists = c.fetchone()[0]
                            if exists:
                                c.execute("UPDATE rtd_chapters SET shows=?, poster=?, chapter_player=? WHERE chapter=?", (shows, poster, chapter_player, chapter))
                            else:
                                c.execute("INSERT INTO rtd_chapters VALUES (?, ?, ?, ?)", (shows, chapter, poster, chapter_player))
    
                            db_con.commit()
                    
                            url = sys.argv[0] + "?" + urllib.parse.urlencode({'chapter': chapter})
                            item = xbmcgui.ListItem(chapter)
                            item.setArt({'icon': poster, 'poster': poster, 'banner': poster, 'fanart': ''})
                            items.append((url, item, True))
                               
                    xbmcplugin.addDirectoryItems(self._plugin_id, items)
                    xbmcplugin.endOfDirectory(self._plugin_id, cacheToDisc=True)
                

    def _play_chapter(self, urlparam):
        "Play the stream corresponding to chapter."
        chapter = urlparam.split("=")[1]
        chapter = unquote(chapter) 

        with self.connect_chapters_db() as db_con:
            c = db_con.cursor()

            query = "SELECT chapter_player FROM rtd_chapters WHERE chapter = ?"

            c.execute(query, (chapter,))
            result = c.fetchone()

            if result is not None and len(result) > 0:      
                chapter_player = result[0]
                             
                scraper = Shows_MP4()
                chapter_page = scraper.get_chapter_player_page_in_a_string(chapter_player)            
                
                chapters2 = Chapters2()
                mp4_url = chapters2.mp4_url_link(chapter_page)                                              
    
                path = mp4_url[0]
                listitem = xbmcgui.ListItem(path=path)
                listitem.setProperty('IsPlayable', 'true')
    
                req = urllib.request.Request(path)
                req.add_header('User-Agent', USER_AGENT)
                
                dialog = xbmcgui.DialogProgress()
                dialog.create('Loading Video', 'Playing from direct link')
    
                with urllib.request.urlopen(req) as response:
                    dialog.close()
                xbmc.Player().play(response.url)  
        
    def connect_more_db(self):
        """Connect to more database and create one if it does not exist."""
        db_exists = os.path.exists(db_more)
        db_con = sqlite3.connect(db_more)
        c = db_con.cursor()
        if not db_exists:
            c.execute("""CREATE TABLE more (
                            more TEXT PRIMARY KEY,
                            poster TEXT,
                            more_page TEXT
                         );""")
            db_con.commit()
        return db_con

    def connect_events_db(self):
        """Connect to events database and create one if it does not exist."""
        db_con = sqlite3.connect(db_events)
        c = db_con.cursor()
        try:
            c.execute("SELECT * FROM events;")
        except sqlite3.OperationalError:    
            c.execute("""CREATE TABLE IF NOT EXISTS rt_events(
                            more text,
                            event text PRIMARY KEY,
                            poster text,
                            event_player text)""")                                                              
            db_con.commit()
        return db_con
                
    def _create_submenu_more(self, urlparam):
        Texture13DB.clean_database()
        category = urlparam.split("=")[1]
        
        with self.connect_more_db() as db_con:
            c = db_con.cursor()        
            self._create_more_list(category, c, db_con)            

    def _create_more_list(self, category, c, db_con):
        items = []
        
        for poster, more, href in More().more_page_main(category):
            more_page = Config.RT_URL + href                        
            c.execute("INSERT OR REPLACE INTO more (more, poster, more_page) VALUES (?, ?, ?)", (more, poster, more_page))
            
            db_con.commit()
                                    
            url = sys.argv[0] + "?" + urllib.parse.urlencode({'more': more})
            item = xbmcgui.ListItem(more)
            item.setArt({'icon': poster, 'poster': poster, 'banner': poster, 'fanart': ''})
            items.append((url, item, True))           
           
        xbmcplugin.addDirectoryItems(self._plugin_id, items)
        xbmcplugin.endOfDirectory(self._plugin_id, cacheToDisc=True)                                     

    def _create_submenu_events(self, urlparam):       
        """Call more page corresponding to more."""
        
        more = urlparam.split("=")[1]
        more = unquote(more)
        xbmc.log(f"more value is: {more}")
        
        with self.connect_more_db() as db_con:
            c = db_con.cursor()                       
            query = "SELECT more_page FROM more WHERE more = ?"
            c.execute(query, (more,))
            result = c.fetchone()            
        
            if result is not None and len(result) > 0:
                more_page = result[0]
                   
                scraper = Scraper_Events()
                events_page = scraper.get_events_page_in_a_string(more_page)
           
                event = Events()
                evts_list = event.events_list(events_page)

                with self.connect_events_db() as db_con:
                    c = db_con.cursor()
                    c.execute("BEGIN TRANSACTION")
                    
                    items = []
                    for item in evts_list:
                        poster = item[0]
                        event = item[1]
                        href = item[2]
                        xbmc.log(f"Processing item: {poster}, {event}, {href}") 
                        xbmc.log(f"Processing event: {event}") 
                        event_player = Config.RT_URL + href                                              
                                
                        if 'shows' in event_player:
                            more = event_player.split('/')[4].replace('-', ' ').title()                       
                            
                            c.execute("SELECT EXISTS(SELECT 1 FROM rt_events WHERE event=?)", (event,))
                                                
                            exists = c.fetchone()[0]
                            if exists:
                                c.execute("UPDATE rt_events SET more=?, poster=?, event_player=? WHERE event=?", (more, poster, event_player, event))

                            else:
                                c.execute("INSERT INTO rt_events VALUES (?, ?, ?, ?)", (more, event, poster, event_player))
    
                            db_con.commit()
                    
                            url = sys.argv[0] + "?" + urllib.parse.urlencode({'event': event})
                            item = xbmcgui.ListItem(event)
                            item.setArt({'icon': poster, 'poster': poster, 'banner': poster, 'fanart': ''})
                            items.append((url, item, True))
                               
                    xbmcplugin.addDirectoryItems(self._plugin_id, items)
                    xbmcplugin.endOfDirectory(self._plugin_id, cacheToDisc=True)               


    def _play_event(self, urlparam):
        "Play the stream corresponding to event."
        event = urlparam.split("=")[1]
        event = unquote(event) 
    
        with self.connect_events_db() as db_con:
            c = db_con.cursor()

            query = "SELECT event_player FROM rt_events WHERE event = ?"

            c.execute(query, (event,))
            result = c.fetchone()
            
            if result is not None and len(result) > 0:      
                event_player = result[0]
                             
                scraper = More_MP4()
                event_page = scraper.get_event_player_page_in_a_string(event_player)            
                
                events2 = Events2()
                mp4_url = events2.mp4_url_link(event_page)                                              
    
                path = mp4_url[0]
                listitem = xbmcgui.ListItem(path=path)
                listitem.setProperty('IsPlayable', 'true')
    
                req = urllib.request.Request(path)
                req.add_header('User-Agent', USER_AGENT)
                
                dialog = xbmcgui.DialogProgress()
                dialog.create('Loading Video', 'Playing from direct link')
    
                with urllib.request.urlopen(req) as response:
                    dialog.close()
                xbmc.Player().play(response.url)
       
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
