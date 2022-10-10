from asyncio.log import logger
from ..env.config import engine
from sqlalchemy.sql import text
from pydantic import BaseModel
from typing import Optional
from ..env.config import get_logger

logger = get_logger('user_dao')

class User(BaseModel):
    member_id: str
    member_password: str
    member_email: Optional[str]

def check_member_id_email_exist_dao(member_id: str, member_email: str):
   logger.info('check_member_id_email_exist_dao()')
   logger.info('member_id: {}'.format(member_id))
   logger.info('member_email: {}'.format(member_email))
   query = "SELECT * FROM User WHERE member_id=:member_id OR member_email=:member_email"
   try:
      result = engine.execute(text(query), {"member_id": member_id, "member_email": member_email}).mappings().all()
      return result
   except Exception as e:
      logger.error("Error occurs when check_user_exist_dao(), error message: {}".format(e))


def check_member_id_exist_dao(member_id: str):
   logger.info('check_member_id_exist_dao()')
   logger.info('member_id: {}'.format(member_id))
   query = "SELECT * FROM User WHERE member_id=:member_id "
   try:
      result = engine.execute(text(query), {"member_id": member_id}).mappings().all()
      return result
   except Exception as e:
      logger.error("Error occurs when check_member_id_exist_dao(), error message: {}".format(e))

def create_user_dao(member_id: str, member_password: str, member_email: str):
   logger.info('create_user_dao()')
   logger.info('member_id: {}'.format(member_id))
   logger.info('member_password: {}'.format(member_password))
   logger.info('member_email: {}'.format(member_email))
   query = "INSERT INTO User \
            (member_id, member_password, member_email) VALUES (:member_id, :member_password, :member_email) "
   try:
      result = engine.execute(text(query), {"member_id": member_id, "member_password": member_password, 
                                          "member_email": member_email})
      if result.rowcount == 1:
         return {"success": True, "message": "Register successfully!"} 
      else:
         return {"success": False,"message": "Register unsuccessfully!"} 
   except Exception as e:
      logger.error("Error occurs when create_user_dao(), error message: {}".format(e))
      return {"success": False,"message": "Register unsuccessfully!"} 


def login_dao(member_id: str, member_password: str):
   logger.info('login_dao()')
   logger.info('member_password: {}'.format(member_password))
   logger.info('member_id: {}'.format(member_id))
   query = "SELECT * FROM User WHERE member_id= :member_id AND member_password= :member_password"
   try:
      result = engine.execute(text(query), {"member_id": member_id, "member_password": member_password}).mappings().all()
      return result
   except Exception as e:
      logger.error("Error occurs when login_dao(), error message: {}".format(e))


def reset_password_dao(member_id: str, member_new_password: str):
   logger.info('reset_password_dao()')
   logger.info('member_id: {}'.format(member_id))
   logger.info('member_new_password: {}'.format(member_new_password))
   query = "UPDATE User SET member_password=:member_new_password WHERE member_id=:member_id"
   try:
      result = engine.execute(text(query), {"member_new_password": member_new_password, "member_id": member_id})
      if result.rowcount == 1:
         return {"success": True, "message": "Reset password successfully!"} 
      else:
         return {"success": False,"message": "Reset password unsuccessfully!"} 
    
   except Exception as e:
      logger.error("Error occurs when reset_password_dao, error message: {}".format(e))
      return {"success": False, "message": e} 

def get_member_id_byemail_dao(member_email: str):
   logger.info('get_member_id_byemail_dao()')
   logger.info('member_email: {}'.format(member_email))
   query = "SELECT member_id FROM User WHERE member_email=:member_email "
   try:
      result = engine.execute(text(query), {"member_email": member_email}).mappings().all()
      return result
   except Exception as e:
      logger.error("Error occurs when get_member_id_byemail_dao(), error message: {}".format(e))
