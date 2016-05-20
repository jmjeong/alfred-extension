#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# pinboard-download, v1.1
#
# Jaemok Jeong, 2014/05/08

import os
import urllib
import sys
import json
import time
import json

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

ALFRED_WORKDIR = "~/Library/Application Support/Alfred 3/Workflow Data/com.jmjeong.alfredv2.pinboard/"
PINBOARD_TOKEN='xxxx:xxxxxx'                                            # get it from https://pinboard.in/settings/password

def note_list_cache():
    try:
        filename = os.environ['HOME']+'/.bookmarks-note.json'
        return json.loads(open(filename, 'r').read())
    except:
        return {}

def note_list_server(token):
    try:
        url = 'https://api.pinboard.in/v1/notes/list?format=json&auth_token=%s'%token
        data = urllib.urlopen(url)
        return json.load(data)
    except IOError as e:
        print e
        sys.exit(0)

def update_content(notes_cache,id,hash,token):
    try:
        for n in notes_cache['notes']:
            if n['id']==id and n['hash']==hash and n['text']:
                print "    - Found: %s" % n['title']
                return n['text']
    except KeyError:
        pass
        
    try:
        time.sleep(3)
        url = 'https://api.pinboard.in/v1/notes/%s?format=json&auth_token=%s'%(id,token)
        data = urllib.urlopen(url)
        note = json.load(data)
        print "  - Update: %s" % note['title']
        return note['text']
    except:
        return ""


def load_pinboard_data(token):
    try:
        print "Sleep 3 seconds because of API limit"
        time.sleep(3)
        print "Loading links from pinboard.in"
        url = 'https://api.pinboard.in/v1/posts/all?format=json&auth_token=%s'%token
        data = urllib.urlopen(url).read()
        with open(os.environ['HOME']+'/.bookmarks.json', "w+") as f:
            f.write(data)
        print "Loading links completed"
    except IOError as e:
        print e
        sys.exit(0)

if __name__ == '__main__':
    try:
        config = json.loads(open(os.path.join(os.path.expanduser(ALFRED_WORKDIR), 'config.json')).read())
        pinboard_token = config['pinboard_username']+':'+config['pinboard_token']
    except:
        pinboard_token = PINBOARD_TOKEN
    
    print "Loading notes from pinboard.in"
    
    notes_server = note_list_server(pinboard_token)
    notes_cache = note_list_cache()
    
    for n in notes_server['notes']:
        text = update_content(notes_cache,n['id'],n['hash'],pinboard_token)
        n['text'] = text

    with open(os.environ['HOME']+'/.bookmarks-note.json', 'w+') as myFile:
        myFile.write(json.dumps(notes_server))

    print "Loading notes completed"

    load_pinboard_data(pinboard_token)
