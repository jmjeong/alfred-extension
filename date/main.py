#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# jmjeong, 2013/3/25

import alfred
import os
import datetime
from transdate import lunardate
from uuid import uuid4

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def process(query):
    query = query.strip()
    if query == "":
        mode = "mode_today"
        
        targetdate = lunardate.today()
    else:
        param = query.split(' ')
        if len(param) == 2 and param[1].lower() == 'leap':
            leap = True
        else:
            leap = False

        if '-' in param[0]:
            lunar = True
            mode = "mode_convert_lunar"
            
        else:
            lunar = False
            mode = "mode_convert_solar"

        date = param[0].replace('-', '')

        try:
            date = map(int, date.split('/'))
            if len(date) == 3:
                year = date[0]
                month = date[1]
                day = date[2]
            else:
                year = datetime.date.today().year
                month = date[0]
                day = date[1]

            if year < 100: year += 2000

            if lunar:
                targetdate = lunardate(year,month,day,leap)
            else:
                targetdate = lunardate.fromsolardate(datetime.date(year,month,day))

        except ValueError as error:
            mode = "mode_error"
            error_str = error
        
    results = [alfred.Item(title= u"입력 양식 : [-]y/m/d [leap]",
                           subtitle="ex) date, date 2013/4/1, date -2013/3/1, date -2013/3/2 leap",
                           attributes = {'uid':uuid4(),
                                         'valid':"no"},
                           icon=u"icon.png"
                           )]
    if mode == "mode_today" or mode == "mode_convert_solar":
        results.append(alfred.Item(title=targetdate.strftime('양력 %Y년 %m월 %d일 %a'), 
                                   subtitle=(mode=="mode_today") and u"오늘은..." or u"양력날짜는...",
                                   attributes = {'uid':uuid4(),
                                                 'valid':"no"},
                                   icon=u"solar.png"))
                                   
        isleap = targetdate.lunarleap and '(윤달)' or ''
        results.append(alfred.Item(title=targetdate.strftime('음력 %LY년 %Lm월 %Ld일') + isleap, 
                                   subtitle=u"음력날짜는...",
                                   attributes = {'uid':uuid4(),
                                                 'valid':"no"},
                                   icon=u"lunar.png"
                                   ))
    elif mode == "mode_convert_lunar":
        isleap = targetdate.lunarleap and '(윤달)' or ''
        results.append(alfred.Item(title=targetdate.strftime('음력 %LY년 %Lm월 %Ld일') + isleap, 
                                   subtitle=u"음력날짜는...",
                                   attributes = {'uid':uuid4(),
                                                 'valid':"no"},
                                   icon=u"lunar.png"
                                   ))
          
        results.append(alfred.Item(title=targetdate.strftime('양력 %Y년 %m월 %d일 %a'), 
                                   subtitle=u"양력날짜는...",
                                   attributes = {'uid':uuid4(),
                                                 'valid':"no"},
                                   icon=u"solar.png"))
    elif mode == "mode_error":
        results.append(alfred.Item(title=error_str,
                                   subtitle=u"오류 메시지",
                                   attributes = {'uid':uuid4(),
                                                 'valid':"no"},
                                   icon=u"icon.png"))
                                  
    print alfred.xml(results)
    
if __name__ == '__main__':
    try:
        query = alfred.args()[0]
    except IndexError:
        query = ""

    process(query)
