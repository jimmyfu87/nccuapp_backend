from fastapi import APIRouter, Body, Request
from fastapi.templating import Jinja2Templates
from ..env.config import root_url
import requests 
import json
from fastapi.responses import HTMLResponse


from ..dao.product_dao import get_product_dao
router = APIRouter()

templates = Jinja2Templates(directory="templates")

# 取得所有現有的卡片
@router.get("/{member_id}", response_class=HTMLResponse, tags=['product'])
def get_product_view(request: Request, member_id: str):
    end_url = root_url + 'product/get_product'
    all_data = requests.post(end_url, json = {'member_id':member_id})
    all_data_array = json.loads(all_data.text)
    return templates.TemplateResponse("Product_List.html",{"request": request, "product_rows": all_data_array,
                                                           "member_id": member_id})
    
@router.post("/get_product", tags=['product'])   
def get_product(member_id: str = Body(..., embed=True)):
    data = get_product_dao(member_id)
    return data
