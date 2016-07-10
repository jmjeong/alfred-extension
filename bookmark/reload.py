#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# pinboard-reload, v1.0
#
# Jaemok Jeong, 2016/06/16

import os
import urllib
import sys
import json
import urlparse
import util
import datetime

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

INSERT_UPDATE_PINBOARD = """
insert or replace into pinboard(href,host,description,extended,time,tags,shared,toread,launch_count,accessed,private,mark,updated)
values
(?,?,?,?,?,?,?,?,
(select launch_count from pinboard where href=?),
(select accessed from pinboard where href=?),
(select private from pinboard where href=?),
(select mark from pinboard where href=?),
datetime('now'))
"""
    
def populate_data(c,pins,now):
    for p in pins:
        shared = 0 if p['shared']=='no' else 1
        toread = 0 if p['toread']=='no' else 1

        c.execute(INSERT_UPDATE_PINBOARD,
                  (p['href'],urlparse.urlparse(p['href'])[1],
                   p['description'],p['extended'],p['time'],p['tags'],shared,toread,
                   p['href'],p['href'],p['href'],p['href']))

    c.execute('delete from pinboard where updated < ?', (now,));
    
def populate_tags(c,tags,now):
    for t in tags:
        c.execute("insert or replace into tags(tag,count,updated) values (?,?,datetime('now'))",(t,tags[t]))

    c.execute('delete from tags where updated < ?', (now,));
    
def pinboard_update_time(token):
    url = 'https://api.pinboard.in/v1/posts/update?format=json&auth_token=%s'%token
    data = json.loads(urllib.urlopen(url).read())
    
    return data['update_time'].replace('T',' ').replace('Z','')

def update_sql_update_time_to_now(c):
    c.execute("insert or replace into setting(name,value,updated) values('update_time',datetime('now'),datetime('now'))")
    
def load_pinboard_data(token):
    try:
        # print "Loading links from pinboard.in"
        url = 'https://api.pinboard.in/v1/posts/all?format=json&auth_token=%s'%token
        data = urllib.urlopen(url).read()

        try:
            bookmark = json.loads(data)
        except:
            print data
            sys.exit(0)
        else:
            # print "Loading links completed"
            return bookmark
    except IOError as e:
        print e
        sys.exit(0)

def load_tags_data(token):
    try:
        # print "Loading tags information from pinboard.in"
        url = 'https://api.pinboard.in/v1/tags/get?format=json&auth_token=%s'%token
        data = urllib.urlopen(url).read()

        try:
            tags = json.loads(data)
        except:
            print data
            sys.exit(0)
        else:
            # print "Loading tags completed"
            return tags
    except IOError as e:
        print e
        sys.exit(0)

if __name__ == '__main__':

    conn = util.opendb()
    
    c = conn.cursor()
    util.create_schema(c)
    
    pinboard_token=util.authinfo(c)
    if not pinboard_token:
        print "Setup Pinboard authentication token"
        sys.exit(0)
    
    server_time = pinboard_update_time(pinboard_token)
    sql_time = util.sql_update_time(c)

    now = datetime.datetime.utcnow()
    
    if (sql_time < server_time):
        
        pins = load_pinboard_data(pinboard_token)
        populate_data(c,pins,now)
        
        tags = load_tags_data(pinboard_token)
        populate_tags(c,tags,now)

        print "Sync with pinboard done..."
    else:
        print "No new data found..."
        
    util.update_sql_update_time_to_now(c,now)
    
    util.closedb(conn)
