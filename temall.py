
# 2019/04/11
# 第一次迭代 2019/04/14
# -*- coding: utf-8 -*-


import datetime
import re
import os
import requests

import fangtang

"""
1.由于爬取天猫这个东西需要用到cookie,需要替换自己的cookie
2.方糖的key也需要换成自己的key
3.fangtang为自己封装的一个api，用于推送服务器的消息给用户【这么说。。真要脸】
4.目前天猫有个促销价格和优惠没有找到是哪个js文件，所以暂时先不写【搞一个单独的模块】
5.价格对比没有想好怎么搞
6.对于天猫有好几个不同的网址，所以在main()中设置了简单的host替换，如果不换就404
"""

# 将爬虫获取的数据写入本地，这里本来的预设是价格对比，目前没有想好怎么写，就暂时写一个存本地的模块


def flie_change(price):
    with open('price.txt', 'a+') as f:
        f.write(str(price))
        f.write('\t')
        f.write(str(datetime.datetime.now()))
        f.write('\n')
        fangtang.shuju("今日检测价格,喵喵喵~", "今日份价格：" + str(price) +
                       "获取时间：" + str(datetime.datetime.now()))

# 爬虫的主体


def url(url_new, header):
    req = requests.get(url_new, headers=header).text
    req = req.replace('\n', '')
    req = req.replace('\r', '')
    req = req.replace('\t', '')
    if "priceCent" in req:
        pat_1 = '"priceCent":[0-9]*'
        price = re.compile(pat_1).findall(req)
        price_shop = price[0]
        charge = int(price_shop.replace('"priceCent":', ''))
        return charge
    else:
        return False


def main():
    # 读取本地url文件，获取temall的url地址
    os.chdir('/root/pachong')
    with open('url.txt', 'r') as f:
        url_frist = f.readlines()
    ziheng = 0
    while ziheng < len(url_frist):
        # 添加循环，增加监控的次数
        url_old = url_frist[ziheng]
        url_old = url_old.replace("\n", "")
        url_last = str(url_old)  # 获取循环的网址

        # 这里添加一个判断，因为天猫有很多不同的头，所以需要应对，会慢慢补充！
        if "chaoshi.detail.tmall.com" in url_last:
            host_ = 'chaoshi.detail.tmall.com'
        elif "detail.tmall.com" in url_last:
            host_ = 'detail.tmall.com'
        elif 'detail.tmall.hk' in url_last:
            host_ = 'detail.tmall.hk'
        else:
            fangtang.shuju("你托管的网址商品的头部并不在支持列表中", " 遇到这样的问题肯定就要联系那个写这个代码的人了！")
            exit()

        header = {
            'Host': host_,
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
            fangtang.shuju(
                "这是一个预设性质的错误！", "遇到这错误是因为访问出错或者天猫改变了原来代码的变量，联系那个写代码的男人吧！")
            exit()
        else:
            charge_new = float(data/100)
            flie_change(charge_new)
        ziheng += 1


if __name__ == "__main__":
    main()
