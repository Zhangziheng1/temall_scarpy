# Author : ziheng_wind
# Email : wn345361049@163.com
# github : https://github.com/Zhangziheng1/temall_scarpy
# -*- coding: utf-8 -*-

import datetime
import json
import os
import re
import time

import requests

import fangtang
import fileread


def url_more(url_list, leng):
    """
    这里设置了url队列模式
    也就是多url多商品模式
    """
    fliename = 1
    for url in url_list:
        # 替换商品的请求头，模拟手机，并更换header
        if "chaoshi.detail.tmall.com" in url:
            host_ = 'chaoshi.m.detail.tmall.com'
        elif "detail.tmall.com" in url:
            host_ = 'detail.m.tmall.com'
        elif 'detail.tmall.hk' in url:
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
            'Cookie': "__YOUR_COOKIE__" ,
            'Upgrade-Insecure-Requests': '1',
            'TE': 'Trailers'
        }
        print(url)
        # 请求网址并且去掉那些没用的东西 = =
        req = requests.get(url, headers=header).text
        req = req.replace('\n', '')
        req = req.replace('\r', '')
        req = req.replace('\t', '')
        # 看咱们请求的网址对不对，有没有想要的东西，再用re匹配出josn字典，解析，不行就报错呗，嘿嘿嘿
        if "addressData" in req:
            pat_json = '"addressData":[\S\s]*} </script>'
            json_re = re.compile(pat_json).findall(req)
            json_re = str(json_re)
            json_re = json_re.replace("['", "{")
            json_re = json_re.replace(" </script>']", '')
            data = json.loads(json_re)
        else:
            fangtang.shuju(
                "这是一个预设性质的错误！", "遇到这错误是因为访问出错或者天猫改变了原来代码的变量，联系那个写代码的男人吧！")
            exit()
        # json字典解析出来的，咱们需要的东西~~
        title = data["item"]["title"]
        post_money = data['delivery']['postage']  # 快递费
        price = data['price']['price']['priceText']  # 促销价#促销价格【若无促销价格即为原价】
        other = data['price']['shopProm']  # 其他优惠信息
        # 进入logs目录，以爬取的次序为文件名进行存取操作
        os.chdir('/__YOUR__FLIE__/logs/')  # 进入logs目录
        with open(str(fliename)+'.txt', 'a+') as f:
            f.write(str(price))
            f.write('\n')
            f.write(str(datetime.datetime.now()))
            f.write('\n')
        with open(str(fliename)+'.txt', 'r') as f:
            charge = f.readlines()
        if len(charge) == 2:
            fangtang.shuju(str(title), " - 价格为【如果有优惠即优惠价格，如果没有优惠即原价】  " + str(price) + "\n" +
                           ' - 快递费      '+str(post_money) + "\n" + " - 其他优惠信信息【未处理】" + "\n" + str(other))
        else:
            charge_date = charge[-4:]
            if float(charge_date[0]) > float(charge_date[2]):
                fangtang.shuju("价格降低了嘞 喜大普奔 ", str(title) + " - 可以考虑入手 但是要考虑好你的钱包" + "\n" + " - 价格为【如果有优惠即优惠价格，如果没有优惠即原价】 " +
                               charge_date[2] + "\n" + ' - 快递费'+str(post_money) + "\n" + "  - 其他优惠信信息【未处理】" + "\n" + str(other))
            elif float(charge_date[0]) < float(charge_date[2]):
                fangtang.shuju("价格升高了嘞 嘤嘤嘤 ", str(title) + " - 让你刚才不买 让你不买 不买" + "\n" + " - 价格为【如果有优惠即优惠价格，如果没有优惠即原价】 " +
                               charge_date[2]+"\n" + ' - 快递费'+str(post_money) + "\n" + "  - 其他优惠信信息【未处理】" + "\n" + str(other))
            else:
                pass
        # 温馨的消息提醒
        if fliename == 1:
            time.sleep(5)
            fangtang.shuju(
                '休息一下', '为了防止天猫把我们的IP列为黑名单 方糖的消息提醒也是有限制的 于是让我们休息15秒钟 以后的每次爬取都会休息一会哦！')
            time.sleep(10)
        else:
            time.sleep(15)
        fliename += 1


"""

单url和多url是一样的东西，就是最后的存文件的操作不同，不多注释

"""


def onlyoneurl(url):
        # 这里添加一个判断，因为天猫有很多不同的头，所以需要应对，会慢慢补充！
    if "chaoshi.detail.tmall.com" in url:
        host_ = 'chaoshi.m.detail.tmall.com'
    elif "detail.tmall.com" in url:
        host_ = 'detail.m.tmall.com'
    elif 'detail.tmall.hk' in url:
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
        'Cookie': "__YOUR_COOKIE__",
        'Upgrade-Insecure-Requests': '1',
        'TE': 'Trailers'
    }
    req = requests.get(url, headers=header).text
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
    else:
        fangtang.shuju(
            "这是一个预设性质的错误！", "遇到这错误是因为访问出错或者天猫改变了原来代码的变量，联系那个写代码的男人吧！")
        exit()

    title = data["item"]["title"]
    post_money = data['delivery']['postage']  # 快递费
    price = data['price']['price']['priceText']  # 促销价#促销价格【若无促销价格即为原价】
    other = data['price']['shopProm']  # 其他优惠信息

    os.chdir('/__YOUR__FLIE__/logs/')  # 进入logs目录
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


def main():

    os.chdir('/__YOUR__FLIE__/')
    # 读取本地url文件，获取temall的url地址
    (url_list, leng) = fileread.fread('url.txt')
    if leng <= 1:
        url = str(url_list[0])
        onlyoneurl(url)
    else:
        url_more(url_list, leng)


if __name__ == "__main__":
    main()