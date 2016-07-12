#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# jmjeong, 2014/02/19

import os
import json
import unicodedata
import urlparse
import sqlite3
import util
import applescript
import urllib
import time
import re
from statsd import StatsClient

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

title_pattern=re.compile('(.*?)[\.:\|\-]+')
# title_pattern=re.compile('(.*)')

def pretty_date(time=False):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    """
    from datetime import datetime
    now = datetime.now()
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time,datetime):
        diff = now - time 
    elif not time:
        diff = now - now
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(second_diff) + " seconds ago"
        if second_diff < 120:
            return  "a minute ago"
        if second_diff < 3600:
            return str( second_diff / 60 ) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str( second_diff / 3600 ) + " hours ago"
    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        return str(day_diff) + " days ago"
    if day_diff < 31:
        return str(day_diff/7) + " weeks ago"
    if day_diff < 365:
        return str(day_diff/30) + " months ago"
    return str(day_diff/365) + " years ago"

def query_build(q,tag_list,option,order_by):
    query = "select description,href,host,tags,launch_count,mark,private,shared,toread from pinboard "

    mark_phase = {
        2: "1",
        1: "mark=1",
        0: "mark=0"
        }[option['mark']]
    private_phase = {
        2: "1",
        1: "private=1",
        0: "private=0"
        }[option['private']]
    filter_phase = ' '+mark_phase+" and "+private_phase+' '

    if len(tag_list)==0:
        tag_phase = "1"
    else:
        tag_phase = "("+" and ".join(map(lambda x:"tags like '%%%s%%'"%x, tag_list))+")"
        
    qsi = q.strip().split(' ')

    query += "where "

    dphases = "(" + " and ".join(map(lambda x: "description like '%%%s%%'" % x, qsi)) + ")"
    ephases = "(" + " and ".join(map(lambda x: "extended like '%%%s%%'" % x, qsi)) + ")"
    tphases = "(" + " and ".join(map(lambda x: "tags like '%%%s%%'" % x, qsi)) + ")"

    return query+"("+" or ".join([dphases, ephases, tphases])+") and "+mark_phase+" and "+private_phase+" and "+tag_phase+order_by

def title_build(title):
    if len(title)<45:
        return title
    
    short_title=title_pattern.search(title)
    if short_title != None: return short_title.group(1)
    
    return title

def pbsearch_sql(c,option,q):
    if ':' in q:   # tag
        (tags,q) = q.split(':')
        tag_list = [t[1:] for t in tags.split(' ') if t.startswith('#')]
    else:
        tag_list = []

    order_by = " order by "+util.sort_option[util.sql_orderby(c)]
    query = query_build(q,tag_list,option,order_by);

    output = []
    for r in c.execute(query):
        tags = ' '.join(map(lambda x: '#'+x, (r["tags"].strip().split(' ')))) if r['tags'] else ""
        launch_count = ' +'+str(r["launch_count"]) if r["launch_count"] else ''
        icon = "icon-%d.png"%((r['mark']<<1)+r['private'])
        output.append({"title": title_build(r['description']),
                       "subtitle": r['host']+" "+tags+launch_count, # "uid": r['hash'],
                       "arg": r['href'],
                       "quicklookurl": r['href'],
                       "mods": {"cmd": {"subtitle": "[Copy] %s"%r['href']}},
                       "icon":{ "path": icon}
        })

    add_head_bottom(c,q,output,tag_list,option)

    print json.dumps({"items": output})

def sql_update_time(c):
    import datetime
    r = c.execute("select datetime(value,'localtime') from setting where name='update_time'").fetchone()
    if r == None: return datetime.datetime.strptime("1970-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
    else: return datetime.datetime.strptime(r[0],"%Y-%m-%d %H:%M:%S")

def add_head_bottom(c,q,output,tag_list,option):
    auth = util.authinfo(c)
    
    help_string = "!-all, @-private, *-mark, #-tag"
    sync_time = "Checked: %s    ::: "%pretty_date(sql_update_time(c))
    subtitle_string = "%s"%help_string
    if auth:
        subtitle_string=sync_time+subtitle_string
    help = {
        "valid": False,
        "subtitle": subtitle_string
    }
    icon = "bicon-%d.png"%((option['mark']*3)+(option['private']))
    head = {"title": "Links: %d items" % len(output),
            "subtitle": subtitle_string,
            "valid": False,
            "icon": {"path": icon}
    }
    
    if len(tag_list)==0:  # all
        head["autocomplete"]="_"
        head["mods"] = { "alt": help, "ctrl": help, "cmd": help, "shift": help }
    else:
        tag_str="".join(tag_list)
        head["mods"] = { "ctrl": { "valid": True, "subtitle": "Set [Mark] on #%s"%tag_str,
                                   "arg": "#%s_mark=1"%tag_str},
                         "shift": { "valid": True, "subtitle": "Unset [Mark] on #%s"%tag_str,
                                   "arg": "#%s_mark=0"%tag_str},
                         "alt": { "valid": True, "subtitle": "Set [Private] on #%s"%tag_str,
                                   "arg": "#%s_private=1"%tag_str},
                         "cmd": { "valid": True, "subtitle": "Unset [Private] on #%s"%tag_str,
                                   "arg": "#%s_private=0"%tag_str}
        }
        
    output.insert(0,head)
    
    # indicator = "filter status: mark-%s, priv-%s"%(util.filter_option[option['mark']],util.filter_option[option['private']])

    auth = util.authinfo(c)
    if auth:
        pinboard_url = q and 'https://pinboard.in/search/?query=%s&mine=Search+Mine'%q.replace(' ','+') or 'https://pinboard.in/'
        pinboard_title = q and 'Search \'%s\' in pinboard.in'%q or 'Goto Pinboard'
        output.append({"title": pinboard_title,
                       "subtitle": pinboard_url,
                       "arg": pinboard_url,
                       "valid": True,
                       "mods": {
                           "alt": {"valid":False, "subtitle":pinboard_url},
                           "ctrl": {"valid":False, "subtitle":pinboard_url},
                           "cmd": {"valid":False, "subtitle":pinboard_url},
                           "shift": {"valid":False, "subtitle":pinboard_url}
                       }
        })

def add_option_submenu(result,mods,name,value):
    if name=="mark" or name=="private":
        target = util.filter_option
    else:
        target = util.sort_option
        
    for (idx,val) in enumerate(target):
        if len(target[idx])>20: ac=target[idx][:20]+"..."
        else: ac = target[idx]
        
        result.append({"title": " -> %s"%val,
                       "valid": True,
                       "autocomplete":"_%s=%s"%(name,ac),
                       "arg": "_%s=%d"%(name,idx),
                       "icon":{ "path": ((idx==value) and "on.png") or "off.png"},
                       "mods": mods
        });
    
def process_option(c,q):
    result = []
    help_back_string = "enter to go Back"
    help_select_string = ""
    mods = {
        "ctrl": {"valid": False, "subtitle": ""},
        "alt": {"valid": False, "subtitle": ""},
        "cmd": {"valid": False, "subtitle": ""},
        "shift": {"valid": False, "subtitle": ""}
    }
    mark = util.filter_mark(c)
    private = util.filter_private(c)
    sort = util.sql_orderby(c)

    if q.startswith("_mark"):
        result.append({"title": "mark [filter] - "+util.filter_option[mark],
                       "subtitle": help_back_string,
                       "valid": False,
                       "autocomplete":"_",
                       "mods": mods
        })
        add_option_submenu(result,mods,"mark",mark)
    elif q.startswith("_private"):
        result.append({"title": "private [filter] - "+util.filter_option[private],
                       "subtitle": help_back_string,
                       "valid": False,
                       "autocomplete":"_",
                       "mods": mods
        })
        add_option_submenu(result,mods,"private",private)
    elif q.startswith("_sort"):
        result.append({"title": "sort - "+util.sort_option[sort],
                       "subtitle": help_back_string,
                       "valid": False,
                       "autocomplete":"_",
                       "mods": mods
        })
        add_option_submenu(result,mods,"sort",sort)
    elif q.startswith("_pbauth"):
        result.append({"title": "_pbauth username:token",
                       "subtitle": "Setup Pinboard authentication token",
                       "valid": False,
                       "mods": mods
        })
        if ' ' in q and ':' in q:
            result[0]['valid'] = True
            result[0]['arg'] = '_auth='+q.split(' ')[1]
            result[0]['subtitle'] = "Enter to set"
    else:
        result.append({"title": "Settings",
                       "subtitle": "enter to go Back",
                       "valid": False,
                       "autocomplete": "",
                       "mods": mods
                       })
                       
        result.append({"title": "mark [filter] - "+util.filter_option[mark],
                       "subtitle": help_select_string,
                       "valid": False,
                       "autocomplete":"_mark",
                       "mods": mods
        })
        result.append({"title": "private [filter] - "+util.filter_option[private],
                       "subtitle": help_select_string,
                       "valid": False,
                       "autocomplete":"_private",
                       "mods": mods
        })
        result.append({"title": "sort - "+util.sort_option[sort],
                       "subtitle": help_select_string,
                       "valid": False,
                       "autocomplete":"_sort",
                       "mods": mods
        })
        auth = util.authinfo(c)
        if auth:
            result.append({"title": "> Pinboard User - %s"%auth.split(':')[0],
                           "subtitle": 'enter to change',
                           "valid": False,
                           "autocomplete":"_pbauth ",
                           "mods": mods
            })
            result.append({"title": ">> Download pinboard data",
                           "subtitle": 'enter to reload pinboard',
                           "valid": True,
                           "arg": "_pbreload",
                           "autocomplete":"_pbreload ",
                           "mods": mods
            })
        else:
            result.append({"title": ">> Login Pinboard account",
                           "subtitle": 'pbauth - username:token',
                           "valid": False,
                           "autocomplete":"_pbauth ",
                           "mods": mods
            })
            
    print json.dumps({"items": result})
    
def add_bookmark(c,q):
    result = []
    help = {"valid": False, "subtitle": ""}
    mods = { "alt": help, "ctrl":help, "cmd":help, "shift":help}
    
    last_q = q[1:].split(' ')[-1]
    prefix = '+'+' '.join(q[1:].split(' ')[:-1])

    tags = find_tags(c,last_q)

    for r in tags:
        expand_str = prefix+(prefix and " " or "")+r['tag']+' '
        result.append({"title": r['tag'],
                       "subtitle": "Count: %d"%r['count'],
                       "autocomplete":expand_str,
                       "valid": False,
                       "mods": mods})
    if last_q and last_q != ';' and not (last_q.lower() in [t['tag'].lower() for t in tags]):
        result.append({"title": last_q,
                       "subtitle": "NEW TAG",
                       "autocomplete":  prefix+(prefix and " " or "")+last_q+' ',
                       "valid": False,
                       "mods": mods})

    url = "Add frontmost browser's url to bookmark"
    result.append({"title": url, 
                   "subtitle": "Syntax: + tag tag ...",
                   "valid": True,
                   "arg": q,
                   "icon":{ "path": "help.jpg"},
                   "mods": mods})
        
    print json.dumps({"items": result})

def find_tags(c,q):    
    output = []
    
    sql = 'select tag, count from tags'
    order_by = " order by accessed desc, count desc, tag asc"

    tag_like = '%%'+'%%'.join(list(q))+'%%'
    if q: sql+= ' where tag like "%s"'%tag_like
    sql+=order_by

    for r in c.execute(sql):
        output.append({'tag':r['tag'],'count':r['count']})
        
    return output

def pbsearch_tag(c,prefix,q):
    output = []
    help = {"valid": False, "subtitle": ""}
    
    tags = find_tags(c,q)
    for r in tags:
        expand_str = prefix+(prefix and " " or "")+"#"+r['tag']+" : "        
        output.append({"title": r['tag']+" ("+str(r['count'])+")", "autocomplete":expand_str, "valid": False,
                       "mods": { "alt": help, "ctrl":help, "cmd":help, "shift":help}})

    if len(tags)==0:
        output.append({"title": "no tags",
                       "valid": False,
                       "mods": { "alt": help, "ctrl":help, "cmd":help, "shift":help}});
    print json.dumps({"items": output})


def get_option(c,q):
    option = {
        "mark": util.filter_mark(c),
        "private": util.filter_private(c)
        }

    if '!' in q:   # all option
        q = q.replace('!', '')
        option['mark']=2
        option['private']=2
    elif '@' in q:   # private only option
        q = q.replace('@', '')
        option['private']=1
    elif '*' in q:   # mark only option
        q = q.replace('*', '')
        option['mark']=1

    return (q,option)

def main():
    # arg parsing
    category = sys.argv[1]
    
    try: q = unicodedata.normalize('NFC',  unicode(sys.argv[2].strip()))
    except: q = ""

    conn = util.opendb()
    c = conn.cursor()

    util.create_schema(c)
    auth = util.authinfo(c)
    
    (q,option) = get_option(c,q)
    last_q = q.split(' ')[-1]
    if q.startswith('_'):   # option
        process_option(c,q)
    elif q.startswith('+'): # add bookmark
        add_bookmark(c,q)
    elif last_q.startswith('#') and (':' not in q): # tag expansion
        pbsearch_tag(c,'',last_q[1:])
    else:
        pbsearch_sql(c,option,q)
    
    util.closedb(conn)

if __name__ == '__main__':
    statsd = StatsClient(host='g.jmjeong.com',
                         port=8125,
                         prefix='jmjeong.alfred.bookmark')
    
    with statsd.timer('main'):
        statsd.incr('launch');
        main()
