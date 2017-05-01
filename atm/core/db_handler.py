#!_*_coding:utf-8_*_
# __author__:"Alex Li"

'''
handle all the database interactions
'''
import json, time, os
from  conf import settings


def file_db_handle(conn_params):
    '''
    parse the db file path
    :param conn_params: the db connection params set in settings
    :return:
    '''
    print('file db:', conn_params)
    # db_path ='%s/%s' %(conn_params['path'],conn_params['name'])
    return file_execute


def db_handler():
    '''
    connect to db
    :param conn_parms: the db connection params set in settings
    :return:a
    '''
    conn_params = settings.DATABASE
    if conn_params['engine'] == 'file_storage':
        return file_db_handle(conn_params)
    elif conn_params['engine'] == 'mysql':
        pass  # todo


def read_from_file(filename):
    # 读取数据文件
    # :return:
    f = open(filename, 'r+')  # 打开文件
    data = json.loads(f.read())
    f.close()  # 关闭文件
    return data


def write_to_file(filename, data):
    # 写入文件
    # :param data:
    # :return:
    f = open(filename, 'w+')  # 打开文件
    f.write(json.dumps(data))
    f.close()  # 关闭文件


def create_account_file(db_path, **kwargs):
    account_file = "%s/%s.json" % (db_path, kwargs["id"])
    print("account_file: %s" % account_file)
    write_to_file(account_file, kwargs)
    pass


def file_execute(sql, **kwargs):
    conn_params = settings.DATABASE
    db_path = '%s/%s' % (conn_params['path'], conn_params['name'])

    print(sql, db_path)
    print("kwargs:%s" % kwargs)
    if sql.find("where") >= 0:
        sql_list = sql.split("where")
        print(sql_list)
        if sql_list[0].startswith("select") and len(sql_list) > 1:  # has where clause
            column, val = sql_list[1].strip().split("=")

            if column == 'account':
                account_file = "%s/%s.json" % (db_path, val)
                print(account_file)
                if os.path.isfile(account_file):
                    with open(account_file, 'r', encoding="utf-8") as f:
                        print("f:  %s" % f)
                        account_data = json.load(f)
                        print("account_data : %s" % account_data)
                        return account_data
                else:
                    print("\033[31;1mAccount [%s] does not exist!\033[0m" % val)
                    return False

        elif sql_list[0].startswith("update") and len(sql_list) > 1:  # has where clause
            column, val = sql_list[1].strip().split("=")
            if column == 'account':
                account_file = "%s/%s.json" % (db_path, val)
                # print(account_file)
                if os.path.isfile(account_file):
                    account_data = kwargs.get("account_data")
                    with open(account_file, 'w') as f:
                        acc_data = json.dump(account_data, f)
                    return True
    elif sql.find("create account") >= 0:
        # 管理员创建用户
        create_account_file(db_path, **kwargs)
