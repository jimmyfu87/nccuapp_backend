from fastapi import APIRouter, Body, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from ..env.config import root_url
import requests 
import json
from fastapi.responses import HTMLResponse
from ..env.config import redis
from ..dao.product_dao import get_member_product_dao, delete_product_dao, Product, \
                              add_product_topool_dao, check_no_repeat_product_dao, update_one_product_dao, \
                              get_one_product_dao
from ..tool.crawl import web_crawl

router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse, tags=['product'])
def get_member_product_view(request: Request):
    if request.cookies:
        if 'sid' in list(request.cookies.keys()):
            session_id = request.cookies['sid']
            member_id = redis.get(session_id)
            if member_id:
                get_member_product_url = root_url + 'product/get_member_product'
                all_data = requests.get(get_member_product_url, json = {'member_id':member_id})
                all_data_array = json.loads(all_data.text)
                return templates.TemplateResponse("Product_List.html",{"request": request, "product_rows": all_data_array,
                                                                        "member_id": member_id})
            else:
                return JSONResponse(content={'message': "Cookie outdate, please login again!!"})
        else:
            return JSONResponse(content={'message': "No cookie!!"})
        
    else:
        return JSONResponse(content={'message': "No cookie!!"})


@router.get("/get_member_product", tags=['product'])   
def get_member_product(member_id: str = Body(..., embed=True)):
    data = get_member_product_dao(member_id)
    return data


@router.post("/get_one_product", tags=['product'])   
def get_one_product(member_id: str = Body(..., embed=True), id: str = Body(..., embed=True)):
    data = get_one_product_dao(member_id, id)
    return data


@router.delete("/delete_product", tags=['product'])   
def delete_product(request: Request, id: str=Body(..., embed=True)):
    if request.cookies:
        if 'sid' in list(request.cookies.keys()):
            session_id = request.cookies['sid']
            member_id = redis.get(session_id)
            if member_id:
                result = delete_product_dao(id=id, member_id=member_id)
                if result['success']:
                    return JSONResponse(content={"success":True, 'message': "Delete product successfully!"})
                else:
                    return JSONResponse(content={"success":False, 'message':result["message"]})
            else:
                return JSONResponse(content={'message': "Cookie outdate, please login again!!"})
        else:
            return JSONResponse(content={'message': "No cookie!!"})
        
    else:
        return JSONResponse(content={'message': "No cookie!!"})




@router.post("/add_product_topool", tags=['product'])
def add_product_topool(request: Request, input_url: str = Body(...,embed=True)):
    if request.cookies:
        if 'sid' in list(request.cookies.keys()):
            session_id = request.cookies['sid']
            member_id = redis.get(session_id)
            if member_id:
                if input_url.strip() == '':
                    return JSONResponse(content={'success': False, 'message': "Value cannot be blank, please fill in!!"})

                response = web_crawl(input_url)
                if response['success']:
                    product_info = response['product_info']
                    product_name = product_info['product_name']
                    product_price = product_info['product_price']
                    product_url = product_info['product_url']
                    channel_name = product_info['channel_name']
                    input_product = Product(product_name=product_name, product_price=product_price, product_url=product_url,
                                            member_id=member_id, channel_name=channel_name)
                    try:
                        no_repeat = check_no_repeat_product_dao(input_product)
                        if no_repeat:
                            try: 
                                response = add_product_topool_dao(input_product)
                                return JSONResponse(content=response)
                            except:
                                return JSONResponse(content={'success': False, 'message': "Error occurs when add product to pool!"})
                        else:
                            return JSONResponse(content={'success': False, 'message': "Product has already been put in the pool!!"})
                    except:
                        return JSONResponse(content={'success': False, 'message': "Error occurs when check repeated product!"})
                else:
                    ## url無法解析
                    return JSONResponse(content={'success': False, 'message': str(response['message'])})
                    
            
            else:
                return JSONResponse(content={'success': False, 'message': "Cookie outdate, please login again!!"})
        else:
            return JSONResponse(content={'success': False, 'message': "No cookie!!"})
            
    else:
        return JSONResponse(content={'success': False, 'message': "No cookie!!"})


@router.put("/update_one_product", tags=['product'])
def update_one_product(request: Request, input_url: str = Body(...), id: str =Body(...)):
    if request.cookies:
        if 'sid' in list(request.cookies.keys()):
            session_id = request.cookies['sid']
            member_id = redis.get(session_id)
            if member_id:
                response = web_crawl(input_url)
                get_one_product_url = root_url + 'product/get_one_product'
                data = requests.post(get_one_product_url, json = {'member_id':member_id, 'id':id})
                original_product = json.loads(data.text)[0]
                if response['success']:
                    product_info = response['product_info']
                    product_name = product_info['product_name']
                    product_price = product_info['product_price']
                    product_url = product_info['product_url']
                    channel_name = product_info['channel_name']
                    input_product = Product(product_name=product_name, product_price=product_price, product_url=product_url,
                                            member_id=member_id, channel_name=channel_name)
                    if product_name == original_product['product_name'] and int(product_price) == original_product['product_price']:
                        change = False
                    else:
                        change = True
                    try:
                        try: 
                            response = update_one_product_dao(input_product, id)
                            if change:
                                response['change'] = True
                                response['message'] = response['message'] + '\n' + 'Product info has changed!'
                            else:
                                response['change'] = False
                                response['message'] = response['message'] + '\n' + 'No product info changes!'
                            print(response)
                            return JSONResponse(content=response)
                        except:
                            return JSONResponse(content={'success': False, 'message': "Error occurs when add product to pool!"})
                        
                    except: 
                        return JSONResponse(content={'success': False, 'message': "Error occurs when check repeated product!"})
                else:
                    ## url無法解析
                    return JSONResponse(content={'success': False, 'message': str(response['message'])})
                    
            
            else:
                return JSONResponse(content={'success': False, 'message': "Cookie outdate, please login again!!"})
        else:
            return JSONResponse(content={'success': False, 'message': "No cookie!!"})
            
    else:
        return JSONResponse(content={'success': False, 'message': "No cookie!!"})

@router.put("/update_all_product", tags=['product'])
def update_all_product(request: Request):
    if request.cookies:
        if 'sid' in list(request.cookies.keys()):
            session_id = request.cookies['sid']
            member_id = redis.get(session_id)
            if member_id:
                get_member_product_url = root_url + 'product/get_member_product'
                data = requests.get(get_member_product_url, json = {'member_id':member_id})
                original_products = json.loads(data.text)
                change_product = 0
                try:
                    for original_product in original_products:
                        update_one_product_url = root_url + 'product/update_one_product'
                        response = requests.put(update_one_product_url, json = {'input_url':original_product['product_url'], 'id':original_product['id']}, cookies=request.cookies)
                        response = json.loads(response.text)
                        if response['change']:
                            change_product = change_product + 1
                    response['success'] = True
                    response['message'] = 'Update all product successfully'
                    response['message'] = response['message'] + '\n' + '{} product info has changed!'.format(change_product)
                    return JSONResponse(content=response)
                except:
                    return JSONResponse(content={'success': False, 'message': "Error occurs when update product!"})
            else:
                return JSONResponse(content={'success': False, 'message': "Cookie outdate, please login again!!"})
        else:
            return JSONResponse(content={'success': False, 'message': "No cookie!!"})
            
    else:
        return JSONResponse(content={'success': False, 'message': "No cookie!!"})


