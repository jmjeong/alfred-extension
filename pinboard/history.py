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

if __name__ == '__main__':
    try:
        q = unicode(sys.argv[1].strip())
        q = unicodedata.normalize('NFC', q)
    except:
        q = ""
    
    history = main.history_data()
    history = sorted(history,key=lambda s:s[2],reverse=True)

    results = []
    for h in history:
        if q=="" or q in h[0]:
            results.append(alfred.Item(title=h[0]+" (%d)"%h[1], subtitle=time.strftime('%Y.%m.%d %H:%M:%S', time.localtime(h[2])),
                                   attributes={'arg':h[0]}, icon="icon.png"))

    alfred.write(alfred.xml(results,maxresults=20))
