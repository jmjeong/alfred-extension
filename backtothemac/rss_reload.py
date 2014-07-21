# -*- coding: utf-8 -*-
#
# Jaemok Jeong, 2013

import feedparser
import re
import urllib
import alfred
import os
import subprocess
import json
import time
import main

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def reload():
    imageregex = re.compile(r"img.*src=\"(.*?)\"")
    config = main.config_data()

    d = feedparser.parse('http://macnews.tistory.com/rss')
    items = []
    for e in d.entries:
        try:
            imageurl = imageregex.search(e.description)
            if imageurl:
                url = imageurl.group(1)
                filepath = os.path.join(alfred.work(True), os.path.split(url)[1])
                if not os.path.exists(filepath):
                    urllib.urlretrieve(url, filepath)
                    cmd = "sips -z 72 72 '%s'" % filepath
                    subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
                imageurl = filepath
            else:
                imageurl = u"icon.png"
        except:
            imageurl = u"icon.png"
        items.append({'title':e.title,'published':e.published,'link':e.link,'image':imageurl})

    with open(os.path.join(alfred.work(True), 'rss-cache.json'), 'w+') as myFile:
        myFile.write(json.dumps(items))

    config['last_updated'] = int(time.time())
    with open(os.path.join(alfred.work(False), 'config.json'), 'w+') as myFile:
        myFile.write(json.dumps(config))

    print "Reloading BackToTheMac completed..."
    # alfred.write(alfred.xml([alfred.Item(title="Reloading Finished", subtitle="Move to http://macnews.tistory.com",
    #                                 attributes={'arg':'http://macnews.tistory.com','uid':alfred.uid('t')}, icon="icon.png")], maxresults=None))
if __name__ == '__main__':
    reload()
