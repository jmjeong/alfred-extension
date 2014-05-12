#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2014 Jaemok Jeong(jmjeong@gmail.com)
#
# [2014/02/21]


import os
import json
import urllib
import main
import alfred
import time

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def note_list_cache():
    try:
        filename = os.environ['HOME']+'/.bookmarks-note.json'
        return json.loads(open(filename, 'r').read())
    except:
        return {}

def note_list_server(user,token):
    try:
        time.sleep(3)
        url = 'https://api.pinboard.in/v1/notes/list?format=json&auth_token=%s:%s'%(user,token)
        data = urllib.urlopen(url)
        return json.load(data)
    except IOError:
        return {}

def update_content(notes_cache,id,hash):
    try:
        for n in notes_cache['notes']:
            if n['id']==id and n['hash']==hash:
                return n['text']
    except KeyError:
        return ""
        
if __name__ == '__main__':
    config = main.config_data()
    try:
        user=config['pinboard_username']
        token=config['pinboard_token']
    except:
        print "Setup not complete\npbauth username:token"
        exit(0)

    try:
        url = 'https://api.pinboard.in/v1/posts/all?format=json&auth_token=%s:%s'%(user,token)
        data = urllib.urlopen(url).read()
        filename = os.environ['HOME']+'/.bookmarks.json'
        f = open(filename,'w')
        f.write(data)
        f.close()
        try:
            os.remove(os.path.join(alfred.work(False),'deleted-url.json'))
        except OSError:
            pass
    except:
        print "Error in loading links"

    notes_server = note_list_server(user,token)
    notes_cache = note_list_cache()
    
    for n in notes_server['notes']:
        text = update_content(notes_cache,n['id'],n['hash'])
        if text:
            n['text'] = text

    with open(os.environ['HOME']+'/.bookmarks-note.json', 'w+') as myFile:
        myFile.write(json.dumps(notes_server))

    print "Reload completed"
