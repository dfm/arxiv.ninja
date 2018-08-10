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

header_text = """
<div style="text-align: center; font-family: 'Comic Sans MS'; font-size: 2em;
            padding: 20px; background-color: blue; color: yellow;">
    Note: this is arXiv<strong>.ninja</strong> not
    <a href="https://arxiv.org"
        style="color: yellow;">arXiv<strong>.org</strong></a>
    so the listings
    have been randomly reordered.
</div>
"""
header_div = html.fromstring(header_text)

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

    content = content.replace(
        "arXiv.org",
        "<span style=\"font-family: 'Comic Sans MS';\">arXiv.ninja</span>")
    content = content.replace("href=\"/", "href=\"https://arxiv.org/")
    tree = html.fromstring(content.encode("utf-8"))

    for head in tree.xpath("//head"):
        element = etree.Element("style")
        element.text = """.list-title {
    font-size: large;
    font-weight: bold;
    margin: .25em 0 0 0;
    line-height: 120%;
    font-family: "Comic Sans MS";
}"""
        head.insert(0, element)

    for body in tree.xpath("//body"):
        body.insert(0, header_div)

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
