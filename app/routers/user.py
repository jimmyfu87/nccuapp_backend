from http.client import HTTPException
from typing import Optional
import redis
from fastapi import APIRouter, Body, Request
from sqlalchemy.sql import text
from pydantic import BaseModel
import json
from ..env.db_connect import engine
from ..env.config import redis
from ..tool.authentication import get_hash_password
from ..dao.user_dao import create_user_dao, check_user_exist_dao, login_dao, User
from fastapi.responses import JSONResponse

router = APIRouter()


@router.post("/register", tags=["user"])
def register(user: User):  
    if user.member_id == "" or user.member_password == "" or user.member_email == "":
        return JSONResponse(content={"success": False, 'message': "Value cannot be blank, please fill in!!"})
    if " " in user.member_id or " " in user.member_password or " " in user.member_email:
        return JSONResponse(content={"success": False, 'message': "Value cannot contains blank, please fill in!!"})
    check_user_exist_response = check_user_exist_dao(user.member_id)
    if len(check_user_exist_response) == 0:
        hash_password = get_hash_password(user.member_password)
        create_user_dao(user.member_id, hash_password, user.member_email)
        return JSONResponse(content={"success": True, 'message': "Register successfully"})
    else:
        return JSONResponse(content={"success": False, 'message': "This member id or email has already been used, please change it!!"})

@router.post("/login", tags=["user"])
def login(user: User):
    check_user_exist_response = check_user_exist_dao(user.member_id)
    if len(check_user_exist_response) == 1:
        hash_password = get_hash_password(user.member_password)
        login_response = login_dao(user.member_id, hash_password)
        if len(login_response) == 1:
            hash_key = get_hash_password(user.member_id)
            redis.setex(hash_key, 1800, user.member_id)
            response = JSONResponse(content={"success": True})
            response.set_cookie(key="sid", value=hash_key)
            return response
        else:
            return JSONResponse(content={"success": False, 'message': "Incorrect member id or member password!!"})

    elif len(check_user_exist_response) == 0:
        return JSONResponse(content={"success": False, 'message': "{member_id} is not a valid member id, please register it!!".format(member_id=user.member_id)})


@router.get("/logout", tags=['user'])
def logout(request: Request):
    if redis.exists(request.cookies['sid']):
        redis.delete(request.cookies['sid'])
        return JSONResponse(content={"success": True, 'message': "Logout Successfully"})
    else:
        return JSONResponse(content={"success": False, 'message': "Already logout!!"})






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