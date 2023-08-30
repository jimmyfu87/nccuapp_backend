from fastapi import APIRouter, Body, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from ..env.config import root_url
import requests, json, httpx, asyncio
from fastapi.responses import HTMLResponse
from ..dao.product_dao import get_member_product_dao, delete_product_dao, Product, \
                              add_product_topool_dao, check_no_repeat_product_dao, update_one_product_dao, \
                              get_one_product_dao
from ..tool.crawl import web_crawl
from ..tool.authentication import verify_cookies
from ..env.config import get_logger

router = APIRouter()

templates = Jinja2Templates(directory="templates")
logger = get_logger('product')

@router.get("/", response_class=HTMLResponse, tags=['product'])
def get_member_product_view(request: Request):
    logger.info('get_member_product_view()')
    verify_response = verify_cookies(request)
    if verify_response['success']:
        member_id = verify_response['member_id']
        all_data_array = get_member_product_dao(member_id)
        return templates.TemplateResponse("Product_List.html",{"request": request, "product_rows": all_data_array,
                                                                "member_id": member_id})
    else:
        logger.error('Error occurs when get_member_product_view(), error message: {}'.format(verify_response['message']))
        return JSONResponse(content={'message': 'Error occurs when get product list view, please login again'})


@router.delete("/delete_product", tags=['product'])   
def delete_product(request: Request, id: str=Body(..., embed=True)):
    logger.info('delete_product()')
    logger.info('id: {}'.format(id))
    verify_response = verify_cookies(request)
    if verify_response['success']:
        member_id = verify_response['member_id']
        result = delete_product_dao(id=id, member_id=member_id)
        if result['success']:
            logger.info("Delete product successfully!")
            return JSONResponse(content={"success":True, 'message': "Delete product successfully!"})
        else:
            logger.error(('Error occurs when delete_product(), error message: {}'.format(result["message"])))
            return JSONResponse(content={"success":False, 'message':result["message"]})
    else:
        logger.error('Error occurs when delete_product(), error message: {}'.format(verify_response['message']))
        return JSONResponse(content={'message': 'Error occurs when delete product, please login again'})
       

@router.post("/add_product_topool", tags=['product'])
def add_product_topool(request: Request, input_url: str = Body(...,embed=True)):
    logger.info('add_product_topool()')
    logger.info('input_url: {}'.format(input_url))
    verify_response = verify_cookies(request)
    if verify_response['success']:
        member_id = verify_response['member_id']
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
                        logger.info("response: {}".format(response))
                        return JSONResponse(content=response)
                    except Exception as e:
                        logger.error('Error occurs when add_product_topool(), error message: {}'.format(e))
                        return JSONResponse(content={'success': False, 'message': "Error occurs when add product to pool!"})
                else:
                    return JSONResponse(content={'success': False, 'message': "Product has already been put in the pool!!"})
            except Exception as e:
                logger.error('Error occurs when add_product_topool(), error message: {}'.format(e))
                return JSONResponse(content={'success': False, 'message': "Error occurs when check repeated product!"})
        else:
            ## url無法解析
            logger.error("Error occurs when add_product_topool(), error message: {}".format(str(response['message'])))
            return JSONResponse(content={'success': False, 'message': str(response['message'])})
    else:
        logger.error('Error occurs when add_product_topool(), error message: {}'.format(verify_response['message']))
        return JSONResponse(content={'message': 'Error occurs when add product to pool, please login again'})


