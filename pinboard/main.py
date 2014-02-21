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
    result = [alfred.Item(title='Setup incomplete', subtitle='look up documentation. press enter.', attributes={'arg':'http://j.mp/1c4E6Q2'}, icon="icon.png")]
    alfred.write(alfred.xml(result))

def tags(pins,deleted_url,q):
    if not "→" in q:                      # tag search
        q = q.lower()
        tag_list = {}
        for p in pins:
            url = p['href']
            if url in deleted_url: continue
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
            if not q or q in i.lower():
                resultData.append(alfred.Item(title="tag:"+i+"("+str(tag_list[i])+")→", subtitle='', attributes={'arg':i, 'autocomplete':i+"→"}, icon='icon.png'))
        alfred.write(alfred.xml(resultData,maxresults=None))
    else:
        (q_tag, q_title)=q.split("→")
        qs = q_title.lower()
        results=[]
        for p in pins:
            url = p['href']
            if url in deleted_url: continue
            title = p['description'].replace(' ', '').lower()
            tags = p['tags'].split(' ')
            for t in tags:
                if (q_tag in t) and (not qs or qs in title or qs in p['tags']):
                    results.append({'title':p['description'],'url':url})
                    break
        resultData = [alfred.Item(title=f['title'].encode('utf-8'), subtitle=f['url'].encode('utf-8'), attributes = {'arg':f['url'].replace(' ','%20')}, icon="item.png") for f in results]
        pinboard_url = q_title and 'https://pinboard.in/search/?query=%s&mine=Search+Mine'%q_title.replace(' ','+') or 'https://pinboard.in/'
        pinboard_title = q_title and 'Search \'%s\' in pinboard.in'%q_title or 'Goto pinboard site'
        resultData.append(alfred.Item(title=pinboard_title, subtitle=pinboard_url, attributes={'arg':pinboard_url}, icon="icon.png"))
        alfred.write(alfred.xml(resultData,maxresults=None))
    sys.exit(0)

def auth(q):
    if not q:
        alfred.write(alfred.xml([alfred.Item(title='Set Pinboard Authentication Token', subtitle='you can get it from https://pinboard.in/settings/', attributes={'valid':'no'}, icon="icon.png")]))
    else:
        alfred.write(alfred.xml([alfred.Item(title='Set Pinboard Authentication Token', subtitle='username:XXXXXXXXXXXXXXXXXXX', attributes={'arg':q}, icon="icon.png")]))        

# start routine
try:
    filename = os.environ['HOME']+'/.bookmarks.json'
    pins = json.loads(open(filename, 'r').read())
except:
    intro()
    sys.exit(0)

try:
    deleted_url=json.loads(open('deleted-url.json').read())
except IOError:
    deleted_url=[]

# arg parsing
category = sys.argv[1]
try:
    q = unicode(sys.argv[2].strip())
    q = unicodedata.normalize('NFC', q)
except:
    q = ""

# tag processing
if category=='tags':
    tags(pins,deleted_url,q)
    sys.exit(0)
elif category=='auth':
    auth(q)
    sys.exit(0)
    
results = []
q = q.lower()
qs = q.replace(' ', '')

for p in pins:
    title = p['description'].replace(' ', '').lower()
    url = p['href'].lower()
    extended = p['extended'].replace(' ', '').lower()
    tags = p['tags'].lower()
    toread = p['toread']
    
    if url in deleted_url: continue

    if qs=="":
        if category=='toread':
            if toread=='yes':            
                results.append({'title':p['description'],'url':p['href']})
        else: 
            results.append({'title':p['description'],'url':p['href']})
    else:
        if category=='title' and qs in title:
            results.append({'title':p['description'],'url':p['href']})
        elif category=='link' and qs in url:
            results.append({'title':p['description'],'url':p['href']})
        elif category=='description' and qs in extended:
            results.append({'title':p['description'],'url':p['href']})
        elif category=='toread' and qs in title and toread=='yes':
            results.append({'title':p['description'],'url':p['href']})
        elif category=='all' and (qs in title or qs in url or qs in tags):
            results.append({'title':p['description'],'url':p['href']})

resultData = [alfred.Item(title=f['title'].encode('utf-8'), subtitle=f['url'].encode('utf-8'), attributes = {'arg':f['url'].replace(' ','%20')}, icon="item.png") for f in results]
pinboard_url = q and 'https://pinboard.in/search/?query=%s&mine=Search+Mine'%q.replace(' ','+') or 'https://pinboard.in/'
pinboard_title = q and 'Search \'%s\' in pinboard.in'%q or 'Goto pinboard site'
resultData.append(alfred.Item(title=pinboard_title, subtitle=pinboard_url, attributes={'arg':pinboard_url}, icon="icon.png"))
alfred.write(alfred.xml(resultData,maxresults=None))
