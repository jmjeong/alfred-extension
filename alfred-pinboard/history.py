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
import util

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# DELIMETER = "'"

def compare_key(x,y):
    if x[4] and not y[4]:
        return -1
    elif not x[4] and y[4]:
        return 1
    elif x[3] < y[3]:
        return 1
    else:
        return -1
    
if __name__ == '__main__':
    try:
        q = unicode(sys.argv[2].strip())
        q = unicodedata.normalize('NFC', q)
    except:
        q = ""
    
    history = main.history_data()

    if sys.argv[1] == "search":
        results = []
        history.sort(cmp=compare_key,reverse=False)
        for h in history:
            if q=="" or q in h[1]:
                results.append(alfred.Item(title=(h[4] and main.STAR or "")+h[1]+" (%d)"%h[2],
                                           # // subtitle=time.strftime('%Y.%m.%d %H:%M:%S', time.localtime(h[3])),
                                           subtitle = util.pretty_date(h[3]),
                                           attributes={'arg':h[1]}, icon="icon.png"))
        alfred.write(alfred.xml(results,maxresults=20))
    elif sys.argv[1] == "delete":
        for h in history:
            if q == h[1]:
                history.remove(h)
                break
        with open(os.path.join(alfred.work(False), 'search-history.json'), 'w+') as myFile:
            myFile.write(json.dumps(history))
    elif sys.argv[1] == "star":
        for h in history:
            if q == h[1]:
                h[4] = not h[4]
                break
        with open(os.path.join(alfred.work(False), 'search-history.json'), 'w+') as myFile:
            myFile.write(json.dumps(history))
