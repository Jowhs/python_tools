#!/usr/bin/env python

import requests
import re
import urlparse


target_url = "http://anyweb.com"
target_links = []


def extract_links(url):
    # global href_links
    response = requests.get(url)
    href_links = re.findall('(?:href=")(.*?)"', response.content)
    return href_links


def crawl(url):
    href_links = extract_links(url)
    for link in href_links:
        link = urlparse.urljoin(url, link)

        if "#" in link:
            link = link.split("#")[0]

        if target_url in link and link not in target_links:
            target_links.append(link)
            crawl(link)
            print(link)


crawl(target_url)
