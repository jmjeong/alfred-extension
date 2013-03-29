#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Make distribution file for alfred extension
#
# Jaemok Jeong(jmjeong@gmail.com), [2013/03/29]

import alfred
import os
import plistlib
import zipfile
import re
import json
import shutil

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

ignore_patterns = [
    r".*([\/]|[\\])_.*",   #All files that start with an underscore
    r".*([\/]|[\\])#.*",   #Emacs temporary files
    r".*~$]",              #Emacs temporary files
    r".*pyc",              #Python compiled file
    r".*alfredworkflow",   #alfred workflow
    r"screenshot.png",     #extension screenshot
    ]

compiled_ignore_patterns = []

def get_title(info_file):
    try:
        plist = plistlib.readPlist('info.plist')
        title = plist['name'].replace(" ", "").replace("/","")
    except:
        title = "default-extension"
    return title

def should_ignore_path(path):
    for p in compiled_ignore_patterns:
        if p.match(path):
            return True
    return False

def do_archive(dirname, filename):
    files = [f for f in os.listdir(dirname)
             if os.path.isfile(os.path.join(dirname, f)) and not should_ignore_path(f)]
    with zipfile.ZipFile(filename, 'w') as z:
        for f in files:
            z.write(f)
    z.close()

def do_src_archive(dirname, targetdir):
    files = [f for f in os.listdir(dirname)
             if os.path.isfile(os.path.join(dirname, f)) and not should_ignore_path(f)]
    
    for f in files:
        shutil.copy(f, targetdir)

def main():
    title = get_title('info.plist')
    try:
        with open('export.json') as f:
            export_info = json.load(f, encoding="utf-8")
    except:
        print "no export_json file"
        sys.exit(1)

    try:
        workflow_export_dir = os.path.expanduser(export_info['workflow-export']['directory'])
        alfred._create(workflow_export_dir)
        will_workflow_export = export_info['workflow-export']['enable']

        source_export_dir = os.path.expanduser(export_info['source-export']['directory'])
        alfred._create(source_export_dir)
        will_source_export = export_info['source-export']['enable']
    except KeyError:
        print "invalid export_json file"
        sys.exit(1)
    except IOError:
        print "io error"
        sys.exit(1)
        
    def compile_ignore_pattern():
        for p in ignore_patterns:
            if type(p) in (str,unicode):
                compiled_ignore_patterns.append(re.compile(p,re.IGNORECASE))
            else:
                compiled_ignore_patterns.append(p)
                
    compile_ignore_pattern()

    try:
        if will_workflow_export:
            do_archive(".", os.path.join(workflow_export_dir, title+".alfredworkflow"))
        if will_source_export:
            do_src_archive(".", source_export_dir)
        print "Export successful"
    except:
        print "Export fail"
        
if __name__ == '__main__':
    main()
