# -*- coding=utf8 -*-
#******************************************************************************
# Onair.py
#------------------------------------------------------------------------------
# RTD
#******************************************************************************  
                    
class Onair:
    def __init__(self):
        super(Onair, self).__init__()

    def media_list(self):
        MEDIA = [
            {
                'name': 'RT Documentary',
                'thumb': 'http://www.glaz.tv/images/logos/tv/big/russia-today-documentary.jpg',
                'video': 'https://rt-rtd.rttv.com/live/rtdoc/playlist.m3u8'
            },
            {
                'name': 'RT News 1',
                'thumb': 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/Russia-today-logo.svg/512px-Russia-today-logo.svg.png',
                'video': 'https://rumble.com/live-hls-dvr/2td0fs/playlist.m3u8'
            },
            {
                'name': 'RT News 2',
                'thumb': 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/Russia-today-logo.svg/512px-Russia-today-logo.svg.png',
                'video': 'https://cdn.odysee.live/content/fdd11cb3ab75f95efb7b3bc2d726aa13ac915b66/master.m3u8'
            },
            {
                'name': 'RT News Global',
                'thumb': 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/Russia-today-logo.svg/512px-Russia-today-logo.svg.png',
                'video': 'https://rt-glb.rttv.com/live/rtnews/playlist.m3u8'
            },
            {
                'name': 'RT News Actualidad',
                'thumb': 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/Russia-today-logo.svg/512px-Russia-today-logo.svg.png',
                'video': 'https://rt-esp.rttv.com/live/rtesp/playlist.m3u8'
            },
            {
                'name': 'RT en Español',
                'thumb': 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/Russia-today-logo.svg/512px-Russia-today-logo.svg.png',
                'video': 'https://cdn.odysee.live/content/9f638b94d11d879726ae55dd5a0923621b96a45b/master.m3u8'
            },
            {
                'name': 'RT News France',
                'thumb': 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b8/RT-France-logo.svg/512px-RT-France-logo.svg.png',
                'video': 'https://rt-fra.rttv.com/live/rtfrance/playlist.m3u8'
            }
        ]
        return MEDIA
        