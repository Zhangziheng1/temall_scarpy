# 2019/04/11
# -*- coding: utf-8 -*-

import re
import time
import json

import requests

def json_editor(data):
    json_data = json.loads(data)
    print(json_data)

def index_page(url_index,headers):
    index_page_s = requests.get(url_index,headers=headers) #获取搜索页面的结果
    data_index = index_page_s.text
    pat = 'g_page_config = [\S\s]*g_srp_loadCss'
    re_json = re.compile(pat).findall(data_index)
    data_json = str(re_json)
    data = data_json.lstrip("['g_page_config = ")
    data_new = data.rstrip("\ng_srp_loadCss']")
    return data_new
    
    
if __name__ == "__main__":
    data = str(input(
        "商品内容:"
    ))
    url = "https://s.taobao.com/search?q="+data+"&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306"
    headers = {
        'Host': 's.taobao.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0',
        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Connection': 'keep-alive',
        'Cookie': 't=edc8b3e37d5a6aa1fa671c8e4f92d029; cna=0tA1FWrG71sCAbYgMTK0FSn3; isg=BDMz5WtWa3VDJiegN9NxJ0jqwTFXa9vDXtu7peXQr9KJ5FOGbTnKepF2ntSv3x8i; l=bBTv7DYuvkAZ0bsbBOCNNZ1sc97ORIOYYuWbYPy6i_5wK68_U07OlMXCZFJ6Vs5R6oYB4i5Wivp9-etXZ; thw=cn; cookie2=196ca9fcd6dc1c8e7d0f67879a81d7b7; v=0; _tb_token_=e3068e7b3e705; unb=4059506413; uc1=cookie14=UoTZ4MbunVjc9g%3D%3D&lng=zh_CN&cookie16=WqG3DMC9UpAPBHGz5QBErFxlCA%3D%3D&existShop=false&cookie21=VFC%2FuZ9ainBZ&tag=8&cookie15=U%2BGCWk%2F75gdr5Q%3D%3D&pas=0; sg=%E7%B2%893c; _l_g_=Ug%3D%3D; skt=859230eadc0553a2; cookie1=AQDIB2dOIkTfgI827%2FerlFcas7xXvn5ag28HW%2BkYxvc%3D; csg=8d8a6be1; uc3=vt3=F8dByEiVgCD9oAfeyx4%3D&id2=VyyUwjXHwa5x6w%3D%3D&nk2=saDUZFBwM%2BQ%3D&lg2=W5iHLLyFOGW7aA%3D%3D; existShop=MTU1NDk4Mzk4Mw%3D%3D; tracknick=%5Cu4E00%5Cu7897%5Cu80A0%5Cu7C89; lgc=%5Cu4E00%5Cu7897%5Cu80A0%5Cu7C89; _cc_=W5iHLLyFfA%3D%3D; dnk=%5Cu4E00%5Cu7897%5Cu80A0%5Cu7C89; _nk_=%5Cu4E00%5Cu7897%5Cu80A0%5Cu7C89; cookie17=VyyUwjXHwa5x6w%3D%3D; tg=0; mt=ci=21_1; enc=LfDm6GXnvOzezdvS7i9q%2FTGl18jWc2sHqK2S7IRsDzcDtVEO7r2I4dWIx7j0d%2BFepKcWf37QmQLP6LrOG3otsA%3D%3D; JSESSIONID=3D01309E5EFB33401A05BCCBAF3C80EE; hng=CN%7Czh-CN%7CCNY%7C156',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0',
        'TE': 'Trailers'
    }
    data = index_page(url,headers)
    json_editor(data)