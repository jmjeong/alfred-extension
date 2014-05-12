#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# history, v1.0
#
# Jaemok Jeong, 2014/05/12

import os
import json
import main
import alfred
import time
import unicodedata

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

DELIMETER = u"\u007C"

def pretty_date(time=False):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    """
    from datetime import datetime
    now = datetime.now()
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time,datetime):
        diff = now - time 
    elif not time:
        diff = now - now
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(second_diff) + " seconds ago"
        if second_diff < 120:
            return  "a minute ago"
        if second_diff < 3600:
            return str( second_diff / 60 ) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str( second_diff / 3600 ) + " hours ago"
    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        return str(day_diff) + " days ago"
    if day_diff < 31:
        return str(day_diff/7) + " weeks ago"
    if day_diff < 365:
        return str(day_diff/30) + " months ago"
    return str(day_diff/365) + " years ago"

if __name__ == '__main__':
    try:
        q = unicode(sys.argv[2].strip())
        q = unicodedata.normalize('NFC', q)
    except:
        q = ""
    
    history = main.history_data()
    history = sorted(history,key=lambda s:s[3],reverse=True)

    if sys.argv[1] == "search":
        results = []
        for h in history:
            if q=="" or q in h[0]:
                results.append(alfred.Item(title=(h[4] and main.STAR+" " or "")+h[0]+" "+DELIMETER+" "+h[1]+" (%d)"%h[2],
                                           # // subtitle=time.strftime('%Y.%m.%d %H:%M:%S', time.localtime(h[3])),
                                           subtitle = pretty_date(h[3]),
                                           attributes={'arg':h[0]+":"+h[1]}, icon="icon.png"))
        alfred.write(alfred.xml(results,maxresults=20))
    elif sys.argv[1] == "delete":
        for h in history:
            if q == h[0]+":"+h[1]:
                history.remove(h)
                break
        with open(os.path.join(alfred.work(False), 'search-history.json'), 'w+') as myFile:
            myFile.write(json.dumps(history))
    elif sys.argv[1] == "star":
        for h in history:
            if q == h[0]+":"+h[1]:
                h[4] = not h[4]
                break
        with open(os.path.join(alfred.work(False), 'search-history.json'), 'w+') as myFile:
            myFile.write(json.dumps(history))
            
