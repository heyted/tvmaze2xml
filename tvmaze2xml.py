#! /usr/bin/env python

import json, urllib2, re
from urllib2 import Request, urlopen, URLError
from datetime import datetime, timedelta

def removeNonAscii(s):
    s = s.replace("&", "and")
    return "".join([x if ord(x) < 128 else '_' for x in s])

req = Request('http://api.tvmaze.com/schedule')
try:
    print 'Visit www.tvmaze.com'
    print 'Opening TVmaze connection'
    response = urlopen(req)
except URLError as e:
    if hasattr(e, 'reason'):
        print 'Failed to reach TVmaze server'
        print 'Reason: ', e.reason
    elif hasattr(e, 'code'):
        print 'TVmaze server could not fulfill request'
        print 'Error code: ', e.code
else:
    print 'Downloading TVmaze schedule'
    schedule_json_wa = response.read()
    schedule_json = removeNonAscii(schedule_json_wa)
    schedule_dicts = json.loads(schedule_json)
    with open('xmltv.xml', 'w') as xml_file:
        xml_file.write('<?xml version="1.0" encoding="ISO-8859-1"?>'+'\n')
        xml_file.write('<!DOCTYPE tv SYSTEM "xmltv.dtd">'+'\n')
        xml_file.write('\n')
        xml_file.write('<tv source-info-name="TVmaze" generator-info-name="tvmaze2xml.py">'+'\n')
        for i in range(len(schedule_dicts)-1):
            name = schedule_dicts[i]['show']['name']
            time = schedule_dicts[i]['airstamp']
            runtime = schedule_dicts[i]['runtime']
            ch_id = str(schedule_dicts[i]['show']['network']['id'])
            description = re.sub('<[^<]+?>', '', schedule_dicts[i]['summary'])
            start = time[0:4]+time[5:7]+time[8:10]+time[11:13]+time[14:16]+time[17:19]+' '+time[19:22]+time[23:25]
            start_time = datetime.strptime(start[0:14], "%Y%m%d%H%M%S")
            stop_time = start_time + timedelta(minutes=runtime)
            stop = stop_time.strftime("%Y%m%d%H%M%S")+' '+time[19:22]+time[23:25]
            xml_file.write('  <programme start="'+start+'" stop="'+stop+'" channel="'+ch_id+'">'+'\n')
            xml_file.write('    <title lang="en">'+name+'</title>'+'\n')
            xml_file.write('    <desc lang="en">'+description+'</desc>'+'\n')
            xml_file.write('  </programme>'+'\n')
        xml_file.write('</tv>')

