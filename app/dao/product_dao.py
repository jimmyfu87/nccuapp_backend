from typing import Optional
from ..env.db_connect import engine
from sqlalchemy.sql import text
from pydantic import BaseModel


class Product(BaseModel):
    id: Optional[str]
    product_name: Optional[str]
    product_price: Optional[str]
    member_id: Optional[str]
    product_url: Optional[str]
    channel_name: Optional[str]


def get_member_product_dao(member_id: str):
    query = "SELECT id, product_name, product_price, product_url, channel_name FROM Product WHERE member_id=:member_id \
             ORDER BY upload_time DESC"
    result = engine.execute(text(query), {"member_id":member_id}).fetchall()
    return result


def delete_product_dao(id: str, member_id: str):
    query = "DELETE FROM Product WHERE id=:id"
    try:
        result = engine.execute(text(query), {"id": id, "member_id":member_id})
        if result.rowcount == 1:
            return {"success": True} 
        else:
            return {"success": False, "message": "No matching product"} 

    except Exception as e:
        return {"success": False, "message": e} 


def check_no_repeat_product_dao(product: Product):
    query = "SELECT * FROM Product WHERE product_name= :product_name AND product_price= :product_price AND \
             member_id=:member_id AND channel_name=:channel_name AND product_url=:product_url"
    result = engine.execute(text(query), {"product_name": product.product_name, "product_price": product.product_price, 
                                          "member_id": product.member_id, "channel_name": product.channel_name, 
                                          "product_url": product.product_url}).fetchall()
    if len(result)==0:
        return True
    else:
        return False



def add_product_topool_dao(product: Product):
    query = "INSERT INTO Product (product_name, product_price, product_url, member_id, channel_name, upload_time) \
             VALUES (:product_name, :product_price, :product_url, :member_id, :channel_name, DATE_ADD(NOW(),INTERVAL 8 HOUR))"
    try:
        result = engine.execute(text(query), {"product_name": product.product_name, "product_price": product.product_price, 
                                              "member_id":product.member_id, "product_url": product.product_url, 
                                              "channel_name": product.channel_name})
        if result.rowcount == 1:
            return {"success": True, "message": "Add product successfully!"} 
        else:
            return {"success": False,"message": "Add product unsuccessfully!"} 
    except Exception as e:
        return {"success": False, "message": e} 


def update_one_product_dao(product: Product, id: str):
    query = "UPDATE Product SET product_name=:product_name, product_price=:product_price, product_url=:product_url, \
             member_id=:member_id, channel_name=:channel_name, upload_time=DATE_ADD(NOW(),INTERVAL 8 HOUR) \
             WHERE id=:id"
    try:
        result = engine.execute(text(query), {"product_name": product.product_name, "product_price": product.product_price, 
                                              "member_id":product.member_id, "product_url": product.product_url, 
                                              "channel_name": product.channel_name, "id": id})
        if result.rowcount == 1:
            return {"success": True, "message": "Update product successfully!"} 
        else:
            return {"success": False,"message": "Update product unsuccessfully!"} 
    
    except Exception as e:
        return {"success": False, "message": e} 


def get_one_product_dao(member_id: str, id: str):
    query = "SELECT id, product_name, product_price, product_url, channel_name FROM Product WHERE member_id=:member_id \
             AND id=:id"
    result = engine.execute(text(query), {"member_id":member_id, "id": id}).fetchall()
    return result