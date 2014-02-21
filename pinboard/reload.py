#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2014 Jaemok Jeong(jmjeong@gmail.com)
#
# [2014/02/21]

import os
import json
import urllib

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

try:
    config=json.loads(open('config.json').read())
    user=config['username']
    token=config['token']
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
    print "Reload completed"
except:
    print "Error occurred"
