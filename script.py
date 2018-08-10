#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function

import os
import random
import requests
from copy import deepcopy
from lxml import html, etree

path = "list/astro-ph/new"

content = requests.get("https://arxiv.org/{0}".format(path)).text
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

path = os.path.join("output", path)
os.makedirs(path, exist_ok=True)
open(os.path.join(path, "index.html"), "wb").write(etree.tostring(tree))
