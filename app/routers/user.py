import redis
from fastapi import APIRouter, Body, Request
from ..env.config import redis
from ..tool.authentication import get_hash_password, verify_cookies
from ..tool.send_email import send_email
from ..dao.user_dao import create_user_dao, check_member_id_exist_dao, login_dao, User, reset_password_dao, \
                           get_member_id_byemail_dao, check_member_id_email_exist_dao
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
import random, string
from ..env.config import get_logger


router = APIRouter()
templates = Jinja2Templates(directory="templates")
logger = get_logger('user')


@router.get("/Reset_Password.html")
def reset_password_view(request: Request):
    return templates.TemplateResponse("Reset_Password.html",{"request": request})


@router.get("/Forget_Password.html")
def forget_password_view(request: Request):
    return templates.TemplateResponse("Forget_Password.html",{"request": request})


@router.post("/register", tags=["user"])
def register(user: User):  
    logger.info('register()')
    logger.info('user: {}'.format(user))
    if user.member_id == "" or user.member_password == "" or user.member_email == "":
        return JSONResponse(content={"success": False, 'message': "Value cannot be blank, please fill in!!"})
    if " " in user.member_id or " " in user.member_password or " " in user.member_email:
        return JSONResponse(content={"success": False, 'message': "Value cannot contains blank, please fill in!!"})
    check_member_id_email_exist_response = check_member_id_email_exist_dao(user.member_id, user.member_email)
    if len(check_member_id_email_exist_response) == 0:
        hash_password = get_hash_password(user.member_password)
        response = create_user_dao(user.member_id, hash_password, user.member_email)
        return JSONResponse(content=response)
    else:
        return JSONResponse(content={"success": False, 'message': "This member id or email has already been used, please change it!!"})

@router.post("/login", tags=["user"])
def login(user: User):
    logger.info('login()')
    logger.info('user: {}'.format(user))
    check_member_id_exist_response = check_member_id_exist_dao(user.member_id)
    if len(check_member_id_exist_response) == 1:
        hash_password = get_hash_password(user.member_password)
        login_response = login_dao(user.member_id, hash_password)
        if len(login_response) == 1:
            hash_key = get_hash_password(user.member_id + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            redis.setex(hash_key, 1800, user.member_id)
            response = JSONResponse(content={"success": True})
            response.set_cookie(key="sid", value=hash_key)
            return response
        else:
            return JSONResponse(content={"success": False, 'message': "Incorrect member id or member password!!"})

    elif len(check_member_id_exist_response) == 0:
        return JSONResponse(content={"success": False, 'message': "{member_id} is not a valid member id, please register it!!".format(member_id=user.member_id)})


@router.get("/logout", tags=['user'])
def logout(request: Request):
    logger.info('logout()')
    if redis.exists(request.cookies['sid']):
        redis.delete(request.cookies['sid'])
        return JSONResponse(content={"success": True, 'message': "Logout Successfully"})
    else:
        return JSONResponse(content={"success": False, 'message': "Already logout!!"})




@router.patch("/reset_password")
def reset_password(request: Request, member_new_password: str=Body(..., embed=True)):
    logger.info('reset_password()')
    logger.info('member_new_password: {}'.format(member_new_password))
    verify_response = verify_cookies(request)
    if verify_response['success']:
        member_id = verify_response['member_id']
        member_new_password = get_hash_password(member_new_password)
        response = reset_password_dao(member_id, member_new_password)
        if response['success']:
            redis.delete(request.cookies['sid'])
        return JSONResponse(content=response)
    else:
        return JSONResponse(content={'message': verify_response['message']})


@router.post("/send_reset_password_email")
def send_reset_password_email(request: Request, member_email: str=Body(..., embed=True)):
    logger.info('send_reset_password_email()')
    logger.info('member_email: {}', member_email)
    try:
        data = get_member_id_byemail_dao(member_email)  
        if len(data) == 1:
            member_id = data[0]['member_id']
            member_new_password = ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(10))
            member_new_password_hash = get_hash_password(member_new_password)
            response = reset_password_dao(member_id, member_new_password_hash)
            if response['success']:
                try:
                    response = send_email(member_email, member_id, member_new_password)
                    if response['success']:
                        return JSONResponse(content=response)
                    else:
                        logger.error("Error occurs when send_reset_password_email()")
                        return JSONResponse(content={'success':False, 'message': 'Error occurs when sending email'})
                
                except Exception as e:
                    logger.error("Error occurs when get_member_product_dao(), error message: {}".format(e))
                    return JSONResponse(content={'success':False, 'message': 'Error occurs when sending email' })
            else:
               return JSONResponse(content=response)
        elif len(data) == 0:
            return JSONResponse(content={'success':False, 'message': 'No member with this email' })
        else:
            return JSONResponse(content={'success':False, 'message': 'More than one member id with email' })

    except Exception as e:
        logger.error("Error occurs when send_reset_password_email(), error message: {}".format(e))
        return JSONResponse(content={'success':False, 'message': e })


