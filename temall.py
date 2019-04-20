
# 2019/04/11
# 第一次迭代 2019/04/14
# 第二次迭代 2019/04/15
# 第三次迭代 2019/04/16 --
# demo_1_0 服务器测试通过 2019/04/17
# -*- coding: utf-8 -*-

import datetime
import os
import re
import time
import json

import requests

import fangtang

"""
3.fangtang为自己封装的一个api，用于推送服务器的消息给用户【这么说。。真要脸】
"""

# 将爬虫获取的数据写入本地，是价格对比，获得每次爬取和上次爬取的价格进行对比，不同的结果对应不同的消息推送了


def flie_change(title, post_money, price, other):
    # 进入日志目录
    os.chdir('__YOUR_FLIE__/logs/')  # 进入logs目录
    time_filename = str(time.strftime('%Y.%m.%d', time.localtime(time.time())))
    with open(time_filename+'.txt', 'a+') as f:
        f.write(str(price))
        f.write('\n')
        f.write(str(datetime.datetime.now()))
        f.write('\n')
    # 搞不明白为什么我写入了文件，然后再直接读出来，却还是之前没有写入的状态。辣鸡
    with open(time_filename+'.txt', 'r') as f:
        charge = f.readlines()
    # 这里设置爬取数据的次数，并且进行计算
    # 如果价格波动了就进行提醒，价格没有波动直接提醒【表示自己还活着】
    if len(charge) == 2:
        fangtang.shuju(str(title), " - 价格为【如果有优惠即优惠价格，如果没有优惠即原价】  " + str(
            price) + "\n" + ' - 快递费      '+str(post_money) + "\n" + " - 其他优惠信信息【未处理】" + "\n" + str(other))
    else:
        charge_date = charge[-4:]
        if float(charge_date[0]) > float(charge_date[2]):
            fangtang.shuju("价格降低了嘞 喜大普奔 ", str(title) +
                           " - 可以考虑入手 但是要考虑好你的钱包" + "\n" + " - 价格为【如果有优惠即优惠价格，如果没有优惠即原价】 " + charge_date[2] + "\n" + ' - 快递费'+str(post_money) + "\n" + "  - 其他优惠信信息【未处理】" + "\n" + str(other))
        elif float(charge_date[0]) < float(charge_date[2]):
            fangtang.shuju("价格升高了嘞 嘤嘤嘤 ", str(title) +
                           " - 让你刚才不买 让你不买 不买" + "\n" + " - 价格为【如果有优惠即优惠价格，如果没有优惠即原价】 " + charge_date[2]+"\n" + ' - 快递费'+str(post_money) + "\n" + "  - 其他优惠信信息【未处理】" + "\n" + str(other))
        else:
            pass

# 爬虫的主体
# 直接在获取的网页中进行寻找，如果有就下一步，如果没有就直接返回一个False


def url(url_new, header):
    req = requests.get(url_new, headers=header).text
    req = req.replace('\n', '')
    req = req.replace('\r', '')
    req = req.replace('\t', '')
    if "addressData" in req:
        pat_json = '"addressData":[\S\s]*} </script>'
        json_re = re.compile(pat_json).findall(req)
        json_re = str(json_re)
        json_re = json_re.replace("['", "{")
        json_re = json_re.replace(" </script>']", '')
        data = json.loads(json_re)
        return data  # 返回的是json读取以后的js
    else:
        return False

def main():
    os.chdir('/__YOUR_FLIE__/')
    # 读取本地url文件，获取temall的url地址
    with open('url.txt', 'r') as f:
        url_frist = f.readlines()
    url_old = url_frist[0]
    url_old = url_old.replace("\n", "")
    url_last = str(url_old)
    # 这里添加一个判断，因为天猫有很多不同的头，所以需要应对，会慢慢补充！
    if "chaoshi.m.detail.tmall.com" in url_last:
        host_ = 'chaoshi.m.detail.tmall.com'
    elif "detail.m.tmall.com" in url_last:
        host_ = 'detail.m.tmall.com'
    elif 'detail.m.tmall.hk' in url_last:
        host_ = 'detail.m.tmall.hk'
    else:
        fangtang.shuju("你托管的网址商品的头部并不在支持列表中", " 遇到这样的问题肯定就要联系那个写这个代码的人了！")
        exit()

    header = {
        'Host': host_,
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/%s Mobile Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Connection': 'keep-alive',
        'Cookie': __YOUR_COOKIE__,
        'Upgrade-Insecure-Requests': '1',
        'TE': 'Trailers'
        }
    data = url(url_last, header)
    if data == False:
        fangtang.shuju(
            "这是一个预设性质的错误！", "遇到这错误是因为访问出错或者天猫改变了原来代码的变量，联系那个写代码的男人吧！")
        exit()
    else:
        title = data["item"]["title"]
        post_money = data['delivery']['postage']  # 快递费
        price = data['price']['price']['priceText']  # 促销价#促销价格【若无促销价格即为原价】
        other = data['price']['shopProm']  # 其他优惠信息
        flie_change(title, post_money, price, other)

if __name__ == "__main__":
    main()
