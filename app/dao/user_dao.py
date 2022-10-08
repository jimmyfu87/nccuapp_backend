from ..env.db_connect import engine
from sqlalchemy.sql import text
from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    member_id: str
    member_password: str
    member_email: Optional[str]

def check_user_exist_dao(member_id: str):
   query = "SELECT * FROM User WHERE member_id=:member_id "
   result = engine.execute(text(query), {"member_id": member_id}).fetchall()
   return result

def create_user_dao(member_id: str, member_password: str, member_email: str):
   query = "INSERT INTO User \
            (member_id, member_password, member_email) VALUES (:member_id, :member_password, :member_email) "
   engine.execute(text(query), {"member_id": member_id, "member_password": member_password, "member_email": member_email})
   return 

def login_dao(member_id: str, member_password: str):
   query = "SELECT * FROM User WHERE member_id= :member_id AND member_password= :member_password"
   result = engine.execute(text(query), {"member_id": member_id, "member_password": member_password}).fetchall()
   return result

def reset_password_dao(member_id: str, member_new_password: str):
   query = "UPDATE User SET member_password=:member_new_password WHERE member_id=:member_id"
   try:
      result = engine.execute(text(query), {"member_new_password": member_new_password, "member_id": member_id})
      if result.rowcount == 1:
         return {"success": True, "message": "Reset password successfully!"} 
      else:
         return {"success": False,"message": "Reset password unsuccessfully!"} 
    
   except Exception as e:
      return {"success": False, "message": e} 
