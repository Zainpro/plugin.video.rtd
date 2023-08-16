# -*- coding=utf8 -*-
#******************************************************************************
# Config.py
#------------------------------------------------------------------------------
# RTD
# Copyright (c) Zain, El Zipa
#******************************************************************************
import xbmc,xbmcvfs

class Config(object):
    "The most important configuration parameters summarized."

    PLUGIN_NAME = "plugin.video.rtd"
    RTD_URL = "https://rtd.rt.com"
    RT_URL = "https://www.rt.com"

    RTD_URL_ON_AIR          = RTD_URL + "/on-air/"
    RTD_URL_FILMS           = RTD_URL + "/films/"
    RTD_URL_SERIES          = RTD_URL + "/series/"
    RTD_URL_SHOWS           = RTD_URL + "/shows/"
    RT_URL_MORE             = RT_URL + "/shows/"

    SCRIPT_SETTINGS = "settings.py"

    
   