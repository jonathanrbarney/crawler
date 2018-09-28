# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy import log
import sqlite3 as sqlite

# This pipeline takes the Item and stuffs it into scrapedata.db
class domainPipeline(object):
    def __init__(self):
        # Possible we should be doing this in spider_open instead, but okay
        self.connection = sqlite.connect('./wpdomains.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS domains ' \
                    '(id INTEGER PRIMARY KEY NOT NULL UNIQUE, domain VARCHAR(80) NOT NULL UNIQUE, wpcheck INTEGER) NOT NULL UNIQUE')

    # Check for duplicates and if not add table to db.
    def process_item(self, item, spider):

        domain = item['domain']
        if domain is not None:
            self.cursor.execute("select * from domains where domain=?", (domain,))
            result = self.cursor.fetchone()
            if result:
                log.msg("Domain already in database: %s" % item, level=log.DEBUG)
            else:
                self.cursor.execute(
                    "insert into domains (domain, wpcheck) values (?, ?)",
                        (domain, 2))

                self.connection.commit()

                log.msg(f'Domain Stored: {domain}', level=log.DEBUG)
        return item
