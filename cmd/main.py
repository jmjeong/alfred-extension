#!/usr/bin/env python
# -*- coding: utf-8 -*-

import alfred

commands = ( ('Hide Hidden Files', 'defaults write com.apple.finder AppleShowAllFiles FALSE; killall Finder'),
             ('Show Hidden Files', 'defaults write com.apple.finder AppleShowAllFiles TRUE; killall Finder'),
             ('Fix [open with] duplicate entries', '/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister -kill -r -domain local -domain system -domain user; killall Finder'),
             ('Clean up Duplicate AppleScript Dictionary', '/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister -kill -r -domain local -domain system -domain user'),
            )

results = [alfred.Item(title=t,subtitle=sub,attributes={'arg':sub},icon='icon.png') for (t, sub) in commands];

alfred.write(alfred.xml(results))
