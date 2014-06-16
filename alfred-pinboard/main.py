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
import urlparse
import util
import re

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger('com.jmjeong.alfredv2.pinboard')
hdlr = logging.FileHandler('/var/tmp/alfred.pinboard.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

PIN_MAX_RESULT = -1
UPDATE_BOOKMARK_THRESHOLD = 4
DELETE_OLDBOOKMARK_THRESHOLD = 60*60*24*14 # 14 days
RELOAD_ASK_THRESHOLD = 60*60*12            # 12 hours
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
        sh = h[1].replace(' ', '')
        sq = q.replace(' ', '')
        if (sh in sq or sq in sh) and now-h[3] <= UPDATE_BOOKMARK_THRESHOLD:
            if not h[4]: history.remove(h)
        elif sh == sq:
            found = h
        elif now-h[3] > DELETE_OLDBOOKMARK_THRESHOLD:
            if not h[4]: history.remove(h)

    if found:
        found[2:4] = (nums,now)
    else:
        if category == "all":
            history.append(["pba",q,nums,now,False])
        elif category == "tags":
            history.append(["pbtag",q,nums,now,False])

    with open(os.path.join(alfred.work(False), 'search-history.json'), 'w+') as myFile:
        myFile.write(json.dumps(history))

def help():
    result = []
    result.append(alfred.Item(title='Look up Documentation', subtitle='Goto project site', attributes={'arg':'https://github.com/jmjeong/alfred-extension/blob/master/alfred-pinboard/README.md','uid':alfred.uid(0)}, icon="icon.png"))
    result.append(alfred.Item(title='pbauth username:token', subtitle='set pinboard authentication token', attributes={'valid':'no','uid':alfred.uid(1)}, icon="icon.png"))
    result.append(alfred.Item(title='pbreload', subtitle='load latest bookmarks from pinboard.in', attributes={'valid':'no','uid':alfred.uid(2)}, icon="icon.png"))
    result.append(alfred.Item(title='pba query', subtitle='search all fields of bookmarks', attributes={'valid':'no','uid':alfred.uid(3)}, icon="icon.png"))
    result.append(alfred.Item(title='pbtag', subtitle='display tags list', attributes={'valid':'no','uid':alfred.uid(7)}, icon="icon.png"))
    result.append(alfred.Item(title='pbnote query', subtitle='display note list', attributes={'valid':'no','uid':alfred.uid(10)}, icon="icon.png"))
    result.append(alfred.Item(title='pbl query', subtitle='search link of bookmarks', attributes={'valid':'no','uid':alfred.uid(5)}, icon="icon.png"))
    result.append(alfred.Item(title='pbu query', subtitle='search title of toread bookmarks', attributes={'valid':'no','uid':alfred.uid(8)}, icon="icon.png"))
    result.append(alfred.Item(title='pbauthpocket', subtitle='Login with Pocket!', attributes={'valid':'no','uid':alfred.uid(1)}, icon="icon.png"))
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

def pred(q, string_list):
    qs = q.lstrip('-')
    if qs=="":
        return True
    elif qs==q:       # query (or)
        return any(qs in s for s in string_list)
    else:             # -query (and)
        return all(qs not in s for s in string_list)

def pbnote(notes,config,deleted_url,q):
    results = []
    qs = map(lambda a:a.strip(), q.lower().split('|'))
    logger.info('query string = [%s]', qs)

    for n in notes['notes']:
        try:
            url = "https://notes.pinboard.in/u:%s/%s"%(config['pinboard_username'],n['id'])
        except KeyError:
            url = "https://notes.pinboard.in/"
        if url in map(lambda x:x.lower(), deleted_url): continue
        
        title = n['title'].lower()
        text = n['text'].lower()
        
        if not q:
            results.append({'title':n['title'],'url':url,'subtitle':text,'time':n['created_at']})
        else:
            for qi in qs:
                if all(qsi and pred(qsi,[title,text]) for qsi in qi.split(' ')):
                    results.append({'title':n['title'],'url':url,'subtitle':text,'time':n['created_at']})
                    break
        if PIN_MAX_RESULT>0 and len(results)>=PIN_MAX_RESULT: break
    results.sort(key=lambda s:s['time'],reverse=True)
    resultData = [alfred.Item(title=f['title'], subtitle=f['subtitle'], attributes={'arg':f['url'],'uid':alfred.uid(idx)}, icon="item.png") for (idx,f) in enumerate(results)]
    resultData.insert(0,alfred.Item(title="Notes: %d items"%len(results), subtitle="", attributes={'valid':'no','uid':alfred.uid('t')}, icon="icon.png"))
    pinboard_url = q and 'https://pinboard.in/search/?query=%s&mine=Search+Mine'%q.replace(' ','+') or 'https://notes.pinboard.in/'
    pinboard_title = q and 'Search \'%s\' in pinboard.in'%q or 'Goto Pinboard Notes'
    resultData.append(alfred.Item(title=pinboard_title, subtitle=pinboard_url, attributes={'arg':pinboard_url}, icon="icon.png"))
    alfred.write(alfred.xml(resultData,maxresults=None))


def process_tag(pins,deleted_url,q,prefix):
    tag_list = {}
    
    for p in pins:
        url = p['href']
        if url in map(lambda x:x.lower(), deleted_url): continue
        tags = p['tags'].encode('utf-8').split(' ')
        for t in tags:
            if t in tag_list:
                tag_list[t] += 1
            else:
                tag_list[t] = 1
    resultData = []
    tag_list_key = sorted(tag_list.keys(),key=str.lower)
    for (idx,i) in enumerate(tag_list_key):
        if not q or q in i.lower():
            expand_str = prefix+(prefix and " " or "")+"#"+i+" : "
            resultData.append(alfred.Item(title=(i and i or "untagged")+" ("+str(tag_list[i])+")", subtitle='',
                                          attributes={'autocomplete':expand_str,
                                                      'valid':'no',
                                                      'uid':alfred.uid(idx)}, icon='tag.png'))
    alfred.write(alfred.xml(resultData,maxresults=None))
    return

def total_num(pins,deleted_url,tags_list,category):
    count = 0
    for p in pins:
        url = p['href'].lower()
        if url in map(lambda x:x.lower(), deleted_url): continue
        
        tags = p['tags'].lower()
        tag_set = set(tags.split(' '))
        if tags_list and tag_set.isdisjoint(tags_list): continue

        if category=='toread':
            if toread=='yes':            
                count += 1
        elif category=='star':
            if p['href'] in starred_url:
                count += 1
        else:
            count += 1
    return str(count)

def process_search(pins,config,deleted_url,starred_url,tags_list,q,full_query,category,sort_option):
    results = []
    qs = map(lambda a:a.strip(), q.lower().split('|'))

    for p in pins:
        url = p['href'].lower()
        if url in map(lambda x:x.lower(), deleted_url): continue
        
        title = p['description'].lower()
        extended = p['extended'].lower()
        tags = p['tags'].lower()
        toread = p['toread']

        tag_set = set(tags.split(' '))
        if tags_list and tag_set.isdisjoint(tags_list): continue

        tagstring = tags and "("+", ".join(map(lambda a:'#'+a, tags.split(' ')))+")" or "(none)"
        if not q:
            if category=='toread':
                if toread=='yes':            
                    results.append({'title':(p['href'] in starred_url and STAR or "")+p['description'],'url':p['href'],'tags':tagstring})
            elif category=='star':
                if p['href'] in starred_url:
                    results.append({'title':(p['href'] in starred_url and STAR or "")+p['description'],'url':p['href'],'tags':tagstring})
            else:
                results.append({'title':(p['href'] in starred_url and STAR or "")+p['description'],'url':p['href'],'tags':tagstring})
        else:
            for qi in qs:
                if category=='all' and all(qsi and pred(qsi,[title,extended,tags]) for qsi in qi.split(' ')):
                    results.append({'title':(p['href'] in starred_url and STAR or "")+p['description'],'url':p['href'],'tags':tagstring})
                    break
                if category=='star' and p['href'] in starred_url and all(qsi and pred(qsi,[title,extended,tags]) for qsi in qi.split(' ')):
                    results.append({'title':(p['href'] in starred_url and STAR or "")+p['description'],'url':p['href'],'tags':tagstring})
                    break
                elif category=='toread' and toread=='yes' and all(qsi and pred(qsi,[title]) for qsi in qi.split(' ')):
                    results.append({'title':(p['href'] in starred_url and STAR or "")+p['description'],'url':p['href'],'tags':tagstring})
                    break
                elif category=='link' and any(qsi and pred(qsi,[url]) for qsi in qi.split(' ')):
                    results.append({'title':(p['href'] in starred_url and STAR or "")+p['description'],'url':p['href'],'tags':tagstring})
                    break
        if PIN_MAX_RESULT>0 and len(results)>=PIN_MAX_RESULT: break
    logger.info(category)
    if sort_option=='a' or sort_option=='ㅇ': results = sorted(results, key=lambda k:k['title'])
    elif sort_option=='z' or sort_option=='ㅁ': results = sorted(results, key=lambda k:k['title'],reverse=True)
    elif sort_option=='d' or sort_option=='ㅣ': results.reverse()
    resultData = [alfred.Item(title=f['title'], subtitle=urlparse.urlparse(f['url'])[1]+"   "+f['tags'], attributes={'arg':f['url'],'uid':alfred.uid(idx)}, icon="item.png") for (idx,f) in enumerate(results)]
    try:
        last_updated = config['last_updated']
    except:
        last_updated = 0
    subtitle = "Last updated: "+(last_updated and util.pretty_date(config['last_updated']) or "no info")
    
    diff = int(time.time())-last_updated
    if diff > RELOAD_ASK_THRESHOLD:
        resultData.insert(0,alfred.Item(title="Links: %d items - Reload pinboard data?"%len(results), subtitle=subtitle,
                                        attributes={'arg':'reload','uid':alfred.uid('t')}, icon="icon.png"))
    else:
        resultData.insert(0,alfred.Item(title="Links: %d items"%len(results), subtitle=subtitle,
                                        attributes={'valid':'no','uid':alfred.uid('t')}, icon="icon.png"))
    pinboard_url = q and 'https://pinboard.in/search/?query=%s&mine=Search+Mine'%q.replace(' ','+') or 'https://pinboard.in/'
    pinboard_title = q and 'Search \'%s\' in pinboard.in'%q or 'Goto Pinboard'
    resultData.append(alfred.Item(title=pinboard_title, subtitle=pinboard_url, attributes={'arg':pinboard_url}, icon="icon.png"))
    alfred.write(alfred.xml(resultData,maxresults=None))
    update_history(category,full_query,len(results))
    return

def process_sortoption(q):
    result = []
    result.append(alfred.Item(title='time ascending', subtitle='^d ',
                              attributes={'valid':'no','autocomplete':q+(q and " " or "")+'^d ','uid':alfred.uid(1)}, icon="general-des.png"))
    result.append(alfred.Item(title='title ascending', subtitle='^a ',
                              attributes={'valid':'no','autocomplete':q+(q and " " or "")+'^a ','uid':alfred.uid(2)}, icon="alpha-asc.png"))
    result.append(alfred.Item(title='title descending', subtitle='^z ',
                              attributes={'valid':'no','autocomplete':q+(q and " " or "")+'^z ','uid':alfred.uid(3)}, icon="alpha-des.png"))
    alfred.write(alfred.xml(result,maxresults=None))
    
def pbsearch(pins,config,deleted_url,starred_url,q,category):
    logger.info('query string = [%s]', q)

    sort_option = ""
    full_query = q
    sort_re = re.compile(r'\^(\w+)\b', flags=re.U)
    if sort_re.findall(q):  # exists sort option?
        sort_option = sort_re.findall(q)[-1]
        q = sort_re.sub('', q)
        
    last_q = q.split(' ')[-1]
    if last_q.startswith('^'):      # sort option
        process_sortoption(" ".join(q.split(' ')[:-1]))
    elif last_q.startswith('#'):      # tag expansion
        process_tag(pins,deleted_url,last_q.lower()[1:]," ".join(q.split(' ')[:-1]))
    elif ':' in q:
        qq = q.split(':')
        query = qq[-1]
        tags = ':'.join(qq[:-1])
        tag_list = [t[1:].lower() for t in tags.split(' ') if t.startswith('#')]
        # logger.error('taglist = %s, query=[%s]', tag_list,query)
        process_search(pins,config,deleted_url,starred_url,tag_list,query.strip(),full_query,category,sort_option)
    elif '#' in q and ':' not in q:
        expand_str = q.strip()+' : '
        tag_list = [t[1:].lower() for t in q.split(' ') if t.startswith('#')]
        resultData = [alfred.Item(title="Selected Category ("+total_num(pins,deleted_url,tag_list,category)+")",
                                  subtitle="# or : or Enter",
                                  attributes={'uid':alfred.uid(0),
                                              'autocomplete':expand_str,
                                              'valid':'no'},
                                  icon="item.png")]
        alfred.write(alfred.xml(resultData,maxresults=None))
    else:
        process_search(pins,config,deleted_url,starred_url,[],q.strip(),full_query,category,sort_option)

def main():
    # arg parsing
    category = sys.argv[1]
    try:
        q = unicode(sys.argv[2])
        q = unicodedata.normalize('NFC', q)
    except:
        q = ""
    
    if category=='help':
        help()
    elif category=='pbauth':
        pbauth(q)
    elif category=='pbauthpocket':
        pbauthpocket(q)
    elif category=='note':
        notes = notes_data()
        config = config_data()
        deleted_url = deleted_url_data()
        pbnote(notes,config,deleted_url,q)
    else:
        pins = pins_data()
        config = config_data()
        deleted_url = deleted_url_data()
        starred_url = starred_url_data()
        pbsearch(pins,config,deleted_url,starred_url,q,category)
    
if __name__ == '__main__':
    start = time.clock()
    main()
    end = time.clock()
    logger.info("Elapsed time : %.5gs"%(end-start))
