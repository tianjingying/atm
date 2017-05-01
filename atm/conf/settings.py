#!_*_coding:utf-8_*_
#__author__:"Alex Li"
import os
import sys
import logging
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


DATABASE = {
    'engine': 'file_storage', #support mysql,postgresql in the future
    'name':'accounts',
    'path': "%s/db" % BASE_DIR
}


LOG_LEVEL = logging.INFO
LOG_TYPES = {
    'transaction': 'transactions.log',
    'access': 'access.log',
}

TRANSACTION_TYPE = {
    'repay':{'action':'plus', 'interest':0.03},
    'withdraw':{'action':'minus', 'interest':0.05},
    'transfer_out':{'action':'transfer_out', 'interest':0.05},  #转出
    'transfer_in':{'action':'transfer_in', 'interest':0},  #转入
    'consume':{'action':'consume', 'interest':0},

}

EXPIRE_TIME = 10   #有效期  10年