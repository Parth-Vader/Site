# -*- coding: utf-8 -*-

import codecs
import json

def main():
    with codecs.open('database/blog/feed.json', 'r', 'utf-8') as f:
        data = json.loads(f.read())

    return data
