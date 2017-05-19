# -*- coding: utf-8 -*-

def main():
    data = {}
    with open("database/mfdf/fortunes", "r") as f:
        data["fortunes"] = f.read()

    data["fortunes"] = data["fortunes"].replace("\n", "<br>")
    return data
