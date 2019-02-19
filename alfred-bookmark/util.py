#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# util, v1.0
#
# Jaemok Jeong, 2018

import sqlite3
import applescript
import os
import json
import urllib

CREATE_PINBOARD_TABLE = """
create table if not exists pinboard (
  href varchar(255) primary key not null,
  host varchar,
  description varchar,
  time datetime,
  shared integer not null default 0,
  toread integer not null default 0,
    
  launch_count integer not null default 0,
  accessed datetime,
    
  private integer not null default 0,
  mark integer not null default 0,

  updated datetime
)
"""


def create_schema(c):
    c.execute(CREATE_PINBOARD_TABLE)

def get_dbpath():
    try:
        workflow_dir = os.environ["alfred_workflow_data"]
    except KeyError:
        workflow_dir = "~/Library/Application Support/Alfred 3/Workflow Data/com.jmjeong.alfred-bookmark"

    try:
        filename = os.path.expanduser(os.path.join(workflow_dir,'config.json'))
        config = json.loads(open(filename, 'r').read())
        return os.path.expanduser(config["DBPATH"])
    except:
        return os.path.expanduser(workflow_dir)
    
def opendb():
    dbpath = get_dbpath()
    pinboard_db_name = "pinboard.db"

    try:
        os.makedirs(dbpath)
    except:
        pass

    dbname = os.path.join(dbpath,pinboard_db_name)
    conn = sqlite3.connect(os.path.expanduser(dbname))
    conn.row_factory = sqlite3.Row

    return conn

def closedb(conn):
    conn.commit()
    conn.close()

def get_browser_url_info():
    script="""
        tell application "System Events" to set frontApp to name of first process whose frontmost is true

        if (frontApp = "Safari") or (frontApp = "Webkit") then
          using terms from application "Safari"
            tell application frontApp to set currentTabUrl to URL of front document
            tell application frontApp to set currentTabTitle to name of front document
          end using terms from
        else if (frontApp = "Google Chrome") or (frontApp = "Google Chrome Canary") or (frontApp = "Chromium") then
          using terms from application "Google Chrome"
            tell application frontApp to set currentTabUrl to URL of active tab of front window
            tell application frontApp to set currentTabTitle to title of active tab of front window
          end using terms from
        else
          return {"error","You need a supported browser as your frontmost app"}
        end if

        return {currentTabUrl, currentTabTitle}
    """
    return applescript.AppleScript(script).run()


def act_param(action, title, url):
    return json.dumps({'action': action, 'title': title, 'url': url})


def set_variables(**kwargs):
    launch_args = """
        set bundleID to(system attribute "alfred_workflow_bundleid")
        tell application "Alfred 3"
    """
    for key, value in kwargs.items():
        launch_args += """set configuration "%s" to value "%s" in workflow bundleID\n""" % (key, urllib.quote(str(value)))
    launch_args += "end tell"

    applescript.AppleScript(launch_args).run()