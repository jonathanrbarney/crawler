# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3 as sqlite
import requests

connection = sqlite.connect('./wpdomains.db')
cursor = connection.cursor()

q = cursor.execute("select * from domains where wpcheck=?", (2,))

for ln in q:
    domain = ln[1]
    print(domain)
    try:
        r = requests.get('http://'+domain+'/license.txt')
    except:
        pass
    found = r.content.find(b'WordPress')+1
    try:
        r = requests.get('https://'+domain+'/license.txt')
    except:
        pass
    found+=r.content.find(b'WordPress')+1
    print(found)
    if found > 0:
        cursor.execute(
                "replace into domains (domain, wpcheck) values (?, ?)",
                    (domain, 1))
    else:
        cursor.execute(
                "replace into domains (domain, wpcheck) values (?, ?)",
                    (domain, 0))

    connection.commit()
