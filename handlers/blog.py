import json

def main():
    with open('/home/hunter/workspace/orkohunter.net/database/blog/feed.json', 'r') as f:
        data = json.loads(f.read())

    return data
