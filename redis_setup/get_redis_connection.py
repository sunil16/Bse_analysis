from redis import StrictRedis
import redis.exceptions
import os
import logging
logging.basicConfig(level=logging.INFO)
def get_redis():
    try:
        url = os.environ.get('REDIS_CONNECTION_URL','redis://localhost:6379/0')
        conn = StrictRedis.from_url(url,charset="utf-8", decode_responses=True)
        conn.ping()
    except redis.exceptions.ConnectionError:
        logging.fatal("Redis server is not running")
        raise
    return conn
