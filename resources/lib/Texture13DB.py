# -*- coding=utf8 -*-
#******************************************************************************
# Texture13DB.py
#------------------------------------------------------------------------------
# RTD
#******************************************************************************
import xbmc,xbmcvfs
import sqlite3

from resources.lib.Config import Config


class Texture13DB(object):
    "Provides up-to-date thumbnails in the display."
    
    @classmethod
    def clean_database(cls):
        "Clears the Texture13.db and local cache."
        conn = sqlite3.connect(xbmcvfs.translatePath("special://database/Textures13.db"))
        try:
            with conn:
                conn.execute("DELETE FROM texture WHERE url LIKE '%roomimg%';")
        except:
            pass
