from sqlalchemy import create_engine

username = 'root'
password = 'example'
host = 'localhost'
port = '3306'
db_name = 'nccuapp'
db_url = "mysql+pymysql://{username}:{password}@{host}:{port}/{db_name}".format(username=username, password=password,
                                                                                host=host, port=port, db_name=db_name)
engine = create_engine(db_url)   
# conn = engine.connect()                                                         