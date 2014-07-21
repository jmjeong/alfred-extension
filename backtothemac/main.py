# -*- coding: utf-8 -*-
#
# Jaemok Jeong, 2013

import feedparser
import itertools
import re
import urllib
import alfred
import os
import subprocess
import json
import util
import time

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

RELOAD_ASK_THRESHOLD = 60*60*1          # 1 hour

def config_data():
    try:
        config = json.loads(open(os.path.join(alfred.work(False), 'config.json')).read())
    except:
        config = {}
    return config

def rss_data():
    try:
        return json.loads(open(os.path.join(alfred.work(True), 'rss-cache.json')).read())
    except:
        return []

def main():
    rss = rss_data()
    config = config_data()
    try:
        max_results = config['max_results']
    except:
        max_results = None

    results = []
    for e in itertools.islice(rss,max_results):
        results.append(alfred.Item(title=e['title'],subtitle=e['published'],attributes={'arg':e['link']},icon=e['image']))

    try:
        last_updated = config['last_updated']
    except:
        last_updated = 0
    subtitle = "Last updated: "+(last_updated and util.pretty_date(config['last_updated']) or "no info")
    
    diff = int(time.time())-last_updated
    if diff > RELOAD_ASK_THRESHOLD or len(rss) == 0:
        results.insert(0,alfred.Item(title="BackToTheMac - Reload Data?", subtitle=subtitle,
                                     attributes={'arg':'reload','uid':alfred.uid('t')}, icon="icon.png"))
    else:
        results.insert(0,alfred.Item(title="BackToTheMac", subtitle=subtitle,
                                     attributes={'arg':'http://macnews.tistory.com','uid':alfred.uid('t')}, icon="icon.png"))
    
    alfred.write(alfred.xml(results, maxresults=None))

if __name__ == '__main__':
    main()
