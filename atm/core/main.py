#!_*_coding:utf-8_*_
# __author__:"Alex Li"

'''
main program handle module , handle all the user interaction stuff

'''

from core import auth
from core import accounts
from core import logger
from core import accounts
from core import transaction
from core.auth import login_required
import time

# transaction logger
trans_logger = logger.logger('transaction')
# access logger
access_logger = logger.logger('access')

# temp account data ,only saves the data in memory
user_data = {
    'account_id': None,
    'is_authenticated': False,  # 登陆之后为 True ，认证状态
    'account_data': None

}


@login_required
def account_info(acc_data):
    print(user_data)


@login_required
def repay(acc_data):
    '''
    print current balance and let user repay the bill
    :return:
    '''
    account_data = accounts.load_current_balance(acc_data['account_id'])
    # 再从硬盘加载一次数据， 为了确保数据是最新的
    # for k,v in account_data.items():
    #    print(k,v )
    current_balance = ''' --------- BALANCE INFO --------
        Credit :    %s
        Balance:    %s''' % (account_data['credit'], account_data['balance'])
    print(current_balance)
    repay_amount = input("\033[33;1mInput repay amount:\033[0m").strip()
    if len(repay_amount) > 0 and repay_amount.isdigit():
        new_balance = transaction.make_transaction(trans_logger, account_data, 'repay', repay_amount)
        if new_balance:
            print('''\033[42;1mNew Balance:%s\033[0m''' % (new_balance['balance']))
    else:
        print('\033[31;1m[%s] is not a valid amount, only accept integer!\033[0m' % repay_amount)


@login_required
def withdraw(acc_data):
    '''
    print current balance and let user do the withdraw action
    :param acc_data:
    :return:
    '''
    account_data = accounts.load_current_balance(acc_data['account_id'])
    current_balance = ''' --------- BALANCE INFO --------
        Credit :    %s
        Balance:    %s''' % (account_data['credit'], account_data['balance'])
    print(current_balance)
    withdraw_amount = input("\033[33;1mInput withdraw amount:\033[0m").strip()
    if len(withdraw_amount) > 0 and withdraw_amount.isdigit():
        new_balance = transaction.make_transaction(trans_logger, account_data, 'withdraw', withdraw_amount)
        if new_balance:
            print('''\033[42;1mNew Balance:%s\033[0m''' % (new_balance['balance']))

    else:
        print('\033[31;1m[%s] is not a valid amount, only accept integer!\033[0m' % withdraw_amount)


@login_required
def transfer(acc_data):
    '''
    转账
    :param acc_data:
    :return:
    '''
    print("acc_data : %s" % acc_data)
    transfer_data = {}
    transfer_data["id"] = input("\033[33;1m:请输入转入的账户\033[0m").strip()
    transfer_data["amount"] = input("\033[33;1m:请输入转账金额\033[0m").strip()
    if not transfer_data["amount"].isdigit():
        print('\033[31;1m[%s] is not a valid amount, only accept integer!\033[0m' % transfer_data["amount"])
    else:
        transfer_data["amount"] = float(transfer_data["amount"])
        # 转入的用戶信息
        account_data_in = accounts.load_current_balance(transfer_data["id"])

        if account_data_in:
            print("account_data:%s" % account_data_in)
            new_balance_out = transaction.make_transaction(
                trans_logger, acc_data["account_data"], 'transfer_out',
                transfer_data["amount"])
            if new_balance_out:
                new_balance_in = transaction.make_transaction(
                    trans_logger, account_data_in, 'transfer_in',
                    transfer_data["amount"])


def pay_check(acc_data):
    pass


def logout(acc_data):
    pass


def interactive(acc_data):
    '''
    interact with user
    :return:
    '''
    menu = u'''
    ------- Oldboy Bank ---------
    \033[32;1m1.  账户信息
    2.  还款(功能已实现)
    3.  取款(功能已实现)
    4.  转账
    5.  账单
    6.  退出
    \033[0m'''
    menu_dic = {
        '1': account_info,
        '2': repay,
        '3': withdraw,
        '4': transfer,
        '5': pay_check,
        '6': logout,
    }
    exit_flag = False
    while not exit_flag:
        print(menu)
        user_option = input(">>:").strip()
        if user_option in menu_dic:
            # print('accdata',acc_data)
            # acc_data['is_authenticated'] =False
            menu_dic[user_option](acc_data)

        else:
            print("\033[31;1mOption does not exist!\033[0m")


def run():
    '''
    this function will be called right a way when the program started, here handles the user interaction stuff
    :return:
    '''
    acc_data = auth.acc_login(user_data, access_logger)
    if user_data['is_authenticated']:
        user_data['account_data'] = acc_data
        interactive(user_data)


def create_account():
    '''
    创建账户
    :return:
    '''
    print("create_account")
    auth.create_account(access_logger)
    pass


def manage_run():
    '''
    管理员入口
    :return:
    '''
    menu = u'''
        ------- 管理员 ---------
        \033[32;1m 1.  添加账户
        2.  修改用户额度
        3.  冻结账户
        4.  退出
        \033[0m'''
    menu_dic = {
        '1': create_account,
        # '2': update_balance,
        # '3': frozen_account,
        # '4': logout,
    }
    exit_flag = False
    while not exit_flag:
        print(menu)
        user_option = input(">>:").strip()
        if user_option in menu_dic:
            menu_dic[user_option]()
            # while(True):
            #     print(menu)
