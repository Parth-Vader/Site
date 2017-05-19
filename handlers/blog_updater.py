#! /usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import json
import feedparser

months_map = {
    1: 'January',
    2: 'February',
    3: 'March',
    4: 'April',
    5: 'May',
    6: 'June',
    7: 'July',
    8: 'August',
    9: 'September',
    10: 'October',
    11: 'November',
    12: 'December',
}

feed_url = "https://medium.com/feed/@orkohunter/"
atom = feedparser.parse(feed_url)

with codecs.open('/home/hunter/orkohunter.net/database/blog/last_id', 'r', 'utf-8') as f:
    last_id = f.read().strip('\n')

new_post = atom['entries'][0]

with codecs.open('/home/hunter/orkohunter.net/database/blog/last_id', 'w', 'utf-8') as f:
    f.write(new_post['id'])

is_old_post = last_id == new_post['id']
is_not_a_reply = 'tags' in new_post  # Responses don't have tags

if not is_old_post and is_not_a_reply:
    print("I'm in")
    print(new_post['title'])
    last_id = new_post['id']

    with codecs.open('/home/hunter/orkohunter.net/database/blog/feed.json', 'r', 'utf-8') as f:
        feed = json.loads(f.read())

    new_post_dict = {}
    new_post_dict['title'] = new_post['title']
    new_post_dict['link'] = new_post['id']
    tags = []
    # If the post does not have tags
    try:
        for tag in new_post['tags']:
            tags.append(tag['term'])
    except:
        pass
    new_post_dict['tags'] = tags

    year = feed['feed'][0]
    if year['year'] == new_post['published_parsed'].tm_year:
        month = year['content'][0]
        if month['month'] == months_map[new_post['published_parsed'].tm_mon]:
            month['content'].insert(0, new_post_dict)
        else:
            new_month = {}
            new_month['month'] = months_map[new_post['published_parsed'].tm_mon]
            new_month['content'] = []
            new_month['content'].insert(0, new_post_dict)
            year['content'].insert(0, new_month)
    else:
        new_year = {}
        new_year['content'] = []
        new_month = {}
        new_month['month'] = months_map[new_post['published_parsed'].tm_mon]
        new_month['content'] = []
        new_month['content'].insert(0, new_post_dict)
        new_year['content'].insert(0, new_month)
        feed['feed'].insert(new_year)

    with codecs.open('/home/hunter/orkohunter.net/database/blog/feed.json', 'w', 'utf-8') as f:
        f.write(json.dumps(feed))
