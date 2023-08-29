from passlib.hash import bcrypt 
import redis
import logging
from sqlalchemy import create_engine

# web_crawl_url
web_crawl_url = "https://7z0lvhbe47.execute-api.ap-northeast-1.amazonaws.com/default/web_crawl"

# MySQL
root_url = "http://127.0.0.1:8000/"
# db_host = 'host.docker.internal'
db_host = 'database.c67eqxezsx2s.ap-northeast-1.rds.amazonaws.com'
db_username = 'root'
db_password = 'nccuapp105306'
db_port = '3306'
db_name = 'nccuapp'
db_url = "mysql+pymysql://{username}:{password}@{host}:{port}/{db_name}".format(username=db_username, password=db_password,
                                                                                host=db_host, port=db_port, db_name=db_name)
engine = create_engine(db_url)   


# Redis
# redis_url = "host.docker.internal"
# redis_url = "nccuapp-001.vfvg8p.0001.apne1.cache.amazonaws.com"
redis_url = "localhost"
redis_port = 6379
pool = redis.ConnectionPool(host=redis_url, port=redis_port, decode_responses=True)
redis = redis.Redis(connection_pool=pool) 
login_time_sec = 180

hash_func = bcrypt.using(rounds=10, salt='ncc.ap.ncc/app4cc3/pp.')

def get_logger(name):
    logging.basicConfig(format='%(asctime)s [%(levelname)s]'
                        + '%(name)s:%(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=logging.INFO)
    logger = logging.getLogger(name)
    return logger




