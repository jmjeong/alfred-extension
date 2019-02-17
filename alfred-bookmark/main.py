#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# jmjeong, 2014/02/19

import os
import json
import unicodedata
import util
import urllib

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def query_build(q, order_by):
    query = "select description,href,host,launch_count,mark,private,shared,toread from pinboard"
        
    qsi = q.strip().split(' ')

    query += " where "

    dphases = "(" + " and ".join(map(lambda x: "description like '%%%s%%'" % x, qsi)) + ")"


    return query+ dphases + order_by


def title_build(data):
    LEN = 50
    return (data[:LEN] + '..') if len(data) > LEN else data


def pbsearch_sql(c, q):
    order_by = " order by accessed desc, launch_count desc, time desc"
    query = query_build(q, order_by);

    output = []
    for r in c.execute(query):

        launch_count = '+'+str(r["launch_count"])+' ' if r["launch_count"] else ''
        icon = "icon-0.png"
        output.append({"title": title_build(r['description']),
                       "subtitle": launch_count + r['href'], # "uid": r['hash'],
                       "arg": util.act_param('search', r['description'], r['href']),
                       "quicklookurl": r['href'],
                       "mods": {
                           "shift": {"subtitle": "[Secret] Open Bookmark in Chrome Incognito mode",
                                     "arg": util.act_param('secret-open', r['description'], r['href'])},
                           "ctrl": {"subtitle": "[Edit] Bookmark",
                                    "arg": util.act_param('edit', r['description'], r['href'])},
                           "cmd": {"subtitle": "[Copy] Bookmark",
                                   "arg": util.act_param('copy', r['description'], r['href'])},
                           "alt": {"subtitle": "[Delete] Bookmark",
                                   "arg": util.act_param('delete', r['description'], r['href'])}
                       },
                       "icon":{ "path": icon}
        })

    add_help("[Help]", "enter:Go, ctrl:Edit, cmd:Copy, alt:Delete, shift: Secret-Mode",  output)
    print json.dumps({"items": output})


def add_help(title, subtitle, result):
    result.append({"title": title,
                   "subtitle": subtitle,
                   "valid": False,
                   "icon": {"path": "help.jpg"}})


def add_bookmark(c, q):
    add_flag = os.getenv('add-bookmark')

    if add_flag == '1':
        (url, title) = util.get_browser_url_info()
        if url == "error":
            print title
            sys.exit(0)
    else:
        url = urllib.unquote(os.getenv('alfred-bookmark-url'))
        title = urllib.unquote(os.getenv('alfred-bookmark-title'))

    r = c.execute("select description from pinboard where href=?", (url,)).fetchone()

    result = []
    mods = {
        'ctrl': {},
        'shift': {}
    }
    if r:       # exists
        title = q or r['description'] or title
        mods['ctrl']['subtitle'] = 'Update Bookmark'
        mods['alt'] = {
            'subtitle': 'DELETE Bookmark',
            'arg': util.act_param('delete', title, url)
        }
    else:
        title = q or title
        mods['ctrl']['subtitle'] = 'Add Bookmark'

    mods['ctrl']['arg'] = util.act_param('add', title, url)

    shorten_title = '-'.join(title.split('-')[:-1]).strip()
    mods['shift']['arg'] = util.act_param('edit', shorten_title, url)
    mods['shift']['subtitle'] = shorten_title
    # mods['shift']['autocomplete'] = shorten_title

    result.append({"title": title,
                   "subtitle": url,
                   "autocomplete": title,
                   "valid": False,
                   "mods": mods
                   })
    if r:
        add_help('[Edit] Bookmark', "enter: Edit, ctrl: Update, alt: Delete", result)
    else:
        add_help('[New] Bookmark', "enter: Edit, ctrl: Add", result)

    print json.dumps({"items": result})


def main():
    category = sys.argv[1]
    
    try:
        q = unicodedata.normalize('NFC',  unicode(sys.argv[2].strip()))
    except:
        q = ""

    conn = util.opendb()
    c = conn.cursor()

    util.create_schema(c)

    if category == 'add':
        add_bookmark(c, q)
    else:
        pbsearch_sql(c, q)

    util.closedb(conn)

if __name__ == '__main__':
    main()
