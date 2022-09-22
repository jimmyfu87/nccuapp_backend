from http.client import HTTPException
from fastapi import APIRouter, Body, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from ..env.config import root_url
import requests 
import json
from fastapi.responses import HTMLResponse
from ..env.config import redis
from ..dao.product_dao import get_product_dao

router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse, tags=['product'])
def get_product_view(request: Request):
    if request.cookies:
        if 'sid' in list(request.cookies.keys()):
            session_id = request.cookies['sid']
            member_id = redis.get(session_id)
            if member_id:
                end_url = root_url + 'product/get_product'
                all_data = requests.post(end_url, json = {'member_id':member_id})
                all_data_array = json.loads(all_data.text)
                return templates.TemplateResponse("Product_List.html",{"request": request, "product_rows": all_data_array,
                                                                        "member_id": member_id})
            else:
                return JSONResponse(content={'message': "Cookie outdate, please login again!!"})
        else:
            return JSONResponse(content={'message': "No cookie!!"})
        
    else:
        return JSONResponse(content={'message': "No cookie!!"})
    
@router.post("/get_product", tags=['product'])   
def get_product(member_id: str = Body(..., embed=True)):
    data = get_product_dao(member_id)
    return data
