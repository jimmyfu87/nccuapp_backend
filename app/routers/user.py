
from http.client import HTTPException
from typing import Optional
from urllib import response
from fastapi import APIRouter, Body
from sqlalchemy.sql import text
from pydantic import BaseModel
import json
from ..env.db_connect import engine
from ..tool.authentication import get_hash_password
from ..dao.user_dao import create_user_dao, check_user_exist_dao, login_dao

router = APIRouter()

class User(BaseModel):
    member_id: str
    member_password: str
    member_email: Optional[str]


@router.post("/register", tags=["user"])
def register(user: User):  
    check_user_exist_response = check_user_exist_dao(user.member_id)
    if len(check_user_exist_response) == 0:
        hash_password = get_hash_password(user.member_password)
        create_user_dao(user.member_id, hash_password, user.member_email)
        response = json.dumps({"success": True})
        return response
    else:
        response = json.dumps({"success": False})
        raise HTTPException("This member_id has already been used, please change it!!")

@router.post("/login", tags=["user"])
def login(user: User):
    check_user_exist_response = check_user_exist_dao(user.member_id)
    if len(check_user_exist_response) == 1:
        hash_password = get_hash_password(user.member_password)
        login_response = login_dao(user.member_id, hash_password)
        if len(login_response) == 1:
            response = json.dumps({"success": True})
            return response
        else:
            raise HTTPException("Incorrect member_id or member_password!!")


    elif len(check_user_exist_response) == 0:
        raise HTTPException("{member_id} not existing member_id, please register it!!".format(member_id=user.member_id))






@router.post("/delete", tags=["card_relation"])
def delete_card_relation(id: str = Body(...,embed=True)):
    query = "DELETE FROM Card_relationship WHERE id=:id"
    engine.execute(text(query), {"id":id})
    response = json.dumps({"success": True})
    return response


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