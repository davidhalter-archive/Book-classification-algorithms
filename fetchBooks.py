#!/usr/bin/python
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import sys
import httplib
import re
from inc.models import *

def process_entry(match, cat_string):
    number = re.search('\d+', match)
    number = number.group(0)
    conn = httplib.HTTPConnection("www.gutenberg.org")
    conn.request("GET", 
                 '/cache/epub/' + number + '/pg' + number + '.txt')
    res = conn.getresponse()
    data = res.read()
    if res.status == 200:
        b = BookRaw(book_raw_id=number, category=cat_string, text_raw=data)
        from datetime import datetime
        b.save()
        print "saved " + str(number)
    else:
        print "not received " + str(number)
        print res.status, res.reason, len(data)
    return

start = int(sys.argv[1])
limit = int(sys.argv[2])

categories = {'fantasy': 46,
              'love': 2487,
              'children': 1415,
              'poetry': 13,
              'sf': 36,
              'detective': 1123,
              'adventure': 2849,
              'comedies': 776};
print "start: " + str(start) + "\nlimit: " + str(limit)

for cat_string, category in categories.iteritems():
    for counter in range(start, limit):
        print category, cat_string
        conn = httplib.HTTPConnection("www.gutenberg.org")
        conn.request("GET", 
                     '/ebooks/search.html/?default_prefix=subject_id&' \
                     + 'sort_order=downloads&query=' + str(category) \
                     + '&start_index=' + str(counter*25+1))
        res = conn.getresponse()

        data = res.read()

        if res.status == 200:
            m = re.findall('/ebooks/\d+', data)
            for match in m:
                process_entry(match, cat_string)
        else:
            print 'no category ' + str(category) + ' ' + cat_string
            print res.status, res.reason, len(data)
