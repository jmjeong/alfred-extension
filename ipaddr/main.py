#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# jmjeong, 2013/3/25

import urllib
from alfred import write, xml, Item, uid

IPHOST = 'http://icanhazip.com'
ipaddress = urllib.urlopen(IPHOST).read().strip()

write(xml([Item(title=ipaddress,
                subtitle=u'external ip',
                attributes={'arg':ipaddress, 'uid':uid(0)},
                icon='icon.png')]))
