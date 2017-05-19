# -*- coding: utf-8 -*-

import codecs

def main():
    data = {}
    with codecs.open("database/mfdf/fortunes", "r", "utf-8") as f:
        data["fortunes"] = f.read()

    data["fortunes"] = data["fortunes"].replace("\n", "<br>")
    return data
