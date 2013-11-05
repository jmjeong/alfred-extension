#!/usr/bin/env python
# -*- coding: utf-8 -*-

import alfred

commands = ( ('Hide Hidden Files', 'defaults write com.apple.finder AppleShowAllFiles FALSE; killall Finder'),
             ('Show Hidden Files', 'defaults write com.apple.finder AppleShowAllFiles TRUE; killall Finder'),
             ('Download pdf file in Safari', 'defaults write com.apple.Safari WebKitOmitPDFSupport -bool YES'),
             ('View pdf file in Safari', 'defaults write com.apple.Safari WebKitOmitPDFSupport -bool NO'),
             ('Fix [open with] duplicate entries', '/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister -kill -r -domain local -domain system -domain user; killall Finder'),
             ('Clean up Duplicate AppleScript Dictionary', '/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister -kill -r -domain local -domain system -domain user'),
             ('Hide Desktop Icons', 'defaults write com.apple.finder CreateDesktop -bool false;killall Finder'),
             ('Show Desktop Icons', 'defaults write com.apple.finder CreateDesktop -bool true;killall Finder')

            )

results = [alfred.Item(title=t,subtitle=sub,attributes={'arg':sub},icon='icon.png') for (t, sub) in commands];

alfred.write(alfred.xml(results))
