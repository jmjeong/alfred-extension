#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# jmjeong, 2014/02/19

import alfred
import os
import json
import unicodedata
import pocket
import time
import urlparse
import logging

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger('com.jmjeong.alfredv2.pinboard')
hdlr = logging.FileHandler('/var/tmp/alfred.pinboard.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.ERROR)


def update_history(arg):
    import main
    history = main.launch_history()
    now = int(time.time())
    if arg in history:
        history[arg][0] += 1
        history[arg][1] = now
    else:
        history[arg] = [1, now]
    with open(os.path.join(alfred.work(False),'launch-history.json'),'w+') as f:
        json.dump(history,f)

def copy(arg):
    print arg
    update_history(arg)
    
def go(arg):
    os.system("open '%s' > /dev/null" % arg)
    update_history(arg)

def star(arg):
    import main
    starred_url = main.starred_url_data()

    if arg in starred_url:
        starred_url.remove(arg)
        print "unmark %s" % urlparse.urljoin(arg,'/')
    else:
        starred_url.append(arg)
        print "mark %s" % urlparse.urljoin(arg,'/')
    
    with open(os.path.join(alfred.work(False),'starred-url.json'),'w+') as f:
        json.dump(starred_url,f)

def delete(arg):
    import urllib,urllib2
    import main

    config = main.config_data()
    try:
        user = config['pinboard_username']
        token = config['pinboard_token']
    except:
        print "Setup not complete\npbauth username:token"
        sys.exit(0)

    deleted_url = main.deleted_url_data()
    history = main.launch_history()
    try:
        url = 'https://api.pinboard.in/v1/posts/delete?format=json&auth_token=%s:%s&url=%s'%(user,token,urllib.quote(arg))
        data = urllib2.urlopen(url).read()
        ret = json.loads(data)
        if ret['result_code']=='done':
            print "%s deleted"%urlparse.urlparse(arg)[1]
            deleted_url.append(arg)
            with open(os.path.join(alfred.work(False),'deleted-url.json'),'w+') as f:
                json.dump(deleted_url,f)

            if arg in history:
                del history[arg]
                with open(os.path.join(alfred.work(False),'launch-history.json'),'w+') as f:
                    json.dump(history,f)
        else:
            print ret['result_code']
    except:
        print "Error"

def delete_history(arg):
    import main

    history = main.launch_history()
    if arg in history:
        del history[arg]
        with open(os.path.join(alfred.work(False),'launch-history.json'),'w+') as f:
            json.dump(history,f)

def addpocket(arg):
    import pocket
    pocket.addpocket(arg)

def pbreload():
    print "Reloading... Please wait."    
    launchArgs = 'tell application "Alfred 2" to run trigger "reload" in workflow "com.jmjeong.alfredv2.pinboard" with argument ""'
    os.system("osascript -e '%s' > /dev/null" % launchArgs)
    
def main(args):
    if args.startswith('goreload'):
        pbreload()
    elif args.startswith('go'):
        go(args[2:])
    elif args.startswith('copy'):
        copy(args[4:])
    elif args.startswith('star'):
        star(args[4:])
    elif args.startswith('deletehistory'):
        delete_history(args[13:])
    elif args.startswith('delete'):
        delete(args[6:])
    elif args.startswith('addpocket'):
        addpocket(args[9:])
    
if __name__ == '__main__':
    start = time.clock()
    main(sys.argv[1])
    end = time.clock()
    logger.info("Elapsed time : %.5gs"%(end-start))
