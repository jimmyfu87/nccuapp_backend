from ..env.db_connect import engine
from sqlalchemy.sql import text



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
   query = "SELECT * FROM User WHERE member_id= :member_id AND member_password= :member_password  "
   result = engine.execute(text(query), {"member_id": member_id, "member_password": member_password}).fetchall()
   return result