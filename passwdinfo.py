#!/usr/bin/env python
# -*- coding: utf-8 -*-

import getpass
import hashlib
import urllib2
from BeautifulSoup import BeautifulSoup
import re

def askddg(hexdigest):
    url = 'http://duckduckgo.com/html/?q="' + hexdigest + '"'
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Gentle spider')]
    try:
        data = opener.open(url).read()
    except:
        return 2
    parsed = BeautifulSoup(data)
    topics = parsed.findAll('a', {'class': 'large'})
    try:
        test = topics[0]
    except:
        return 1
    return 0

def main():
    passwd = getpass.getpass()
    secure = 0
    message = "No hash found on the web"
    hashes = {}
    hashes['md5']    = hashlib.md5(passwd).hexdigest()
    hashes['sha1']   = hashlib.sha1(passwd).hexdigest()
    hashes['sha224'] = hashlib.sha224(passwd).hexdigest()
    hashes['sha256'] = hashlib.sha256(passwd).hexdigest()
    hashes['sha384'] = hashlib.sha384(passwd).hexdigest()
    hashes['sha512'] = hashlib.sha512(passwd).hexdigest()

    for alg in hashes:
        print alg + "\t: " + hashes[alg]
        search = askddg(hashes[alg])
        if search == 1:
            secure = 1
            message = "\n\033[0;31mPassword insecure\033[0m:"
            message = message + " At least one hash found on the web"
        elif search == 2 and secure == 1:
            secure = 2
            message = "\n\033[0;33mPassword may be insecure\033[0m:"
            message = message + " Error while loading search results"

    print message
    return secure

if __name__ == '__main__':
    main()
