#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2014 Jaemok Jeong(jmjeong@gmail.com)
#
# [2014/02/21]


import os
import json
import urllib,urllib2

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

try:
    config=json.loads(open('config.json').read())
    user=config['username']
    token=config['token']
except:
    print "Setup not complete\npbauth username:token"
    sys.exit(0)

try:
    deleted_url=json.loads(open('deleted-url.json').read())
except IOError:
    deleted_url=[]
    
try:
    url = 'https://api.pinboard.in/v1/posts/delete?format=json&auth_token=%s:%s&url=%s'%(user,token,urllib.quote(sys.argv[1]))
    data = urllib2.urlopen(url).read()
    ret = json.loads(data)
    if ret['result_code']=='done':
        print "Bookmark deleted"
        deleted_url.append(sys.argv[1])
        f = open('deleted-url.json','w+')
        json.dump(deleted_url,f)
        f.close()        
    else:
        print ret['result_coode']
except:
    print "Error"
