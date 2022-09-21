from passlib.hash import bcrypt 
import redis

root_url = "localhost:8080/"
redis_url = "localhost"
redis_port = 6379
hash_func = bcrypt.using(rounds=10, salt='ncc.ap.ncc/app4cc3/pp1')
pool = redis.ConnectionPool(host=redis_url, port=redis_port, decode_responses=True)
redis = redis.Redis(connection_pool=pool) 