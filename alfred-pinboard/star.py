#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2014 Jaemok Jeong(jmjeong@gmail.com)
#
# [2014/02/21]


import os
import json
import main
import alfred

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

starred_url = main.starred_url_data()

if sys.argv[1] in starred_url:
    starred_url.remove(sys.argv[1])
    print "Unmark %s" % sys.argv[1]
    
else:
    starred_url.append(sys.argv[1])
    print "Mark %s" % sys.argv[1]
    
with open(os.path.join(alfred.work(False),'starred-url.json'),'w+') as f:
    json.dump(starred_url,f)

