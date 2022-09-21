
from fastapi import APIRouter, Body
from sqlalchemy.sql import text
from pydantic import BaseModel
import json
from ..env.db_connect import engine

router = APIRouter()

class Card_relation(BaseModel):
    member_id: str
    cardtype_name: str


@router.post("/add", tags=["card_relation"])
def add_card_relation(card_relation: Card_relation):
    check_query = "SELECT * FROM Card_relationship WHERE member_id=:member_id \
                   AND cardtype_name= :cardtype_name"
    check_response = engine.execute(text(check_query), {"member_id":card_relation.member_id, "cardtype_name":card_relation.cardtype_name}).fetchall()
    if len(check_response) == 1:
        response = json.dumps({"success": False})
        return response
        
    elif len(check_response) == 0:
        insert_query = "INSERT INTO Card_relationship \
            (member_id, cardtype_name) VALUES (:member_id, :cardtype_name) "
        engine.execute(text(insert_query), {"member_id":card_relation.member_id, "cardtype_name":card_relation.cardtype_name})
        response = json.dumps({"success": True})
        return response

    else:
        response = json.dumps({"Error": "More than one relationship"})
        return response



@router.post("/delete", tags=["card_relation"])
def delete_card_relation(id: str = Body(...,embed=True)):
    query = "DELETE FROM Card_relationship WHERE id=:id"
    engine.execute(text(query), {"id":id})
    response = json.dumps({"success": True})
    return response



