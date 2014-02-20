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
        pinboard_url = 'https://pinboard.in/search/?query=%s&mine=Search+Mine'%query_title
        resultData.append(alfred.Item(title='Search "%s" in pinboard.in'%query_title, subtitle=pinboard_url, attributes={'arg':pinboard_url}, icon="icon.png"))
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
q = q.lower().replace(' ', '')

for p in pins:
    title = p['description'].replace(' ', '').lower()
    url = p['href'].lower()
    extended = p['extended'].replace(' ', '').lower()
    tags = p['tags'].lower()
    toread = p['toread']

    if q=="":
        if category=='toread':
            if toread=='yes':            
                results.append({'title':p['description'],'url':p['href']})
        else: 
            results.append({'title':p['description'],'url':p['href']})
    else:
        if category=='title' and q in title:
            results.append({'title':p['description'],'url':p['href']})
        elif category=='link' and q in url:
            results.append({'title':p['description'],'url':p['href']})
        elif category=='description' and q in extended:
            results.append({'title':p['description'],'url':p['href']})
        elif category=='toread' and q in title and toread=='yes':
            results.append({'title':p['description'],'url':p['href']})
        elif category=='all' and (q in title or q in url or q in tags):
            results.append({'title':p['description'],'url':p['href']})

resultData = [alfred.Item(title=f['title'].encode('utf-8'), subtitle=f['url'].encode('utf-8'), attributes = {'arg':f['url']}, icon="item.png") for f in results]
pinboard_url = 'https://pinboard.in/search/?query=%s&mine=Search+Mine'%q
resultData.append(alfred.Item(title='Search "%s" in pinboard.in'%q, subtitle=pinboard_url, attributes={'arg':pinboard_url}, icon="icon.png"))
alfred.write(alfred.xml(resultData,maxresults=None))
