# 2019/04/11
# -*- coding: utf-8 -*-

import datetime
import re
import os

import requests

import fangtang

"""
1.由于爬取天猫这个东西需要用到cookie,需要替换自己的cookie
2.对于商品短链接是否需要转换成长连接需要测试
3.fangtang为自己封装的一个api，用于推送服务器的消息给用户
"""


def flie_change(price):
    with open('price.txt', 'a+') as f:
        f.write(str(price))
        f.write('\t')
        f.write(str(datetime.datetime.now()))
        f.write('\n')
        fangtang.shuju("今日检测价格,喵喵喵~", "今日份价格：" + str(price) +
                       "获取时间：" + str(datetime.datetime.now()))


def url(url_new, header):
    req = requests.get(url_new, headers=header).text
    if "priceCent" in req:
        req = req.replace('\r', '')
        req = req.replace('\n', '')
        req = req.replace('\t', '')
        pat_0 = 'TShop.Setup[\s\S]*</script></div>'
        re_json_old = re.compile(pat_0).findall(req)
        data_josn = str(re_json_old)
        pat_1 = '"priceCent":[0-9]*'
        price = re.compile(pat_1).findall(data_josn)
        return price
    else:
        fangtang.shuju("爬虫数据不见了！", "这是一个预设性的警告，大概是因为主人很久没有更新了吧，你掀起波澜~把我忘了吧~~")
        return False


def main():
    print(os.getcwd())
    os.chdir('/root/pachong')
    # 读取本地url文件，获取temall的url地址
    with open('url.txt', 'r') as f:
        url_frist = f.readlines()
    url_old = url_frist[0]
    url_last = str(url_old)
    print(url_last)
    header = {
        'Host': 'detail.tmall.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Referer': url_last,
        'Connection': 'keep-alive',
        'Cookie': 't=edc8b3e37d5a6aa1fa671c8e4f92d029; cna=0tA1FWrG71sCAbYgMTK0FSn3; isg=BLa23S1B9q6HfYLLstzcrFUtBOqy1P1-kzyejiCfUBk0Y1b9iGeQIRwSe_-qUPIp; l=bBTv7DYuvkAZ0N81BOfwCZ111C79XIR44kPPhhmGvICP9N5B574lWZs3ePY6C31Vw1EvR3SVNIDpBeYBcQC..; thw=cn; uc3=vt3=F8dByEiVgCD9oAfeyx4%3D&id2=VyyUwjXHwa5x6w%3D%3D&nk2=saDUZFBwM%2BQ%3D&lg2=W5iHLLyFOGW7aA%3D%3D; tracknick=%5Cu4E00%5Cu7897%5Cu80A0%5Cu7C89; lgc=%5Cu4E00%5Cu7897%5Cu80A0%5Cu7C89; _cc_=W5iHLLyFfA%3D%3D; tg=0; mt=ci=21_1; enc=LfDm6GXnvOzezdvS7i9q%2FTGl18jWc2sHqK2S7IRsDzcDtVEO7r2I4dWIx7j0d%2BFepKcWf37QmQLP6LrOG3otsA%3D%3D; hng=CN%7Czh-CN%7CCNY%7C156; cookie2=1be5441af9776e43e7130bde01f0229a; _tb_token_=efbee03155d83; v=0',
        'Upgrade-Insecure-Requests': '1',
        'TE': 'Trailers'
    }
    data = url(url_last, header)
    if data == False:
        fangtang.shuju("拜拜~", "记得让主人更新代码呦~")
    else:
        price_shop = data[0]
        charge = int(price_shop.replace('"priceCent":', ''))
        charge_new = float(charge/100)
        flie_change(charge_new)


if __name__ == "__main__":
    main()
