#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2014 Jaemok Jeong(jmjeong@gmail.com)
#
# [2014/02/21]


import os
import json
import urllib,urllib2
import main
import alfred

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

config = main.config_data()

try:
    user=config['pinboard_username']
    token=config['pinboard_token']
except:
    print "Setup not complete\npbauth username:token"
    sys.exit(0)

try:
    deleted_url=json.loads(open(os.path.join(alfred.work(False),'deleted-url.json')).read())
except IOError:
    deleted_url=[]
    
try:
    url = 'https://api.pinboard.in/v1/posts/delete?format=json&auth_token=%s:%s&url=%s'%(user,token,urllib.quote(sys.argv[1]))
    data = urllib2.urlopen(url).read()
    ret = json.loads(data)
    if ret['result_code']=='done':
        print "Bookmark deleted"
        deleted_url.append(sys.argv[1])
        f = open(os.path.join(alfred.work(False),'deleted-url.json'),'w+')
        json.dump(deleted_url,f)
        f.close()        
    else:
        print ret['result_code']
except:
    print "Error"
