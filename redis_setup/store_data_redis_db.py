import datetime
import os
import csv
from redis_setup.get_redis_connection import get_redis

class BseDataStore(object):

    def __init__(self):
        self.redis_db_obj = get_redis()

    def get_pipeline(self):
        if self.redis_db_obj is not None:
            try:
                pipeline = self.redis_db_obj.pipeline()
                pipeline.multi()
                pipeline.flushall()
                return pipeline
            except:
                print("Error in pipeline object creation")

    def data_saved_into_redis(self):
        # try:
        file_name = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%d%m%y")
        with open('./bhavlocalzip/' + 'EQ' + '280619' + '.CSV','r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            pipeline_obj = self.get_pipeline()
            temp_dict = dict()
            i = 0;
            for row in csv_reader:
                name = row['SC_NAME'].strip()
                temp_dict = {
                    'code': row['SC_CODE'],
                    'open': row['OPEN'],
                    'high': row['HIGH'],
                    'low': row['LOW'],
                    'close': row['CLOSE']
                }
                if i < 10:
                    pipeline_obj.zadd('first10',{name: i})
                i = i + 1
                pipeline_obj.hmset(name,temp_dict)

            pipeline_obj.save()
            pipeline_obj.execute()
        # except:
        #     print("Error in saving data in redis")
