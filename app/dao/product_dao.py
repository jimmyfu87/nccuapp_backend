from ..env.db_connect import engine
from sqlalchemy.sql import text



def get_product_dao(member_id: str):
    query = "SELECT product_name, product_price, product_url, channel_name FROM Product WHERE member_id=:member_id \
             ORDER BY upload_time DESC"
    result = engine.execute(text(query), {"member_id":member_id}).fetchall()
    return result