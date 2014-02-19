#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# jmjeong, 2014/02/19

import alfred
import os
import json
import unicodedata

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def intro():
    result = [alfred.Item(title='Lookup Documentation', subtitle='setup incomplete.', attributes={'arg':'http://jmjeong.com'}, icon="icon.png")]
    alfred.write(alfred.xml(result))

def tags(pins,query):
    if not "→" in query:                      # tag search
        query = query.lower()
        tag_list = {}
        for p in pins:
            tags = p['tags'].encode('utf-8').split(' ')
            for t in tags:
                if not t: continue
                if t in tag_list:
                    tag_list[t] += 1
                else:
                    tag_list[t] = 1
        resultData = []
        tag_list_key = sorted(tag_list.keys(),key=str.lower)
        for i in tag_list_key:
            if not query or query in i.lower():
                resultData.append(alfred.Item(title="tag:"+i+"("+str(tag_list[i])+")→", subtitle='', attributes={'arg':i, 'autocomplete':i+"→"}, icon='icon.png'))
        alfred.write(alfred.xml(resultData,maxresults=None))
    else:
        (query_tag, query_title)=query.split("→") 
        results=[]
        for p in pins:
            title = p['description'].replace(' ', '')
            tags = p['tags'].split(' ')
            url = p['href']
            for t in tags:
                if (query_tag in t) and ((not query_title) or (query_title.lower() in title.lower())):
                    results.append({'title':p['description'],'url':url})
                    break
        resultData = [alfred.Item(title=f['title'].encode('utf-8'), subtitle=f['url'].encode('utf-8'), attributes = {'arg':f['url']}, icon="item.png") for f in results]
        alfred.write(alfred.xml(resultData,maxresults=None))
    sys.exit(0)

try:
    file = os.environ['HOME']+'/.bookmarks.json'
    pins = json.loads(open(file, 'r').read())
except:
    intro()
    sys.exit(0)

# arg parsing
category = sys.argv[1]
try:
    q = unicode(sys.argv[2].strip())
    q = unicodedata.normalize('NFC', q)
except:
    q = ""

# tag processing
if category=='tags':
    tags(pins,q)
    sys.exit(0)
    
results = []
q = q.lower()

for p in pins:
    title = p['description'].replace(' ', '')
    url = p['href']
    extended = p['extended'].replace(' ', '')
    tags = p['tags'].split(' ')
    toread = p['toread']

    if q=="":
        if category=='toread':
            if toread=='yes':            
                results.append({'title':p['description'],'url':url})
        else: 
            results.append({'title':p['description'],'url':url})
    else:
        if category=='title' and q in title.lower():
            results.append({'title':p['description'],'url':url})
        elif category=='link' and q in url.lower():
            results.append({'title':p['description'],'url':url})
        elif category=='description' and q in extended.lower():
            results.append({'title':p['description'],'url':url})
        elif category=='toread' and q in title.lower() and toread=='yes':
            results.append({'title':p['description'],'url':url})
        elif category=='all' and (q in title.lower() or q in url.lower() or q in extended.lower()):
            results.append({'title':p['description'],'url':url})

resultData = [alfred.Item(title=f['title'].encode('utf-8'), subtitle=f['url'].encode('utf-8'), attributes = {'arg':f['url']}, icon="item.png") for f in results]
alfred.write(alfred.xml(resultData,maxresults=None))
