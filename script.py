#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function

import os
import sys
import random
import requests
from copy import deepcopy
from lxml import html, etree

if len(sys.argv) >= 2:
    paths = sys.argv[1:]
else:
    with open("paths.txt", "r") as f:
        paths = f.read().splitlines()

cache_path = "cache"
for path in paths:
    # Attempt to load from cache
    fn = cache_path + path
    os.makedirs(fn, exist_ok=True)
    fn = os.path.join(fn, "index.html")

    if not os.path.exists(fn):
        r = requests.get("https://arxiv.org{0}?show=500".format(path))
        with open(fn, "wb") as f:
            f.write(r.content)

    with open(fn, "rb") as f:
        content = f.read().decode("utf-8")

    content = content.replace("href=\"/", "href=\"http://arxiv.org/")
    tree = html.fromstring(content.encode("utf-8"))

    for block in tree.xpath('//div[@id="dlpage"]/dl'):
        entries = []
        for inner in block:
            if inner.tag == "dt":
                entries.append([deepcopy(inner), None])
            else:
                entries[-1][1] = deepcopy(inner)
            inner.drop_tree()

        random.shuffle(entries)

        for entry in entries:
            block.append(entry[0])
            block.append(entry[1])

    path = os.path.join("output", path[1:])
    os.makedirs(path, exist_ok=True)
    open(os.path.join(path, "index.html"), "wb").write(etree.tostring(tree))
