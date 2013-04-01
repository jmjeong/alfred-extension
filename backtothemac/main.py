# -*- coding: utf-8 -*-
#
# Jaemok Jeong, 2013

import feedparser
import itertools
import re
import urllib
import alfred
import os
import uuid

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

imageregex = re.compile(r"img.*src=\"(.*?)\"")
MAX_RESULTS = 18

results = []

d = feedparser.parse('http://macnews.tistory.com/rss')
for (idx,e) in enumerate(itertools.islice(d.entries,MAX_RESULTS)):
    imageurl = imageregex.search(e.description)
    if imageurl:
        url = imageurl.group(1)
        filepath = os.path.join(alfred.work(True), os.path.split(url)[1])
        if not os.path.exists(filepath):
            urllib.urlretrieve(url, filepath)
        imageurl = filepath
    else:
        imageurl = u"icon.png"
        
    results.append(alfred.Item(title=e.title,subtitle=e.published,attributes={'uid':uuid.uuid4(), 'arg':e.link},icon=imageurl))
    
alfred.write(alfred.xml(results, maxresults=MAX_RESULTS))
