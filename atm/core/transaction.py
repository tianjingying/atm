#!_*_coding:utf-8_*_

from conf import settings
from core import accounts


# transaction logger

def operation_plus(old_balance, interest, amount):
    new_balance = old_balance + amount + interest
    return new_balance


def operation_minus(old_balance, interest, amount):
    new_balance = old_balance - amount - interest
    # check credit
    if new_balance < 0:
        print('''\033[31;1mYour balance is not enough for this transaction \033[0m''')
        return None
    else:
        return new_balance


def make_transaction(log_obj, account_data, tran_type, amount, **others):
    '''
    deal all the user transactions
    :param account_data: user account data
    :param tran_type: transaction type
    :param amount: transaction amount
    :param others: mainly for logging usage
    :return:
    '''
    amount = float(amount)
    if tran_type in settings.TRANSACTION_TYPE:
        interest = amount * settings.TRANSACTION_TYPE[tran_type]['interest']
        old_balance = float(account_data['balance'])
        if settings.TRANSACTION_TYPE[tran_type]['action'] == 'plus':
            new_balance = operation_plus(old_balance, interest, amount)
        elif settings.TRANSACTION_TYPE[tran_type]['action'] == 'minus':
            new_balance = operation_minus(old_balance, interest, amount)
        elif settings.TRANSACTION_TYPE[tran_type]['action'] == 'transfer_in':
            new_balance = operation_plus(old_balance, interest, amount)
        elif settings.TRANSACTION_TYPE[tran_type]['action'] == 'transfer_out':
            new_balance = operation_minus(old_balance, interest, amount)
        elif settings.TRANSACTION_TYPE[tran_type]['action'] == 'consume':
            new_balance = operation_minus(old_balance, interest, amount)

        if new_balance:
            account_data['balance'] = new_balance
            accounts.dump_account(account_data)  # save the new balance back to file
            log_obj.info("account:%s   action:%s    amount:%s   interest:%s" %
                         (account_data['id'], tran_type, amount, interest))
            return account_data
        else:
            return None
    else:
        print("\033[31;1mTransaction type [%s] is not exist!\033[0m" % tran_type)
        return None
