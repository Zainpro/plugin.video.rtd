# -*- coding=utf8 -*-
#******************************************************************************
# Config.py
#------------------------------------------------------------------------------
# RTD
# Copyright (c) 
#******************************************************************************
import xbmc,xbmcvfs

class Config(object):
    "The most important configuration parameters summarized."

    PLUGIN_NAME    = "plugin.video.rtd"
    RTD_URL = "https://rtd.rt.com"

    RTD_URL_ON_AIR          = RTD_URL + "/on-air/"
    RTD_URL_FILMS           = RTD_URL + "/films/"
    RTD_URL_SERIES          = RTD_URL + "/series/"
    RTD_URL_SHOWS           = RTD_URL + "/shows/"

    SCRIPT_SETTINGS = "settings.py"
    M3U8_PATTERN = "(https:[^>\s]+?.m3u8)"
    
    