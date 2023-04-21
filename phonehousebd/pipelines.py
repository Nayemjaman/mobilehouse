# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# 

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import psycopg2

class PhonehousebdPipeline:
    
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('POSTGRES_HOST'),
            database=crawler.settings.get('POSTGRES_DATABASE'),
            user=crawler.settings.get('POSTGRES_USER'),
            password=crawler.settings.get('POSTGRES_PASSWORD')
        )

    def open_spider(self, spider):
        self.connection = psycopg2.connect(
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.password
        )
        self.cursor = self.connection.cursor()

    def close_spider(self, spider):
        self.cursor.close()
        self.connection.close()

    def process_item(self, item, spider):
        keys = item.fields.keys()
        values = [item[keys] for key in keys]
        placeholders = ', '.join(['%s'] * len(keys))
        columns = ', '.join(keys)
        table = spider.settings.get('POSTGRES_TABLE')
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        self.cursor.execute(query, values)
        self.connection.commit()
        return item
