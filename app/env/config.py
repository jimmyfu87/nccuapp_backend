from passlib.hash import bcrypt 
import redis
import logging

root_url = "http://127.0.0.1:8000/"
redis_url = "localhost"
redis_port = 6379
hash_func = bcrypt.using(rounds=10, salt='ncc.ap.ncc/app4cc3/pp.')
pool = redis.ConnectionPool(host=redis_url, port=redis_port, decode_responses=True)
redis = redis.Redis(connection_pool=pool) 

def get_logger(name):
    logging.basicConfig(format='%(asctime)s [%(levelname)s]'
                        + '%(name)s:%(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=logging.INFO)
    logger = logging.getLogger(name)
    return logger