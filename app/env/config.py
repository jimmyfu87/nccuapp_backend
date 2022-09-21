from passlib.hash import bcrypt 
root_url = "http://127.0.0.1:8080/"
hash_func = bcrypt.using(rounds=10, salt='ncc.ap.ncc/app4cc3/pp1')