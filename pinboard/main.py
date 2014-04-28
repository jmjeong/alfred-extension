#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# jmjeong, 2014/02/19

import alfred
import os
import json
import unicodedata
import logging
import pocket

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger('com.jmjeong.alfredv2.pinboard')
hdlr = logging.FileHandler('/var/tmp/alfred.pinboard.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.ERROR)

PIN_MAX_RESULT=80

def config_data():
    try:
        config=json.loads(open('config.json').read())
    except:
        config={}
    return config

def help():
    result = []
    result.append(alfred.Item(title='Look up Documentation', subtitle='Goto project site', attributes={'arg':'http://j.mp/1c4E6Q2','uid':alfred.uid(0)}, icon="icon.png"))
    result.append(alfred.Item(title='pbauth username:token', subtitle='set pinboard authentication token', attributes={'valid':'no','uid':alfred.uid(1)}, icon="icon.png"))
    result.append(alfred.Item(title='pbreload', subtitle='load latest bookmarks from pinboard.in', attributes={'valid':'no','uid':alfred.uid(2)}, icon="icon.png"))
    result.append(alfred.Item(title='pba query', subtitle='search all fields of bookmarks', attributes={'valid':'no','uid':alfred.uid(3)}, icon="icon.png"))
    result.append(alfred.Item(title='pbt query', subtitle='search description of bookmarks', attributes={'valid':'no','uid':alfred.uid(4)}, icon="icon.png"))
    result.append(alfred.Item(title='pbl query', subtitle='search link of bookmarks', attributes={'valid':'no','uid':alfred.uid(5)}, icon="icon.png"))
    result.append(alfred.Item(title='pbd query', subtitle='search extended field of bookmarks', attributes={'valid':'no','uid':alfred.uid(6)}, icon="icon.png"))
    result.append(alfred.Item(title='pbtag tag query', subtitle='display tags list', attributes={'valid':'no','uid':alfred.uid(7)}, icon="icon.png"))
    result.append(alfred.Item(title='pbu query', subtitle='search title of toread bookmarks', attributes={'valid':'no','uid':alfred.uid(8)}, icon="icon.png"))
    result.append(alfred.Item(title='To selected bookmark', subtitle='enter:goto site, cmd:copy url, alt:delete bookmark, tab:expand', attributes={'valid':'no','uid':alfred.uid(9)}, icon="icon.png"))
    alfred.write(alfred.xml(result))

def pbauth(q):
    try:
        (user,token)=q.split(':')
    except:
        print 'Invalid Token'
        sys.exit(0)

    config = config_data()
        
    config['pinboard_username']=user
    config['pinboard_token']=token

    with open('config.json', 'w+') as myFile:
        myFile.write(json.dumps(config))

    print "Authentication Token Saved"

def pbauthpocket(q):
    ret = pocket.getRequestCode()
    
    config=config_data()
    config['pocket_request_code']=ret['code']
    
    with open('config.json', 'w+') as myFile:
        myFile.write(json.dumps(config))
    
    result = [alfred.Item(title='Login!', subtitle='Login with Pocket.com (you will be taken to pocket.com)', attributes={'arg':ret['code'],'uid':alfred.uid(0)}, icon="icon.png")]
    alfred.write(alfred.xml(result))

def addpocket(q):
    pocket.addpocket(q)

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
        for (idx,i) in enumerate(tag_list_key):
            if not q or q in i.lower():
                resultData.append(alfred.Item(title="tag:"+i+"("+str(tag_list[i])+")→", subtitle='', attributes={'arg':i, 'autocomplete':i+"→",'uid':"p-%04d"%idx}, icon='icon.png'))
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
            if len(results)>PIN_MAX_RESULT: break
        resultData = [alfred.Item(title=f['title'].encode('utf-8'), subtitle=f['url'].encode('utf-8'),attributes={'arg':f['url'].replace(' ','%20'),'uid':"p-%04d"%i},icon="item.png") for (i,f) in enumerate(results)]
        pinboard_url = q_title and 'https://pinboard.in/search/?query=%s&mine=Search+Mine'%q_title.replace(' ','+') or 'https://pinboard.in/'
        pinboard_title = q_title and 'Search \'%s\' in pinboard.in'%q_title or 'Goto pinboard site'
        resultData.append(alfred.Item(title=pinboard_title, subtitle=pinboard_url, attributes={'arg':pinboard_url}, icon="icon.png"))
        alfred.write(alfred.xml(resultData,maxresults=None))

def search(pins,deleted_url,q,category):
    results = []
    q = q.lower()
    qs = q.replace(' ', '')
    logger.info('query string = [%s]', qs)

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
                    results.append({'title':p['description'],'url':p['href'],'valid':'YES'})
            else:
                results.append({'title':p['description'],'url':p['href'],'valid':'YES'})
        else:
            if category=='title' and qs in title:
                results.append({'title':p['description'],'url':p['href'], 'valid':'YES'})
            elif category=='link' and qs in url:
                results.append({'title':p['description'],'url':p['href']})
            elif category=='description' and qs in extended:
                results.append({'title':p['description'],'url':p['href']})
            elif category=='toread' and qs in title and toread=='yes':
                results.append({'title':p['description'],'url':p['href']})
            elif category=='all' and (qs in title or qs in url or qs in tags):
                results.append({'title':p['description'],'url':p['href']})
        if len(results)>PIN_MAX_RESULT: break

    logger.info(category)
    resultData = [alfred.Item(title=f['title'].encode('utf-8'), subtitle=f['url'].encode('utf-8'), attributes = {'arg':f['url'].replace(' ','%20'),'uid':"p-%04d"%idx}, icon="item.png") for (idx,f) in enumerate(results)]

    pinboard_url = q and 'https://pinboard.in/search/?query=%s&mine=Search+Mine'%q.replace(' ','+') or 'https://pinboard.in/'
    pinboard_title = q and 'Search \'%s\' in pinboard.in'%q or 'Goto pinboard site'
    resultData.append(alfred.Item(title=pinboard_title, subtitle=pinboard_url, attributes={'arg':pinboard_url}, icon="icon.png"))

    xml = alfred.xml(resultData,maxresults=None)
    logger.info(xml)
    alfred.write(' '+xml)
    logger.info("write finished")

if __name__ == '__main__':
    
    try:
        filename = os.environ['HOME']+'/.bookmarks.json'
        pins = json.loads(open(filename, 'r').read())
    except:
        pins = {}

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
    elif category=='help':
        help()
        sys.exit(0)
    elif category=='pbauth':
        pbauth(q)
        sys.exit(0)
    elif category=='pbauthpocket':
        pbauthpocket(q)
        sys.exit(0)
    elif category=='addpocket':
        addpocket(q)
        sys.exit(0)

    # search query
    search(pins,deleted_url,q,category)
