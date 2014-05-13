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
import time

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger('com.jmjeong.alfredv2.pinboard')
hdlr = logging.FileHandler('/var/tmp/alfred.pinboard.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.ERROR)

PIN_MAX_RESULT = -1
UPDATE_BOOKMARK_THRESHOLD = 4
DELETE_OLDBOOKMARK_THRESHOLD = 60*60*24*14 # 14 days
STAR = u"\u2605 "

def config_data():
    try:
        config = json.loads(open(os.path.join(alfred.work(False), 'config.json')).read())
    except:
        config = {}
    return config

def pins_data():
    try:
        filename = os.environ['HOME']+'/.bookmarks.json'
        pins = json.loads(open(filename, 'r').read())
    except:
        pins = {}
    return pins

def notes_data():
    try:
        filename = os.environ['HOME']+'/.bookmarks-note.json'
        return json.loads(open(filename, 'r').read())
    except:
        return {}

def deleted_url_data():
    try:
        return json.loads(open(os.path.join(alfred.work(False),'deleted-url.json')).read())
    except IOError:
        return []

def starred_url_data():
    try:
        return json.loads(open(os.path.join(alfred.work(False),'starred-url.json')).read())
    except IOError:
        return []

def history_data():
    try:
        return json.loads(open(os.path.join(alfred.work(False),'search-history.json')).read())
    except IOError:
        return []

def update_history(category,q,nums):
    if q=="" or nums==0: return
    if category != "all" and category != 'tags': return
    
    history = history_data()
    now = int(time.time())
    found = None

    for h in history:
        if (h[1] in q or q in h[1]) and now-h[3] <= UPDATE_BOOKMARK_THRESHOLD:
            if not h[4]: history.remove(h)
        elif h[1] == q:
            found = h
        elif now-h[3] > DELETE_OLDBOOKMARK_THRESHOLD:
            if not h[4]: history.remove(h)

    if found:
        found[2:3] = (nums,now)
    else:
        if category == "all":
            history.append(["pba",q,nums,now,False])
        elif category == "tags":
            history.append(["pbtag",q,nums,now,False])

    with open(os.path.join(alfred.work(False), 'search-history.json'), 'w+') as myFile:
        myFile.write(json.dumps(history))

def help():
    result = []
    result.append(alfred.Item(title='Look up Documentation', subtitle='Goto project site', attributes={'arg':'http://j.mp/1c4E6Q2','uid':alfred.uid(0)}, icon="icon.png"))
    result.append(alfred.Item(title='pbauth username:token', subtitle='set pinboard authentication token', attributes={'valid':'no','uid':alfred.uid(1)}, icon="icon.png"))
    result.append(alfred.Item(title='pbreload', subtitle='load latest bookmarks from pinboard.in', attributes={'valid':'no','uid':alfred.uid(2)}, icon="icon.png"))
    result.append(alfred.Item(title='pba query', subtitle='search all fields of bookmarks', attributes={'valid':'no','uid':alfred.uid(3)}, icon="icon.png"))
    result.append(alfred.Item(title='pbtag', subtitle='display tags list', attributes={'valid':'no','uid':alfred.uid(7)}, icon="icon.png"))
    result.append(alfred.Item(title='pbnote query', subtitle='display note list', attributes={'valid':'no','uid':alfred.uid(10)}, icon="icon.png"))
    result.append(alfred.Item(title='pbl query', subtitle='search link of bookmarks', attributes={'valid':'no','uid':alfred.uid(5)}, icon="icon.png"))
    result.append(alfred.Item(title='pbu query', subtitle='search title of toread bookmarks', attributes={'valid':'no','uid':alfred.uid(8)}, icon="icon.png"))
    result.append(alfred.Item(title='pbauthpocket', subtitle='Login with Pocket!', attributes={'valid':'no','uid':alfred.uid(1)}, icon="icon.png"))
    
    # result.append(alfred.Item(title='pbt query', subtitle='search description of bookmarks', attributes={'valid':'no','uid':alfred.uid(4)}, icon="icon.png"))
    # result.append(alfred.Item(title='pbd query', subtitle='search extended field of bookmarks', attributes={'valid':'no','uid':alfred.uid(6)}, icon="icon.png"))
    result.append(alfred.Item(title='To selected bookmark', subtitle='enter:goto site, cmd:copy url, alt:delete bookmark, tab:expand', attributes={'valid':'no','uid':alfred.uid(9)}, icon="icon.png"))
    alfred.write(alfred.xml(result,maxresults=None))

def pbauth(q):
    try:
        (user,token) = q.split(':')
    except:
        print 'Invalid Token'
        sys.exit(0)

    config = config_data()
        
    config['pinboard_username'] = user
    config['pinboard_token'] = token

    with open(os.path.join(alfred.work(False), 'config.json'), 'w+') as myFile:
        myFile.write(json.dumps(config))

    print "Authentication Token Saved"

def pbauthpocket(q):
    ret = pocket.getRequestCode()
    
    config = config_data()
    config['pocket_request_code'] = ret['code']
    
    with open(os.path.join(alfred.work(False), 'config.json'), 'w+') as myFile:
        myFile.write(json.dumps(config))
    
    result = [alfred.Item(title='Login!', subtitle='Login with Pocket.com (you will be taken to pocket.com)', attributes={'arg':ret['code'],'uid':alfred.uid(0)}, icon="icon.png")]
    alfred.write(alfred.xml(result))

def addpocket(q):
    pocket.addpocket(q)

def pbtag(pins,deleted_url,starred_url,q):
    if not "→" in q:                      # tag search
        q = q.lower()
        tag_list = {}
        for p in pins:
            url = p['href']
            if url in map(lambda x:x.lower(), deleted_url): continue
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
                resultData.append(alfred.Item(title=i+"("+str(tag_list[i])+")→", subtitle='', attributes={'arg':i, 'autocomplete':i+"→",'uid':alfred.uid(idx)}, icon='icon.png'))
        alfred.write(alfred.xml(resultData,maxresults=None))
    else:
        (q_tag, q_title)=q.split("→")
        qs = q_title.lower()
        results = []
        for p in pins:
            url = p['href']
            if url in map(lambda x:x.lower(), deleted_url): continue
            title = p['description'].lower()
            tags = p['tags'].split(' ')
            for t in tags:
                if not q_tag in t: continue
                if not qs:
                    results.append({'title':(p['href'] in starred_url and STAR or "")+p['description'],'url':url})
                elif all(qsi and pred(qsi,[title]) for qsi in qs.split(' ')):
                    results.append({'title':(p['href'] in starred_url and STAR or "")+p['description'],'url':url})
                    break
            if PIN_MAX_RESULT>0 and len(results)>PIN_MAX_RESULT: break
        resultData = [alfred.Item(title=f['title'], subtitle=f['url'],attributes={'arg':f['url'],'uid':alfred.uid(i)},icon="item.png") for (i,f) in enumerate(results)]
        resultData.insert(0,alfred.Item(title="Links: %d items"%len(results), subtitle="", attributes={'valid':'no','uid':alfred.uid('t')}, icon="icon.png"))
        
        pinboard_url = q_title and 'https://pinboard.in/search/?query=%s&mine=Search+Mine'%q_title.replace(' ','+') or 'https://pinboard.in/'
        pinboard_title = q_title and 'Search \'%s\' in pinboard.in'%q_title or 'Goto pinboard site'
        resultData.append(alfred.Item(title=pinboard_title, subtitle=pinboard_url, attributes={'arg':pinboard_url}, icon="icon.png"))
        alfred.write(alfred.xml(resultData,maxresults=None))
        update_history("tags",q,len(results))

def pred(q, string_list):
    qs = q.lstrip('-')
    if qs==q:       # query (or)
        return any(qs in s for s in string_list)
    else:           # -query (and)
        return all(qs not in s for s in string_list)

def pbnote(notes,config,deleted_url,q):
    results = []
    qs = q.lower()
    logger.info('query string = [%s]', qs)

    for n in notes['notes']:
        try:
            url = "https://notes.pinboard.in/u:%s/%s"%(config['pinboard_username'],n['id'])
        except KeyError:
            url = "https://notes.pinboard.in/"
        if url in map(lambda x:x.lower(), deleted_url): continue
        
        title = n['title'].lower()
        text = n['text'].lower()
        
        if not qs:
            results.append({'title':n['title'],'url':url,'subtitle':text,'time':n['created_at']})
        else:
            if all(qsi and pred(qsi,[title,text]) for qsi in qs.split(' ')):
                results.append({'title':n['title'],'url':url,'subtitle':text,'time':n['created_at']})
        if PIN_MAX_RESULT>0 and len(results)>PIN_MAX_RESULT: break

    results.sort(key=lambda s:s['time'],reverse=True)
    resultData = [alfred.Item(title=f['title'], subtitle=f['subtitle'], attributes={'arg':f['url'],'uid':alfred.uid(idx)}, icon="item.png") for (idx,f) in enumerate(results)]
    resultData.insert(0,alfred.Item(title="Notes: %d items"%len(results), subtitle="", attributes={'valid':'no','uid':alfred.uid('t')}, icon="icon.png"))
    pinboard_url = q and 'https://pinboard.in/search/?query=%s&mine=Search+Mine'%q.replace(' ','+') or 'https://notes.pinboard.in/'
    pinboard_title = q and 'Search \'%s\' in pinboard.in'%q or 'Goto Pinboard Notes'
    resultData.append(alfred.Item(title=pinboard_title, subtitle=pinboard_url, attributes={'arg':pinboard_url}, icon="icon.png"))
    alfred.write(alfred.xml(resultData,maxresults=None))

def pbsearch(pins,deleted_url,starred_url,q,category):
    results = []
    qs = q.lower()
    logger.info('query string = [%s]', qs)

    for p in pins:
        title = p['description'].lower()
        url = p['href'].lower()
        extended = p['extended'].lower()
        tags = p['tags'].lower()
        toread = p['toread']

        if url in map(lambda x:x.lower(), deleted_url): continue

        if not qs:
            if category=='toread':
                if toread=='yes':            
                    results.append({'title':(p['href'] in starred_url and STAR or "")+p['description'],'url':p['href']})
            elif category=='star':
                if p['href'] in starred_url:
                    results.append({'title':(p['href'] in starred_url and STAR or "")+p['description'],'url':p['href']})
            else:
                results.append({'title':(p['href'] in starred_url and STAR or "")+p['description'],'url':p['href']})
        else:
            if category=='all' and all(qsi and pred(qsi,[title,extended,tags]) for qsi in qs.split(' ')):
                results.append({'title':(p['href'] in starred_url and STAR or "")+p['description'],'url':p['href']})
            if category=='star' and p['href'] in starred_url and all(qsi and pred(qsi,[title,extended,tags]) for qsi in qs.split(' ')):
                results.append({'title':(p['href'] in starred_url and STAR or "")+p['description'],'url':p['href']})
            elif category=='toread' and toread=='yes' and all(qsi and pred(qsi,[title]) for qsi in qs.split(' ')):
                results.append({'title':(p['href'] in starred_url and STAR or "")+p['description'],'url':p['href']})
            elif category=='link' and any(qsi and pred(qsi,[url]) for qsi in qs.split(' ')):
                results.append({'title':(p['href'] in starred_url and STAR or "")+p['description'],'url':p['href']})
            # elif category=='title' and any(qsi and qsi in title for qsi in qs.split(' ')):
            #     results.append({'title':p['description'],'url':p['href']})
            # elif category=='description' and any(qsi in extended for qsi in qs.split(' ')):
            #     results.append({'title':p['description'],'url':p['href']})
        if PIN_MAX_RESULT>0 and len(results)>PIN_MAX_RESULT: break

    logger.info(category)
    resultData = [alfred.Item(title=f['title'], subtitle=f['url'], attributes={'arg':f['url'],'uid':alfred.uid(idx)}, icon="item.png") for (idx,f) in enumerate(results)]
    resultData.insert(0,alfred.Item(title="Links: %d items"%len(results), subtitle="", attributes={'valid':'no','uid':alfred.uid('t')}, icon="icon.png"))
    pinboard_url = q and 'https://pinboard.in/search/?query=%s&mine=Search+Mine'%q.replace(' ','+') or 'https://pinboard.in/'
    pinboard_title = q and 'Search \'%s\' in pinboard.in'%q or 'Goto Pinboard'
    resultData.append(alfred.Item(title=pinboard_title, subtitle=pinboard_url, attributes={'arg':pinboard_url}, icon="icon.png"))
    alfred.write(alfred.xml(resultData,maxresults=None))
    update_history(category,q,len(results))

if __name__ == '__main__':
    # arg parsing
    category = sys.argv[1]
    try:
        q = unicode(sys.argv[2].strip())
        q = unicodedata.normalize('NFC', q)
    except:
        q = ""
    
    if category=='help':
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

    # tag processing
    if category=='tags':
        pins = pins_data()
        deleted_url = deleted_url_data()
        starred_url = starred_url_data()
        pbtag(pins,deleted_url,starred_url,q)
    elif category=='note':
        notes = notes_data()
        config = config_data()
        deleted_url = deleted_url_data()
        pbnote(notes,config,deleted_url,q)
    else:
        pins = pins_data()
        deleted_url = deleted_url_data()
        starred_url = starred_url_data()
        pbsearch(pins,deleted_url,starred_url,q,category)
