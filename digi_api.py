import os
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests
from time import sleep
import urllib3
import json
from pathlib import Path

headers = [
    {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,fa;q=0.8',
        'Cookie': 'tracker_glob_new=fuxh0u6; _ga=GA1.1.1110305624.1700733532; tracker_session=2TWrpQn; _sp_ses.13cb=*; TS01c77ebf=010231059174b099361fc81358934f6ee0c53821e18211eb649170bd3eff70476a1e316963ac2f16aedd122f4f73f30137eb459c563177599d752dd44fa425c3ee712e0554b82ac6d92de22be9a5840a7e5501eb0c; _hp2_ses_props.1726062826=%7B%22r%22%3A%22https%3A%2F%2Fwww.digikala.com%2F%22%2C%22ts%22%3A1700921585300%2C%22d%22%3A%22www.digikala.com%22%2C%22h%22%3A%22%2Fsearch%2Fcategory-men-polo-shirt%2F%22%7D; _hp2_id.1726062826=%7B%22userId%22%3A%225696216287148220%22%2C%22pageviewId%22%3A%227745448019084829%22%2C%22sessionId%22%3A%228064032131825496%22%2C%22identity%22%3Anull%2C%22trackerVersion%22%3A%224.0%22%7D; _ga_QQKVTD5TG8=GS1.1.1700908592.4.1.1700921601.0.0.0; _sp_id.13cb=0874ab0f-1994-47aa-9ee4-2d26e42241ac.1700733530.4.1700921603.1700742668.b8f0050e-bf1a-42bb-8465-c823fb1b3507.ebce8a5b-7264-43e8-b75e-2659a07d7b12.dd932bfa-63e0-43e6-85d6-069397bf363b.1700908592373.200',
        'Sec-Ch-Ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    },
    {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,fa;q=0.8',
        'Cookie': 'tracker_glob_new=3Gm2c6s; TS01e4b47a=010231059189f448834cd3d3cb03619b11f687f63f9c1f3e640a14ed8e2d6ecfb8e10ee96fe6331d125701f9b3b266d96b0bd0474f941da4972b4f4142683489e3503405ba1f9960c62c1659622592fcc4755d24f9; _hjSessionUser_2754176=eyJpZCI6IjQ5NjA5OWM1LWZkMTMtNWE5MS1iNTRhLWFlMjJiMWU3MjQ2MiIsImNyZWF0ZWQiOjE2NzQ3Mzk5NjcxMzMsImV4aXN0aW5nIjpmYWxzZX0=; _ga_4S04WR965Q=GS1.1.1674739965.1.1.1674740475.0.0.0; _ga_LR50FG4ELJ=GS1.1.1694282212.6.0.1694282611.60.0.0; _ga=GA1.1.1851231018.1674739965; PHPSESSID=p09md3n011vcqp14hi0rc9afom; Digikala:User:Token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxMjM0NDYzMiwiZXhwaXJlX3RpbWUiOjE3MDE3OTA2MTMsInBheWxvYWQiOltdLCJwYXNzd29yZF92ZXJzaW9uIjoxLCJ0eXBlIjoidG9rZW4ifQ.dUxQfT3PRtiwo0EhlEo3EITIsEnIaEwNocAUw-iMriA; TS01b6ea4d=010231059138107928c1ee0258917fb6b72bc2e0d514672d877854eb50c23cc4c5514505b17d461757c8b17c4c20b81237ef5b389b8f9d1ff2cc8a87dfdc7b9b507453f01f22c141e260d4afea0d7e421fa3e6675b3c3b49aedec01b00da44289fd889fc18b95c278ccc67c74b2235b1d435e4c3769b76c1cdddaa3e636c46bdbb81cab4d0; tracker_session=6UTl2kr; _sp_ses.13cb=*; _hp2_ses_props.1726062826=%7B%22ts%22%3A1700985247919%2C%22d%22%3A%22www.digikala.com%22%2C%22h%22%3A%22%2Flanding%2Fmobile_brands%2F%22%7D; TS01c77ebf=0102310591d4efad2241628b539dce32ddebb41a7843e093f54bf8eb5dc1bc7171a097b3dc13867fa19977330d9b3c1696ea50d6492877eac9e09f45a00e7abad2a89c0f4f9416ccb0957f129ea25a466c1351eff5; _hp2_id.1726062826=%7B%22userId%22%3A%227125822647855584%22%2C%22pageviewId%22%3A%222793394214784089%22%2C%22sessionId%22%3A%221484630074962318%22%2C%22identity%22%3Anull%2C%22trackerVersion%22%3A%224.0%22%7D; _ga_QQKVTD5TG8=GS1.1.1700983407.12.1.1700985274.0.0.0; _sp_id.13cb=a635c38a-d5e9-47bb-8f6c-b847c7918741.1674739962.21.1700985292.1700943432.74727343-40de-42e9-a8ff-78e05e0a9840.f890b956-b6b8-4e2a-af24-b8b5a1347233.1274eaae-62b6-4ffc-bf6a-24d27cc32cc7.1700983407084.75',
        'Origin': 'https://www.digikala.com',
        '': 'https://www.digikala.com/',
        'Sec-Ch-Ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        # 'Sec-Fetch-User': '?1',
        # 'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'X-Web-Client':'desktop',
        'X-Web-Optimize-Response':'1',
    }
    ]


def getHeaders():
    return headers[0]



def get_products_id(c):
    global number_of_pages, All_IDS, url
    try:
        for i in range(c,number_of_pages+c,2):
            response = urllib3.request("Get", url.format(i), headers=getHeaders())
            data = BeautifulSoup(response.data, features="html.parser")
            data = json.loads(str(data))
            if data["status"] == 200:
                for pr in data['data']['products']:
                    id = pr["id"]
                    All_IDS.append(id)
            else:
                print("PAGE_LEECH_ERROR", data["status"], data['message'])
                sleep(0.3)
                response = urllib3.request("Get", url.format(i), headers=getHeaders())
                data = BeautifulSoup(response.data, features="html.parser")
                data = json.loads(str(data))
                if data["status"] == 200:
                    for pr in data['data']['products']:
                        id = pr["id"]
                        All_IDS.append(id)
        print("ALL PRODUCTS_ID LEECHED, Thread:",c)        
            # sleep(0.1)
    except Exception as e:
        print("ERROR in get_products_id. Page:", i,"ERROR:",e)
        sleep(0.3)
        get_products_id(c)


def get_product_images(id):
    global leeched, logs
    try:
        pr_res = urllib3.request("Get", f"https://api.digikala.com/v2/product/{id}/", headers=getHeaders())
        pr_data = BeautifulSoup(pr_res.data,features="html.parser")
        images = []
        data = json.loads(str(pr_data))
        if(data['status']==200):
            # logs.append({f"https://api.digikala.com/v2/product/{id}/",str(data['data']['product']['images'])})
            if('main' in data['data']['product']['images'].keys()):
                images.append(data['data']['product']['images']['main']['url'][0])
            if('list' in data['data']['product']['images'].keys()):
                for i in range(len(data['data']['product']['images']['list'])):
                    images.append(data['data']['product']['images']['list'][i]['url'][0])
            # images = image_selector(images)
            download_image(images, id)
            leeched+=1
            if(leeched%10==0):
                print(leeched)
        else:
            print("LEECH_Error_Image:",data['status'], id)
            sleep(0.1)
            get_product_images(id)
    except Exception as e:
        print(f"ERROR in get_product_images {id}:",e)
        sleep(0.3)
        get_product_images(id)

def image_selector(images):
    pass

def download_image(images, id):
    for url in images:
        u = urlparse(url)
        img_data= requests.get(url=url, headers=getHeaders()).content
        with open(f"{os.getcwd()}/images/{id}_"+os.path.basename(u.path), 'wb+') as handler:
            handler.write(img_data)


def download_image_to_folder(images, id):
    if(not Path.is_dir(Path(f"{os.getcwd()}/images/{id}"))):
        os.mkdir(f"{os.getcwd()}/images/{id}")
    for url in images:
        u = urlparse(url)
        img_data= requests.get(url=url, headers=getHeaders()).content
        with open(f"{os.getcwd()}/images/{id}/"+os.path.basename(u.path), 'wb+') as handler:
            handler.write(img_data)
        # sleep(0.1)

def get_pages_info(url):
    global number_of_pages
    try:
        response = urllib3.request("Get", url.format(1), headers=getHeaders())
        data = BeautifulSoup(response.data, features="html.parser")
        data = json.loads(str(data))
        if data["status"] == 200:
            number_of_pages = data['data']['pager']['total_pages']
            print("Pages:", data['data']['pager']['total_pages'], "Products:", data['data']['pager']['total_items'])
            if(number_of_pages>100):
                print("pages are more than 100. please contact me.")
                number_of_pages = 100
    except Exception as e:
        print("get_pages_info Error:", e)

# def logger_func(f):
#     while(True):
#         if(len(logs!=0)):
#             for l in logs:
#                 f.write(l)
#         # sleep(0.5)


# logs=[]
All_IDS = []
number_of_pages = 100




######## URL HEREEEEEE########
######## URL HEREEEEEE########
# has_selling_stock=1&
#                               sort=27
# 'page={0}' ... bayad page injory bashe, age dota page= dasht, faghat oni ke dakhel seo_url NIST. {0}&sort=27&has_selling_stock=1
url = "https://api.digikala.com/v1/categories/stretching-tools/search/?seo_url=%2Fcategory-stretching-tools%2F%3Fsort%3D7&page={0}&sort=7&has_selling_stock=1"
######## URL HEREEEEEE########
######## URL HEREEEEEE########
leeched = 0
# f = open("LOGS.txt",'a')

print("Getting Pages Info")
get_pages_info(url)

executor = ThreadPoolExecutor(max_workers=2)
executor.submit(get_products_id,1)
executor.submit(get_products_id,2)
# executor_log = ThreadPoolExecutor(max_workers=1)
# executor_log.submit(logger_func,f)
print("Starting Loop")
executor2 = ThreadPoolExecutor(max_workers=20)
while(True):
    if len(All_IDS)>0:
        for id in All_IDS:
            executor2.submit(get_product_images,id)
            del All_IDS[All_IDS.index(id)]        
    # executor2.shutdown(wait=True)