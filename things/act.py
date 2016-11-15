#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# act.py, v1.0
#
# Jaemok Jeong, 2016/11/15

import re
import sys
import applescript
from datetime import date, timedelta

import util

reload(sys)
sys.setdefaultencoding('utf-8')

def main():
    q = sys.argv[1]
    (title, tag, day, note) = util.parse(q)

    if not title: return;

    script = """tell application "Things"
        set newToDo to make new to do    
        set name of newToDo to "%s"
    """ % (title)

    
    if note:
        script += '    set notes of newToDo to "%s"\n'%(note)
    if day:
        today = date.today()
        delta = day - today
        script += '    set due date of newToDo to (current date)+%d*days\n'% (delta.days)
    if tag:
        script += 'set tag names of newToDo to "%s"\n'%(tag)
    script += 'end tell'

    applescript.AppleScript(script).run()
    
if __name__ == '__main__':
    main()
