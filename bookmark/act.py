#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# jmjeong, 2014/02/19

import os
import json
import unicodedata
import urlparse
import sqlite3
import applescript
import urllib
import urllib2
import sys
import util

reload(sys)
sys.setdefaultencoding('utf-8')

def update_history(arg,c):
    c.execute("update pinboard set launch_count=launch_count+1,accessed=datetime('now') where href=?",(arg,))

def private(arg,c):
    c.execute("update pinboard set private=not private,accessed=datetime('now') where href=?",(arg,))
    relaunch("launch","")

def mark(arg,c):
    c.execute("update pinboard set mark=not mark,accessed=datetime('now') where href=?",(arg,))
    relaunch("launch","")

def delete_from_db(arg,c):
    r=c.execute("select tags from pinboard where href=?",(arg,)).fetchone()
    if r!=None and r['tags']:
        dec_or_delete_fromdb(c,r['tags'].split(','))
    c.execute("delete from pinboard where href=?",(arg,))
    relaunch("launch","")

def relaunch(cmd,arg):
    launchArgs = 'tell application "Alfred 3" to run trigger "%s" in workflow "com.jmjeong.bookmark" with argument "%s"'%(cmd,arg)
    applescript.AppleScript(launchArgs).run()

def update_sql_option(c,name,value):
    c.execute("insert or replace into setting(name,value,updated) values (?,?,datetime('now'))", (name,value,))

def delete_sql_auth(c):
    c.execute('delete from setting where name="auth"')
    
def update_option(arg,c):
    (name,value)=arg.split('=') # set

    if name!='auth':
        update_sql_option(c,name,value)
        relaunch("launch","_")
        return

    url = 'https://api.pinboard.in/v1/user/api_token/?auth_token=%s&format=json'%(value)
    try:
        data = urllib2.urlopen(url).read()
        ret = json.loads(data)
        if ret['result']:
            update_sql_option(c,name,value)
            print "Setup completed"
        else:
            delete_sql_auth(c)
            print "Invalid username:token"
    except:
        delete_sql_auth(c)
        print "Invalid username:token"
        
    relaunch("launch","_")
    
def change_tag_status(arg,c):
    (tag,set)=arg.split('_')
    (name,value)=set.split('=')

    sql = "update pinboard set %s=?,accessed=datetime('now')"%name
    where_phase=' where tags like "%%%s%%"'%(tag)

    c.execute(sql+where_phase,(value,))
    relaunch("launch","")
    
def copy(arg,c):
    update_history(arg,c)
    print arg
    
def go(arg,c):
    update_history(arg,c)
    os.system("open '%s' > /dev/null" % arg)

def delete(arg,c):
    delete_from_db(arg,c)
    
    auth = util.authinfo(c)
    if auth:
        url = 'https://api.pinboard.in/v1/posts/delete?format=json&auth_token=%s&url=%s'%(auth,urllib.quote(arg))
        data = urllib2.urlopen(url).read()
        ret = json.loads(data)
        if ret['result_code']=='done' or ret['result_code']=='item not found':
            print "%s deleted"%urlparse.urlparse(arg)[1]
        else:
            print ret['result_code']
    else:
        print "%s deleted"%urlparse.urlparse(arg)[1]

def get_browser_url_info():
    script="""
        tell application "System Events" to set frontApp to name of first process whose frontmost is true

        if (frontApp = "Safari") or (frontApp = "Webkit") then
          using terms from application "Safari"
            tell application frontApp to set currentTabUrl to URL of front document
            tell application frontApp to set currentTabTitle to name of front document
          end using terms from
        else if (frontApp = "Google Chrome") or (frontApp = "Google Chrome Canary") or (frontApp = "Chromium") then
          using terms from application "Google Chrome"
            tell application frontApp to set currentTabUrl to URL of active tab of front window
            tell application frontApp to set currentTabTitle to title of active tab of front window
          end using terms from
        else
          return {"error","You need a supported browser as your frontmost app"}
        end if

        return {currentTabUrl, currentTabTitle}
    """
    return applescript.AppleScript(script).run()

