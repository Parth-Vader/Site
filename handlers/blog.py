# -*- coding: utf-8 -*-

import json

def main():
    with open('database/blog/feed.json', 'r') as f:
        data = json.loads(f.read())

    return data
