# -*- coding: utf-8 -*-
#
# Jaemok Jeong, 2013

import itertools
import re
import urllib
import os
import alfred

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

url = 'http://cartoon.media.daum.net/webtoon/view/miseng'
urlRetrieveRe = re.compile(r"data1.push.*img : \"(.*?)\", title:\"(.*?)\",.*url:\"(.*?)\"")
                              
ICON = True
MAX_RESULT = 9

results = []

data = urllib.urlopen(url).read()
searchPos = 0

for i in xrange(MAX_RESULT):
    g = urlRetrieveRe.search(data,searchPos)
    imageUrl = g.group(1)
    title = g.group(2)
    suburl = g.group(3)
    searchPos = g.end()

    filepath = os.path.join(alfred.work(True), os.path.split(imageUrl)[1])
    if not os.path.exists(filepath):
        urllib.urlretrieve(imageUrl, filepath)

    results.append(alfred.Item(title=u"미생 :" + title,
                               subtitle = u"다음 만화속 세상",
                               attributes={'arg':url+suburl},
                               icon = filepath))
alfred.write(alfred.xml(results))