def inc_or_new_fromdb(c,tags):
    for t in tags:
        r = c.execute("select count from tags where tag=?", (t,)).fetchone()
        
        if r==None or r['count']==0:
            c.execute("insert into tags(tag,count,accessed,updated) values(?,1,datetime('now'),datetime('now'))",(t,))
        else:
            c.execute("update tags set count=count+1,accessed=datetime('now'),updated=datetime('now') where tag=?",(t,))

def dec_or_delete_fromdb(c,tags):
    for t in tags:
        r = c.execute("select count from tags where tag=?", (t,)).fetchone()
        if r==None or r['count']>1:
            c.execute("update tags set count=count-1,accessed=datetime('now'),updated=datetime('now') where tag=?", (t,))
        else:
            c.execute("delete from tags where tag=?", (t,))

def update_accessed_fromdb(c,tags):
    for t in tags:
        c.execute("update tags set accessed=datetime('now') where tag=?", (t,))

def add_bookmark_to_db(c,url,title,tag):
    INSERT_UPDATE_PINBOARD = """
        insert or replace into pinboard
        (href,host,description,time,
        shared,toread,tags,
        extended,launch_count,private,mark,
        accessed,updated)
        values
        (?,?,?,datetime('now'),
        0,0,?,
        (select extended from pinboard where href=?),
        (select launch_count from pinboard where href=?),
        (select private from pinboard where href=?),
        (select mark from pinboard where href=?),
        datetime('now'),datetime('now'))
    """
    
    new_tag = tag.split(' ')
    
    r = c.execute("select count(*) as count, tags from pinboard where href=?",(url,)).fetchone()
    c.execute(INSERT_UPDATE_PINBOARD,(url,urlparse.urlparse(url)[1],title,
                                      ",".join(tag.decode('utf-8').split(' ')),
                                      url,url,url,url))

    if r['count']==0:  # new
        inc_or_new_fromdb(c,new_tag)
    else:
        old_tag = r['tags'].split(',')
        deleted = list(set(old_tag)-set(new_tag))
        added = list(set(new_tag)-set(old_tag))

        inc_or_new_fromdb(c,added)
        dec_or_delete_fromdb(c,deleted)
        
        update_accessed_fromdb(c,set(new_tag).intersection(set(old_tag)))

def add_bookmark(args,c):
    (url,title)=get_browser_url_info();
    if url=="error":
        print title
        sys.exit(0)

    tag=args

    auth=util.authinfo(c)
    tag=tag.strip()
    
    add_bookmark_to_db(c,url,title,tag)
    
    if auth:
        qurl=urllib.quote(url.encode('utf-8'))
        qtitle=urllib.quote(title.encode('utf-8'))
        qtag=urllib.quote(tag.encode('utf-8'))

        encode_url='https://api.pinboard.in/v1/posts/add?format=json&auth_token=%s&url=%s&description=%s&tags=%s&shared=no'%(auth,qurl,qtitle,qtag)
        data = urllib2.urlopen(encode_url).read()
        ret = json.loads(data)
        if ret['result_code']=='done':
            print "Successfully added : %s"%title
        else:
            print ret['result_code']
    else:
            print "Successfully added : %s"%title
        
def process(cmd,args,c):
    if cmd=='enter':     # go
        go(args,c)
    elif cmd=='ctrl':    # mark(args,c)
        mark(args,c)
    elif cmd=='cmd':     # copy
        copy(args,c)
    elif cmd=='alt':     # delete
        delete(args,c)
    elif cmd=='shift':   # private
        private(args,c)
    
def main(cmd,args):
    #  ex) tag status change : #tag_mark=1
    #      option change     : _mark=1
    #      add url           : + tag tag ; desc

    conn = util.opendb()
    c = conn.cursor()
    util.create_schema(c)

    if args.startswith('#'):
        change_tag_status(args[1:],c)
    elif args.startswith('_pbreload'):
        relaunch("reload","");
    elif args.startswith('_'):
        update_option(args[1:], c)
    elif args.startswith('+'):
        add_bookmark(args[1:], c)
    else:
        process(cmd,args,c)

    util.closedb(conn)
    
if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
