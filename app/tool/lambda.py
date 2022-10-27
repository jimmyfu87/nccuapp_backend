import json
import requests


def lambda_handler(event, context):
    # TODO implement
    input_url =event['input_url']
    if "pchome.com.tw" in input_url:                    
        response = crawl_pchome(input_url)
    elif ("https://shopee.tw/" in input_url) and ("-i." in input_url):
        response = crawl_shopee(input_url) 
    elif "momoshop.com.tw/goods" in input_url:
        pass
    elif "buy.yahoo.com/gdsale" in input_url:
        pass
    else:
        response = {'success': False, 'message': "Sorry we are not not supported to crawl this website"}

    return {
        'statusCode': 200,
        'body': response
    }



def crawl_pchome(input_url: str):
    product_url = input_url
    try:
        if "?fq" in product_url:
            del_index = product_url.index('?fq')
            product_url = product_url[0:del_index]
        pos1 = product_url.index('/prod')
        product_url = product_url[0:pos1] + "/ecapi/ecshop/prodapi/v2" + product_url[pos1:] + "&fields=Name,Price&_callback=jsonp_prod"
        r_text = requests.get(product_url).text
        r_text = r_text.replace("try{jsonp_prod(","").replace("});}catch(e){if(window.console){console.log(e);}}", "")
        pos2 = r_text.index(':')
        r_text = json.loads(r_text[pos2+1:])
        product_name = r_text['Name']
        product_price = r_text['Price']['P']
        return {'success': True, 'product_info': {'product_name': product_name, 'product_price': product_price, 
                                     'product_url':input_url, 'channel_name': 'Pchome' }}
    except Exception as e:
        return {'success': False, 'message': e}
    
def crawl_shopee(input_url: str):
    product_url = input_url
    pos1 = product_url.index("i.")
    product_url =  product_url[pos1+2:]
    if "." in  product_url:
        pos2 = product_url.index(".")
        pos3 = product_url.index("?")
        shopid = product_url[0:pos2]
        itemid = product_url[pos2+1:pos3]
        product_url = "https://shopee.tw/api/v4/item/get?itemid="+itemid+"&shopid="+shopid;
    try:
        r = requests.get(product_url)
        r.encoding = 'utf-8'
        r_text = json.loads(r.text)['data']
        product_name = r_text['name']
        product_price = str(r_text['price_max'])[0:-5]
        return {'success': True, 'product_info': {'product_name': product_name, 'product_price': product_price, 
                'product_url':input_url, 'channel_name': '蝦皮購物' }}
    except Exception as e:
        return {'success': False, 'message': e}
    