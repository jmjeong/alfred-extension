#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# jmjeong, 2013/3/25

import alfred
import os
import sqlite3
import subprocess
from uuid import uuid4

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

query = sys.argv[1]

dockpath = os.path.expanduser("~/Library/Application Support/Dock/")

dbnames = [os.path.join(dockpath,f) for f in os.listdir(dockpath)
           if os.path.isfile(os.path.join(dockpath,f)) and f.endswith(".db")]

for db in dbnames:
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("delete from apps where title=\"%s\"" % query)
    conn.commit()
    conn.close()

launchArgs = "tell application \"Dock\" to quit"
subprocess.check_call(["osascript", "-e", launchArgs])

alfred.write(query)
