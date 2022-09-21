from http.client import HTTPException
from fastapi import APIRouter, Body, Request
from fastapi.templating import Jinja2Templates
from ..env.config import root_url
import requests 
import json
from fastapi.responses import HTMLResponse
from ..env.config import redis
from ..dao.product_dao import get_product_dao
router = APIRouter()

templates = Jinja2Templates(directory="templates")

# 取得所有現有的卡片
@router.get("/", response_class=HTMLResponse, tags=['product'])
def get_product_view(request: Request):
    if request.cookies:
        session_id = request.cookies['sid']
        member_id = redis.get(session_id)
        print('session_id', session_id)
        print('member_id', member_id)
        if member_id:
            end_url = root_url + 'product/get_product'
            all_data = requests.post(end_url, json = {'member_id':member_id})
            all_data_array = json.loads(all_data.text)
            return templates.TemplateResponse("Product_List.html",{"request": request, "product_rows": all_data_array,
                                                                    "member_id": member_id})
        else:
            raise  HTTPException("Cookie outdate, please login again!!")


    else:
        raise  HTTPException("No cookie!!")
    
@router.post("/get_product", tags=['product'])   
def get_product(member_id: str = Body(..., embed=True)):
    data = get_product_dao(member_id)
    return data
