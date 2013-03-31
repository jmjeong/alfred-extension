#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# jmjeong, 2013/3/25

import alfred
import subprocess
import re
import os
import plistlib
from uuid import uuid4

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

dirname = os.path.dirname(os.path.abspath('.'))

try:
    query = "".join(sys.argv[1:])
except:
    query = u""
    
dirs = [f for f in os.listdir(dirname) if os.path.isdir(os.path.join(dirname, f))]

results = []

for (idx,d) in enumerate(dirs):
    try:
        plist = plistlib.readPlist(os.path.join(dirname, d, 'info.plist'))
    except:
        continue
    
    title = plist['name']
    createdby = plist['createdby']
    disabled = plist.get('disabled', None)
    try:
        keyword = ",".join([o['config']['keyword'] for o in plist['objects'] if 'alfred.workflow.input' in o['type'] ])
    except KeyError:
        keyword = ""
        
    if keyword:
        keyword = " (" + keyword + ")"
        
    if not query in title.lower() + createdby.lower() + keyword.lower():
        continue

    displayTitle = title + (' - disabled' if disabled else '')

    results.append({'title': displayTitle, 'createdby' : createdby, 'disabled' : disabled,
                    'keyword': keyword, 'directory' : d})

results = sorted(results, key=lambda a: a['title'].lower())

resultsData = [alfred.Item(title=f['title'], subtitle=' by ' + f['createdby'] + f['keyword'],
                       attributes = {'uid':uuid4(), 'arg':os.path.join(dirname,f['directory'])},
                       icon=os.path.join(dirname, f['directory'], u"icon.png")) for f in results]    
    
alfred.write(alfred.xml(resultsData,maxresults=None))
