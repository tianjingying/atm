#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print("base_dir:%s" % base_dir)
sys.path.append(base_dir)
print(sys.path)
from atm.bin import atm
from atm.core import main
import login


def close_an_account(user_msg):
    '''
    结算，调用信用卡消费接口
    :return:
    '''
    total_price = 0
    if "product_record" in user_msg:
        for i in range(len(user_msg["product_record"])):
            print(user_msg["product_record"][i])
            print(user_msg["product_record"][i]["price"])
            total_price += user_msg["product_record"][i]["price"]
        print("total_price:%s" % total_price)
        if main.consume(total_price):
            user_msg["product_record"] = []
            data = login.Read_file()
            data[username] = user_msg
            login.Wite_file(data)
        else:
            print("\033[31;1mbalence is not enough!\033[0m")


def check_product(product_list, choice_product, choice_count, user_msg, username):
    '''
    函数功能：将商品放入购物车中
    参数：product_list：商品列表
          choice_product：选择的商品编号
          choice_count：选择的商品个数
          user_msg : 从用户文件中取出的用户信息
           购买商品的用户
    返回值：

    '''
    data = login.Read_file()
    data[username] = user_msg
    result = {}
    result["product_count"] = choice_count
    result["product"] = product_list[choice_product]
    result["price"] = int(choice_count) * float(result["product"][1])
    if "product_record" not in user_msg:
        user_msg["product_record"] = []
    user_msg["product_record"].append(result)
    login.Wite_file(data)
    print("已经将该商品放入购物车")


def fun_choice_shopping(product_list, username):
    print("可选的商品列表")
    for i in range(len(product_list)):
        print("%s  %s  %d" % (i, product_list[i][0], product_list[i][1]))
    print("q  返回上层")
    choice_product = input("输入要买的商品编号   ").strip()
    if not choice_product.isdigit():
        # 输入的不是数字
        if choice_product == "q":
            # 退出
            print("退出商品购买")
            return False
        else:
            print("输入错误,请重新输入")
    else:
        choice_product = int(choice_product)
        lenth = len(product_list) - 1
        if choice_product > len(product_list) - 1:
            print("该商品不存在")
        else:
            # 商品编号在商品列表中
            choice_count = input("请输入商品个数:   ").strip()
            if not choice_count.isdigit():
                print("输入不合法，请输入数字")
            else:
                check_product(product_list,
                              choice_product,
                              choice_count,
                              user_msg, username)
    return True


def funGet_consume_record(user_msg):
    # 获取消费信息
    # 参数：user_msg : 用户信息文件的内容
    #       username : 操作用户
    if "product_record" not in user_msg \
            or len(user_msg["product_record"]) == 0:
        print("购物车为空")
    else:
        for item in user_msg["product_record"]:
            print("*********************")
            print('''  
            购买商品：%s\n
            单价 ： %s\n
            商品个数：%s\n
            总价格: %s
        ''' % (item["product"][0], \
               item["product"][1], \
               item["product_count"], \
               item["price"]
               ))


# 商品列表
product_list = [
    ("iphone", 6000),
    ("bicycle", 600),
    ("notebook", 10),
    ("computer", 6000),
]
menu = u'''\033[32;1m
        1:  购买商品
        2:  查看购物车
        3:  结账
        4:  退出\033[0m
        '''
# menu_dic = {
#     '1': account_info,
#     '2': repay,
#     '3': withdraw
#
# }

# 购买的商品
if __name__ == '__main__':
    my_product_list = []
    my_product_msg = {}  # 购买商品记录，包括购买商品和总价
    username = input("Input username : ").strip()
    print(username)
    password = input("Input password: ").strip()
    user_msg = login.user_login(username, password)
    if user_msg:
        print("user_msg:%s" % user_msg)
        while True:
            print("username:%s" % username)
            print(menu)
            menu_items = input("请输入菜单序号：").strip()
            if not menu_items.isdigit():
                print("请输入数字")
                continue
            else:
                menu_items = int(menu_items)
                if menu_items == 1:
                    fun_choice_shopping(product_list, username)
                elif menu_items == 2:
                    funGet_consume_record(user_msg)
                elif menu_items == 3:
                    close_an_account(user_msg)
                else:
                    print("退出")
                    break
