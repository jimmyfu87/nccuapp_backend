
from fastapi import APIRouter, Body
from sqlalchemy.sql import text
from sqlalchemy import create_engine
from pydantic import BaseModel

router = APIRouter()

username = 'root'
password = 'example'
host = 'localhost'
port = '3306'
db_name = 'nccuapp'
db_url = "mysql+pymysql://{username}:{password}@{host}:{port}/{db_name}".format(username=username, password=password,
                                                                                host=host, port=port, db_name=db_name)

engine = create_engine(db_url)
# conn = engine.connect()

## query paramter
@router.get("/query_parameter")
def get_user(member_id: str):
    query = "SELECT * FROM User WHERE member_id= :member_id "
    response = engine.execute(text(query), {"member_id":member_id}).fetchall()
    return response


## path paramter
@router.get("/path_parameter/{member_id}")
def get_user(member_id: str):
    query = "SELECT * FROM User WHERE member_id= :member_id "
    response = engine.execute(text(query), {"member_id":member_id}).fetchall()
    return response

## 多個參數用model塞法
class User(BaseModel):
    member_id: str
    member_password: str

@router.get("/body/model")
def get_user(user: User):
    query = "SELECT * FROM User WHERE member_id= :member_id and member_password= :member_password "
    response = engine.execute(text(query), {"member_id":user.member_id, "member_password":user.member_password}).fetchall()
    return response

## body內塞單個參數，需要定義embed=True，才會使API需要資料變成json格式
@router.get("/body/no_model")
def get_user(member_id: str = Body(...,embed=True)):
    query = "SELECT * FROM User WHERE member_id= :member_id"
    response = engine.execute(text(query), {"member_id":member_id}).fetchall()
    return response