@router.put("/update_one_product", tags=['product'])
def update_one_product(request: Request, input_url: str = Body(...), id: str =Body(...)):
    logger.info('update_one_product()')
    logger.info('input_url: {}'.format(input_url))
    logger.info('id: {}'.format(id))
    verify_response = verify_cookies(request)
    if verify_response['success']:
        member_id = verify_response['member_id']
        response = web_crawl(input_url)
        original_product = get_one_product_dao(member_id, id)[0]
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
                response = update_one_product_dao(input_product, id)
                if change:
                    response['change'] = True
                    response['message'] = response['message'] + '\n' + 'Product info has changed!'
                else:
                    response['change'] = False
                    response['message'] = response['message'] + '\n' + 'No product info changes!'
                logger.info('response:{}'.format(response))
                return JSONResponse(content=response)
            except Exception as e:
                logger.error("Error occurs when update_one_product(), error message: {}".format(e))
                return JSONResponse(content={'success': False, 'message': "Error occurs when update one product"})
        else:
            ## url無法解析
            logger.error("Error occurs when update_one_product(), error message: {}".format(str(response['message'])))
            return JSONResponse(content={'success': False, 'message': 'Update product unsuccessfully!' + '\n'+ 
                                                                      'The product may be moved from this website, please delete this item.'})
    else:
        logger.error('Error occurs when update_one_product(), error message: {}'.format(verify_response['message']))
        return JSONResponse(content={'message': 'Error occurs when update one product, please login again'})
         
async def update_one_product(input_url: str, product_id: str, cookies: dict):
    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.put(
            root_url + 'product/update_one_product',
            json={'input_url': input_url, 'id': product_id},
            cookies=cookies
        )
    return response.json()

@router.put("/update_all_product", tags=['product'])
async def update_all_product(request: Request):
    logger.info('update_all_product()')
    verify_response = verify_cookies(request)
    if verify_response['success']:
        member_id = verify_response['member_id']
        original_products = get_member_product_dao(member_id)
        change_product = 0
        if len(original_products) == 0:
            return JSONResponse(content={'success': False, 'message': "There is no product in your pool."})
        try:
            async with httpx.AsyncClient(timeout=len(original_products)*20) as client:
                tasks = []
                for original_product in original_products:
                    task = update_one_product(
                        original_product['product_url'],
                        original_product['id'],
                        request.cookies
                    )
                    tasks.append(task)
                responses = await asyncio.gather(*tasks)
                change_product = sum(1 for response in responses if response['change'])
                response = {}
                response['success'] = True
                response['message'] = 'Update all product successfully'
                response['message'] = response['message'] + '\n' + '{} product info has changed!'.format(change_product)
                logger.info('response:{}'.format(response))
                return JSONResponse(content=response)
        except Exception as e:
            logger.error("Error occurs when update_all_product(), error message: {}".format(repr(e)))
            return JSONResponse(content={'success': False, 'message': "Error occurs when update all product, please update product one by one."})

    else:
        logger.error('Error occurs when update_all_product(), error message: {}'.format(verify_response['message']))
        return JSONResponse(content={'message': 'Error occurs when update all products, please login again'})


#同步的API
# @router.put("/update_all_product", tags=['product'])
# def update_all_product(request: Request):
#     logger.info('update_all_product()')
#     verify_response = verify_cookies(request)
#     if verify_response['success']:
#         member_id = verify_response['member_id']
#         original_products = get_member_product_dao(member_id)
#         change_product = 0
#         if len(original_products) == 0:
#             return JSONResponse(content={'success': False, 'message': "There is no product in your pool."})
#         try:
#             for original_product in original_products:
#                 update_one_product_url = root_url + 'product/update_one_product'
#                 response = requests.put(update_one_product_url, json = {'input_url':original_product['product_url'], 'id':original_product['id']}, cookies=request.cookies)
#                 response = json.loads(response.text)
#                 if response['change']:
#                     change_product = change_product + 1
#             response['success'] = True
#             response['message'] = 'Update all product successfully'
#             response['message'] = response['message'] + '\n' + '{} product info has changed!'.format(change_product)
#             logger.info('response:{}'.format(response))
#             return JSONResponse(content=response)
#         except Exception as e:
#             logger.error("Error occurs when update_all_product(), error message: {}".format(e))
#             return JSONResponse(content={'success': False, 'message': "Error occurs when update all product, please update product one by one."})

#     else:
#         logger.error('Error occurs when update_all_product(), error message: {}'.format(verify_response['message']))
#         return JSONResponse(content={'message': 'Error occurs when update all products, please login again'})
