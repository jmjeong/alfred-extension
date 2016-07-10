#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# util, v1.0
#
# Jaemok Jeong, 2016/06/09

import sqlite3
import os

PINBOARD_SQLITE3 = "~/Dropbox/bin/pinboard.db"

filter_option=["off","on","all"]

sort_option=[
    "accessed desc, launch_count desc, time desc",
    "launch_count desc, accessed desc, time desc",
    "time desc, accessed desc"
]

CREATE_PINBOARD_TABLE = """
create table if not exists pinboard (
  href varchar(255) primary key not null,
  host varchar,
  description varchar,
  extended varchar,
  time datetime,
  tags varchar,
  shared integer not null default 0,
  toread integer not null default 0,
    
  launch_count integer not null default 0,
  accessed datetime,
    
  private integer not null default 0,
  mark integer not null default 0,

  updated datetime
)
"""

CREATE_TAGS_TABLE = """
create table if not exists tags (
  tag varchar primary key not null,
  count integer not null,
  accessed datetime,
  updated datetime);
"""

CREATE_SETTING_TABLE = """
create table if not exists setting (
  name varchar primary key not null,
  value varchar,
  updated datetime);
"""

def create_schema(c):
    c.execute(CREATE_PINBOARD_TABLE)
    c.execute(CREATE_TAGS_TABLE)
    c.execute(CREATE_SETTING_TABLE)

def sql_update_time(c):
    r = c.execute("select value from setting where name='update_time'").fetchone()
    if r == None: return "1970-01-01 00:00:00"
    else: return r['value']

def update_sql_update_time_to_now(c,now):
    c.execute("insert or replace into setting(name,value,updated) values('update_time',?,?)",(now,now,))

def filter_mark(c):
    r = c.execute('select value from setting where name="mark"').fetchone()
    if r==None: return 2
    else: return int(r['value'])

def filter_private(c):
    r = c.execute('select value from setting where name="private"').fetchone()
    if r==None: return 2
    else: return int(r['value'])

def sql_orderby(c):
    r = c.execute('select value from setting where name="sort"').fetchone()
    if r==None: return 0
    else: return int(r['value'])

def authinfo(c):
    r = c.execute('select value from setting where name="auth"').fetchone()
    if r==None: return ''
    else: return r['value']
    
def opendb():
    conn = sqlite3.connect(os.path.expanduser(PINBOARD_SQLITE3))
    conn.row_factory = sqlite3.Row

    return conn

def closedb(conn):
    conn.commit()
    conn.close()

