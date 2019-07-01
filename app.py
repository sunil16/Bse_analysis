# -*- coding: utf-8 -*-
import cherrypy
import os
import json
from jinja2 import Environment, FileSystemLoader
from redis_setup.store_data_redis_db import BseDataStore
from redis_setup.get_redis_connection import get_redis
from bse.get_bse import BseBhav
env = Environment(loader=FileSystemLoader('templates'))

class Api(object):

    def __init__(self):
        self.redis_conn = get_redis()
        bse_obj = BseBhav()
        bse_obj.get_bhav_zip()
        bse_obj.local_file_store()
        store_obj = BseDataStore()
        store_obj.data_saved_into_redis()

    def get_pipeline(self):
        if self.redis_conn is not None:
            try:
                pipeline = self.redis_conn.pipeline()
                pipeline.multi()
                return pipeline
            except:
                print("Error in pipeline object creation")

    @cherrypy.expose
    def index(self):
        pipeline = self.get_pipeline()
        redis_keys = self.redis_conn.zrange("first10", 0, -1)
        for key in redis_keys: # getting all values from redis by keys
            pipeline.hgetall(key)
        result = pipeline.execute()
        i = 0
        for item in result: #inserting name filed into dict
            item.update( { "name":  redis_keys[i]})
            i = i + 1
        # print(result)
        tmpl = env.get_template('index.html')
        return tmpl.render(data=result)


    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def search(self):
        input_json = cherrypy.request.json
        name = input_json["name"]
        name = name.upper()
        redis_keys = self.redis_conn.keys(pattern='*' + name + '*')
        pipeline = self.get_pipeline()
        for key in redis_keys:
            pipeline.hgetall(key)
        result = pipeline.execute()

        i = 0
        for item in result: #inserting name filed into dict
            item.update( { "name":  redis_keys[i]})
            i = i + 1
        return json.dumps(result)

config = {
    'global': {
        'server.socket_host': '127.0.0.1',
        'server.socket_port': int(os.environ.get('PORT', 5000)),
    },
    '/assets': {
        'tools.staticdir.root': os.path.dirname(os.path.abspath(__file__)),
        'tools.staticdir.on': True,
        'tools.staticdir.dir': 'assets',
    }
}



if __name__ == '__main__':
    cherrypy.quickstart(Api(), '/', config=config)
