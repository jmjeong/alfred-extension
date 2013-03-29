#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# jmjeong, 2013/3/25

import alfred
import subprocess
import re
import os
import plistlib
import sqlite3
from uuid import uuid4

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

if len(sys.argv) == 2:
    query = sys.argv[1].lower().strip()
else:
    query = ""

dockpath = os.path.expanduser("~/Library/Application Support/Dock/")
dbnames = [os.path.join(dockpath,f) for f in os.listdir(dockpath) if os.path.isfile(os.path.join(dockpath,f))]

appnames = []

for db in dbnames:
    conn = sqlite3.connect(db)
    c = conn.cursor()
    try:
        c.execute("select title from apps")
    except sqlite3.OperationalError:
        conn.close()
        continue

    appnames.extend(c.fetchall())
    conn.close()

appnames = list(set(appnames))

results = [alfred.Item(title=f[0],
                       subtitle="",
                       attributes = {'uid':uuid4(),
                                     'arg':f[0],
                                     'autocomplete':f[0]},
                    
                       ) for f in appnames if query in f[0].lower()]
alfred.write(alfred.xml(results,maxresults=None))
