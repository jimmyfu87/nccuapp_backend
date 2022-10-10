from passlib.hash import bcrypt 
import redis
import logging
from sqlalchemy import create_engine

# MySQL
root_url = "http://127.0.0.1:8000/"
db_host = 'host.docker.internal'
# db_host = 'localhost'
db_username = 'root'
db_password = 'example'
db_port = '3306'
db_name = 'nccuapp'
db_url = "mysql+pymysql://{username}:{password}@{host}:{port}/{db_name}".format(username=db_username, password=db_password,
                                                                                host=db_host, port=db_port, db_name=db_name)
engine = create_engine(db_url)   


# Redis
redis_url = "host.docker.internal"
# redis_url = "localhost"
redis_port = 6379
pool = redis.ConnectionPool(host=redis_url, port=redis_port, decode_responses=True)
redis = redis.Redis(connection_pool=pool) 

hash_func = bcrypt.using(rounds=10, salt='ncc.ap.ncc/app4cc3/pp.')

def get_logger(name):
    logging.basicConfig(format='%(asctime)s [%(levelname)s]'
                        + '%(name)s:%(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=logging.INFO)
    logger = logging.getLogger(name)
    return logger




