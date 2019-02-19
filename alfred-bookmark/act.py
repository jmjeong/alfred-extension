#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# jmjeong, 2014/02/19

import os
import json
import urlparse
import applescript
import sys
import util
import subprocess

reload(sys)
sys.setdefaultencoding('utf-8')

def update_history(arg,c):
    c.execute("update pinboard set launch_count=launch_count+1,accessed=datetime('now') where href=?",(arg,))

def delete_from_db(arg,c):
    c.execute("delete from pinboard where href=?",(arg,))
    relaunch("launch","")

def relaunch(cmd, title):
    launch_args = """
        set bundleID to(system attribute "alfred_workflow_bundleid")
        tell application "Alfred 3" to run trigger "%s" in workflow bundleID with argument "%s"
    """ % (cmd, title.replace('"', '\\"'))
    applescript.AppleScript(launch_args).run()


def write_to_clipboard(output):
    process = subprocess.Popen(
        'pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
    process.communicate(output.encode('utf-8'))
    
def copy_bookmark(params, c):
    url = params['url']
    update_history(url, c)
    write_to_clipboard(url)
    print url
    
def go(params, c, secret = False):
    url = params['url']
    update_history(url ,c)

    if secret:
        cmd = 'open -na "Google Chrome" --args --incognito "%s" > /dev/null' % url
    else:
        cmd = 'open "%s" > /dev/null' % url

    os.system(cmd)

def delete_bookmark(params, c):
    url = params['url']
    delete_from_db(url, c)

    title = params['title']
    print "Deleted : %s" % title


def edit_bookmark(params):
    url = params['url']
    title = params['title']

    util.set_variables(**{'alfred-bookmark-url':url, 'alfred-bookmark-title':title})
    relaunch("add", title)


def add_bookmark_to_db(c, url, title):
    INSERT_UPDATE_PINBOARD = """
        insert or replace into pinboard
        (href,host,description,time,
        shared,toread,
        launch_count,private,mark,
        accessed,updated)
        values
        (?,?,?,datetime('now'),
        0,0,
        (select launch_count from pinboard where href=?),
        (select private from pinboard where href=?),
        (select mark from pinboard where href=?),
        datetime('now'),datetime('now'))
    """

    c.execute(INSERT_UPDATE_PINBOARD,(url,urlparse.urlparse(url)[1],title,
                                      url,url,url))


def add_bookmark(params,c):
    url = params['url']
    title = params['title']
    
    add_bookmark_to_db(c, url, title)
    print "Updated: %s" % title
    relaunch("launch","")


def main(args):
    try:
        params = json.loads(args)
    except:
        print "Invalid Params error"
        sys.exit(0)

    conn = util.opendb()
    c = conn.cursor()
    util.create_schema(c)

    action = params['action']

    if action == 'add':
        add_bookmark(params, c)
    elif action == 'delete':
        delete_bookmark(params, c)
    elif action == 'copy':
        copy_bookmark(params, c)
    elif action == 'edit':
        edit_bookmark(params)
    elif action == 'secret-open':
        go(params, c, secret=True)
    else:
        go(params, c)

    util.closedb(conn)
    
if __name__ == '__main__':
    main(sys.argv[1])