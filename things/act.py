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

def getClipboardText():
    s = """
    tell application "System Events"    
      Set aText to the clipboard
      return aText
    end tell
    """

    return applescript.AppleScript(s).run()    

def main():
    q = sys.argv[1]
    (title, area, tag, day, note) = util.parse(q[1:])

    if not title: return;

    script = """tell application id "com.culturedcode.ThingsMac"
        activate
        set newToDo to make new to do   
        set name of newToDo to "%s"
    """ % title

    if q[0] == 'm' and not note:
        note = getClipboardText()
    
    if note:
        note = note.replace('"', '\\\"')
        note = note.replace('\n', '\\\n')
        script += '    set notes of newToDo to "%s"\n'%(note)
    if day:
        today = date.today()
        delta = day - today
        script += '    set due date of newToDo to (current date)+%d*days\n'% (delta.days)
    if tag:
        script += 'set tag names of newToDo to "%s"\n'%(tag)
    script += 'show newTodo\nmove newTodo to list id "%s"\nend tell' % area

    # print script
    applescript.AppleScript(script).run()
    
if __name__ == '__main__':
    main()
