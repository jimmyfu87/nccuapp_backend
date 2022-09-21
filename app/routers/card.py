
from fastapi import APIRouter, Body
from sqlalchemy.sql import text
from ..env.db_connect import engine

router = APIRouter()


# 取得所有現有的卡片
@router.get("/all", tags=['card'])
def get_all_card():
    query = "SELECT id, cardtype_name FROM Card_type"
    response = engine.execute(text(query)).fetchall()
    if len(response)==0:
        return "NoValue"
    else:
        return response


# 取得特定使用者擁有的卡片
@router.post("/get_card", tags=['card'])
def get_card(member_id: str = Body(...,embed=True)):
    query = "SELECT id, cardtype_name FROM Card_type WHERE cardtype_name \
             IN(SELECT cardtype_name FROM Card_relationship WHERE member_id= :member_id)"
    response = engine.execute(text(query), {"member_id":member_id}).fetchall()
    if len(response) == 0:
        return "NoValue"
    else:
        return response

# 取得特定使用者沒有的卡片
@router.post("/get_other_card", tags=['card'])
def get_other_card(member_id: str = Body(...,embed=True)):
    query = "SELECT id, cardtype_name FROM Card_type WHERE cardtype_name \
             NOT IN(SELECT cardtype_name FROM Card_relationship WHERE member_id= :member_id)"
    response = engine.execute(text(query), {"member_id":member_id}).fetchall()
    if len(response) == 0:
        return "NoValue"
    else:
        return response

