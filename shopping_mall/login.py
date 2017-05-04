#!/usr/bin/env python
# -*- coding: utf-8 -*-


import getpass
import json

def Read_file():
    f = open('user_information.json','r+') #打开文件
    data = json.loads(f.read()) # 读取剩下的所有内容,文件大时不要用
    f.close() #关闭文件
    return data

def Wite_file(data):
    f = open('user_information.json','w+') #打开文件
    f.write(json.dumps(data))
    # f.write(data)
    f.close() #关闭文件


def user_login(login_name , login_pwd):
    data = Read_file()
    if login_name in data:
        if login_pwd == data[login_name]["password"]:
            print("Login success")
            print("data[login_name]:  %s"%data[login_name])
            return data[login_name]
        else:
            #判断是否登录三次
            if data[login_name]["login_count"] != 3:
                data[login_name]["login_count"] += 1
                # Wite_file(json.dumps(data))
                Wite_file(data)
                print("password error")
                return False
            else:
                print ("%s has inputed three times is locked"%login_name )
                return False
    else:
        print("There is no people")
        return False






