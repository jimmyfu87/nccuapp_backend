from bs4 import BeautifulSoup
import requests
import json

def lambda_handler(event, context):
    # TODO implement
    # print(event['body'])
    # print(json.loads(event['body']))
    input_url = json.loads(event['body'])['input_url']
    # input_url = event['input_url']
    if "pchome.com.tw" in input_url:                    
        response = crawl_pchome(input_url)
    # elif ("https://shopee.tw/" in input_url) and ("-i." in input_url):
    #     response = crawl_shopee(input_url) 
    elif "momoshop.com.tw/goods" in input_url:
        response = crawl_momo(input_url) 
    elif "buy.yahoo.com/gdsale" in input_url:
        pass
    else:
        response = {'success': False, 'message': "Sorry we are not not supported to crawl this website"}
    
    return response


def crawl_pchome(input_url: str):
    product_url = input_url
    try:
        if "?fq" in product_url:
            del_index = product_url.index('?fq')
            product_url = product_url[0:del_index]
        pos1 = product_url.index('/24h')
        pos11 = product_url.index('/prod')
        product_url = product_url[0:pos1] + "/ecapi-cdn.pchome.com.tw/ecshop/prodapi/v2" + product_url[pos11:] + "-000&fields=Name,Price&_callback=jsonp_prod"
        headers = {"user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}
        r_text = requests.get(product_url, headers=headers).text
        r_text = r_text.replace("try{jsonp_prod(","").replace("});}catch(e){if(window.console){console.log(e);}}", "")
        pos2 = r_text.index(':')
        r_text = json.loads(r_text[pos2+1:])
        product_name = r_text['Name']
        product_price = r_text['Price']['P']
        return {'success': True, 'product_info': {'product_name': product_name, 'product_price': product_price, 
                                     'product_url':input_url, 'channel_name': 'Pchome' }}
    except Exception as e:
        return {'success': False, 'message':str(e)}

    
# def crawl_shopee(input_url: str):
#     product_url = input_url
#     pos1 = product_url.index("i.")
#     product_url =  product_url[pos1+2:]
#     if "." in  product_url:
#         pos2 = product_url.index(".")
#         pos3 = product_url.index("?")
#         shopid = product_url[0:pos2]
#         itemid = product_url[pos2+1:pos3]
#         product_url = "https://shopee.tw/api/v4/item/get?itemid="+itemid+"&shopid="+shopid;
#     try:
#         headers = {"x-api-source":"pc","af-ac-enc-dat": "null"} 
#         r = requests.get(product_url, headers=headers)
#         r.encoding = 'utf-8'
#         r_text = json.loads(r.text)['data']
#         product_name = r_text['name']
#         product_price = str(r_text['price_max'])[0:-5]
#         return {'success': True, 'product_info': {'product_name': product_name, 'product_price': product_price, 
#                 'product_url':input_url, 'channel_name': '蝦皮購物' }}
#     except Exception as e:
#         # logger.error("Error occurs when crawl_shopee(), error message: {}".format(e))
#         return {'success': False, 'message': e}


def crawl_momo(input_url: str):
    product_url = input_url
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}
        r_text = requests.get(product_url, headers=headers).text
        soup = BeautifulSoup(r_text, features="html.parser")
        product_name =  soup.find('meta',{'property':'og:title'})['content']
        product_price =  soup.find('meta',{'property':'product:price:amount'})['content']
        return {'success': True, 'product_info': {'product_name': product_name, 'product_price': product_price, 
                'product_url':input_url, 'channel_name': 'Momo' }}
    except Exception as e:
        return {'success': False, 'message': str(e)}