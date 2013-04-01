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
# import subprocess

import sys
reload(sys)

# imageregex = re.compile(r"img.*src=\"(.*?)\"")
MAX_RESULTS = 18

results = []

d = feedparser.parse('http://macnews.tistory.com/rss')
for (idx,e) in enumerate(itertools.islice(d.entries,MAX_RESULTS)):
    # try:
    #     imageurl = imageregex.search(e.description)
    #     if imageurl:
    #         url = imageurl.group(1)
    #         filepath = os.path.join(alfred.work(True), os.path.split(url)[1])
    #         if not os.path.exists(filepath):
    #             urllib.urlretrieve(url, filepath)
    #             cmd = "sips -z 72 72 '%s'" % filepath
    #             subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
    #         imageurl = filepath
    #     else:
    #         imageurl = u"icon.png"
    # except:
    #     imageurl = u"icon.png"
    imageurl = u"icon.png"
        
    results.append(alfred.Item(title=e.title,subtitle=e.published,attributes={'uid':uuid.uuid4(), 'arg':e.link},icon=imageurl))

alfred.write(alfred.xml(results, maxresults=MAX_RESULTS))
