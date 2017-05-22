#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# main.py, v1.0
#
# Jaemok Jeong, 2016/11/15


import re
import sys
import unicodedata
import json
from datetime import date, timedelta

import util

reload(sys)
sys.setdefaultencoding('utf-8')

def main():
    try: q = unicodedata.normalize('NFC',  unicode(sys.argv[1].strip()))
    except: q = ""

    (title, area, tag, day, note) = util.parse(q[1:])

    display = title.strip()+' '
    if area != 'Inbox':
        display += '@'+area+' '

    if day:
        display += '> ' + day.strftime('%m/%d %a')

    subtitle = "title #tag @t|a|s ::note >duedate (ex. fri, 3d, 2w, 12/31)"
    help = {"valid": False, "subtitle": subtitle}
    
    output = []
    output.append({"title": display, "subtitle": subtitle, "arg":q, "valid": True,
                  "mods": { "alt": help, "ctrl":help, "cmd":help, "shift":help}})
    print json.dumps({"items": output})

if __name__ == '__main__':
    main()
