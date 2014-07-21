#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# jmjeong, 2014/02/19

import alfred
import os
import rss_reload

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def main(arg):
    if arg=='reload':
        rss_reload.reload()
    else:
        os.system("open '%s' > /dev/null" % arg)
    
if __name__ == '__main__':
    main('reload')
    # main(sys.argv[1])
