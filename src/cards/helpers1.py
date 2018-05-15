from datetime import datetime

from django.db import transaction

from .models import Card, CardHistory, CardOperate, CardInfo, CardStatus

class NotAutoCommit:
    ''' 不使用django的自动提交 '''

    def __init__(self):
        # print('NotAutoCommit.__init__(): ...')
        # 保存django自动事务的设置
        self.old_autocommit = transaction.get_autocommit()

    def __enter__(self):
        # print('NotAutoCommit.__enter__(): ...')
        # 关闭django自动事务
        transaction.set_autocommit(False)

    def __exit__(self, exc_type, exc_val, exc_tb):
        # print('NotAutoCommit.__exit__(): ...')
        # 恢复django自动事务的设置
        transaction.set_autocommit(self.old_autocommit)

def open_account(num, name, phone, email, money):
    '''开户'''
    with NotAutoCommit():
        try:
            try:
                operator = CardOperate.objects.get(name='开户')
            except CardOperate.DoesNotExist:
                msg = '操作类型不存在. operator_type: {}'.format(operator)
                raise ValueError(msg)
            card = Card()
            data_old = card.to_json()
            card.id = num
            card.balance = money
            card.balance_available = money
            card.balance_freeze = 0
            card.status = CardStatus.objects.get(id=1)
            card.save()
            data_new = card.to_json()

            cardinfo = CardInfo.createcardinfo(name, phone, email, card)
            cardinfo.save()

            remark = '''
                                时间：{time},
                                发生金额：{money},
                                业务发生前的数据：{data_old},
                                业务发生后的数据：{data_new},
                            '''.format(
                time=datetime.now(),
                money=money,
                data_old=data_old,
                data_new=data_new,

            )
            # raise ValueError('调试')

            cardhistory = CardHistory.createcardhistory(card, remark, operator)
            cardhistory.save()

            # 数据提交
            transaction.commit()
            print('数据提交!')
        except Exception as e:
            # 数据回滚
            msg = '未知错误. e: {}'.format(e)
            transaction.rollback()
            print(msg)

def delete_account(card):
    '''销户'''
    with NotAutoCommit():
        try:
            status = card.status.name
            if status == '正常':
                try:
                    operator = CardOperate.objects.get(name='销户')
                except CardOperate.DoesNotExist:
                    msg = '操作类型不存在. operator_type: {}'.format(operator)
                    raise ValueError(msg)
                money = card.balance
                data_old = card.to_json()
                card.balance = 0
                card.balance_available = 0
                card.status = "销户"
                card.save()

                data_new = card.to_json()

                # remark = "时间：" + str(time) + "\n" + "存款：" + str(money) + "元\n" "前金额：" + str(pre_balance) + "元\n" "后金额：" + str(card.balance) + "元\n" "状态：" + str(status)
                remark = '''
                                   时间：{time},
                                   发生金额：{money},
                                   业务发生前的数据：{data_old},
                                   业务发生后的数据：{data_new},
                               '''.format(
                    time=datetime.now(),
                    money=money,
                    data_old=data_old,
                    data_new=data_new,

                )

                # raise ValueError('调试')

                cardhistory = CardHistory.createcardhistory(card, remark, operator)
                cardhistory.save()

                # 数据提交
                transaction.commit()
                print('数据提交!')

            else:
                msg = "银行卡状态错误.status:{}".format(card.status.name)
                raise ValueError(msg)

        except Exception as e:
            # 数据回滚
            msg = '未知错误. e: {}'.format(e)
            transaction.rollback()
            print(msg)

def modify_account(card, name, phone, email):
    '''修改账号信息'''
    with NotAutoCommit():
        try:
            status = card.status.name
            if status == '正常':
                try:
                    operator = CardOperate.objects.get(name='修改账号信息')
                except CardOperate.DoesNotExist:
                    msg = '操作类型不存在. operator_type: {}'.format(operator)
                    raise ValueError(msg)

                data_old = card.to_json()
                card.name = name
                card.phone = phone
                card.email = email
                card.save()
                data_new = card.to_json()

                cardinfo = CardInfo.createcardinfo(name, phone, email, card)
                cardinfo.save()

                remark = '''
                                    时间：{time},
                                    发生金额：{money},
                                    业务发生前的数据：{data_old},
                                    业务发生后的数据：{data_new},
                                '''.format(
                    time=datetime.now(),
                    money=0,
                    data_old=data_old,
                    data_new=data_new,

                )
                # raise ValueError('调试')

                cardhistory = CardHistory.createcardhistory(card, remark, operator)
                cardhistory.save()

                # 数据提交
                transaction.commit()
                print('数据提交!')
            else:
                msg = "银行卡状态错误.status:{}".format(card.status.name)
                raise ValueError(msg)
        except Exception as e:
            # 数据回滚
            msg = '未知错误. e: {}'.format(e)
            transaction.rollback()
            print(msg)

def put_money(card, money):
    '''存款'''
    with NotAutoCommit():
        try:
            status = card.status.name
            if status == '正常':
                try:
                    operator = CardOperate.objects.get(name='存款')
                except CardOperate.DoesNotExist:
                    msg = '操作类型不存在. operator_type: {}'.format(operator)
                    raise ValueError(msg)

                data_old = card.to_json()

                pre_balance = card.balance
                card.balance = pre_balance + int(money)
                card.balance_available += int(money)
                card.save()

                data_new = card.to_json()

                #remark = "时间：" + str(time) + "\n" + "存款：" + str(money) + "元\n" "前金额：" + str(pre_balance) + "元\n" "后金额：" + str(card.balance) + "元\n" "状态：" + str(status)
                remark = '''
                    时间：{time},
                    发生金额：{money},
                    业务发生前的数据：{data_old},
                    业务发生后的数据：{data_new},
                '''.format(
                    time=datetime.now(),
                    money=money,
                    data_old=data_old,
                    data_new=data_new,

                )

                # raise ValueError('调试')

                cardhistory = CardHistory.createcardhistory(card, remark, operator)
                cardhistory.save()

                # 数据提交
                transaction.commit()
                print('数据提交!')

            else:
                msg = "银行卡状态错误.status:{}".format(card.status.name)
                raise ValueError(msg)
        except Exception as e:
            # 数据回滚
            msg = '未知错误. e: {}'.format(e)
            transaction.rollback()
            print(msg)

def put_money_2(card, money):
    '''存款'''
    # 保存django自动事务的设置
    old_autocommit = transaction.get_autocommit()
    try:
        # 关闭django自动事务
        transaction.set_autocommit(False)

        status = card.status.name
        if status == '正常':
            try:
                operator = CardOperate.objects.get(name='存款')
            except CardOperate.DoesNotExist:
                msg = '操作类型不存在. operator_type: {}'.format(operator)
                raise ValueError(msg)

            data_old = card.to_json()

            pre_balance = card.balance
            card.balance = pre_balance + int(money)
            card.balance_available += int(money)
            card.save()

            data_new = card.to_json()

            #remark = "时间：" + str(time) + "\n" + "存款：" + str(money) + "元\n" "前金额：" + str(pre_balance) + "元\n" "后金额：" + str(card.balance) + "元\n" "状态：" + str(status)
            remark = '''
                时间：{time},
                发生金额：{money},
                业务发生前的数据：{data_old},
                业务发生后的数据：{data_new},
            '''.format(
                time=datetime.now(),
                money=money,
                data_old=data_old,
                data_new=data_new,

            )

            raise ValueError('调试')

            cardhistory = CardHistory.createcardhistory(card, remark, operator)
            cardhistory.save()

            # 数据提交
            transaction.commit()

        else:
            msg = "银行卡状态错误.status:{}".format(card.status.name)
            raise ValueError(msg)
    except Exception as e:
        # 数据回滚
        msg = '未知错误. e: {}'.format(e)
        transaction.rollback()
        print(msg)
    finally:
        # 恢复django自动事务的设置
        transaction.set_autocommit(old_autocommit)

def draw_money(card, money):
    '''取款'''
    with NotAutoCommit():
        try:
            status = card.status.name
            if status == '正常':
                try:
                    operator = CardOperate.objects.get(name='取款')
                except CardOperate.DoesNotExist:
                    msg = '操作类型不存在. operator_type: {}'.format(operator)
                    raise ValueError(msg)

                if card.balance >= money:

                    data_old = card.to_json()

                    card.balance -= int(money)
                    card.balance_available -= int(money)
                    card.save()

                    data_new = card.to_json()

                    remark = '''
                                        时间：{time},
                                        发生金额：{money},
                                        业务发生前的数据：{data_old},
                                        业务发生后的数据：{data_new},
                                    '''.format(
                        time=datetime.now(),
                        money=money,
                        data_old=data_old,
                        data_new=data_new,

                    )

                    # raise ValueError('调试')

                    cardhistory = CardHistory.createcardhistory(card, remark, operator)
                    cardhistory.save()

                    # 数据提交
                    transaction.commit()
                    print('数据提交!')

                else:
                    return "金额不足 ： " .format(card.balance)
            else:
                msg = "银行卡状态错误.status:{}".format(card.status.name)
                raise ValueError(msg)
        except Exception as e:
            # 数据回滚
            msg = '未知错误. e: {}'.format(e)
            transaction.rollback()
            print(msg)

def tansfer(card1, card2, money):
    '''转账'''

    with NotAutoCommit():
        try:
            status = card1.status.name
            if status == '正常':
                try:
                    operator = CardOperate.objects.get(name='取款')
                except CardOperate.DoesNotExist:
                    msg = '操作类型不存在. operator_type: {}'.format(operator)
                    raise ValueError(msg)

                if card1.balance >= money:

                    data_old = card1.to_json()

                    card1.balance -= int(money)
                    card1.balance_available -= int(money)
                    card1.save()

                    data_new = card1.to_json()

                    remark = '''
                                        时间：{time},
                                        发生金额：{money},
                                        业务发生前的数据：{data_old},
                                        业务发生后的数据：{data_new},
                                    '''.format(
                        time=datetime.now(),
                        money=money,
                        data_old=data_old,
                        data_new=data_new,

                    )

                    # raise ValueError('调试')

                    cardhistory = CardHistory.createcardhistory(card1, remark, operator)
                    cardhistory.save()

                    # 数据提交
                    transaction.commit()
                    print('数据提交!')

                else:
                    return "金额不足 ： " .format(card1.balance)
            else:
                msg = "银行卡状态错误.status:{}".format(card1.status.name)
                raise ValueError(msg)
        except Exception as e:
            # 数据回滚
            msg = '未知错误. e: {}'.format(e)
            transaction.rollback()
            print(msg)

    with NotAutoCommit():
        try:
            status = card2.status.name
            if status == '正常':
                try:
                    operator = CardOperate.objects.get(name='存款')
                except CardOperate.DoesNotExist:
                    msg = '操作类型不存在. operator_type: {}'.format(operator)
                    raise ValueError(msg)

                data_old = card2.to_json()

                pre_balance = card2.balance
                card2.balance = pre_balance + int(money)
                card2.balance_available += int(money)
                card2.save()

                data_new = card2.to_json()

                #remark = "时间：" + str(time) + "\n" + "存款：" + str(money) + "元\n" "前金额：" + str(pre_balance) + "元\n" "后金额：" + str(card.balance) + "元\n" "状态：" + str(status)
                remark = '''
                    时间：{time},
                    发生金额：{money},
                    业务发生前的数据：{data_old},
                    业务发生后的数据：{data_new},
                '''.format(
                    time=datetime.now(),
                    money=money,
                    data_old=data_old,
                    data_new=data_new,

                )

                # raise ValueError('调试')

                cardhistory = CardHistory.createcardhistory(card2, remark, operator)
                cardhistory.save()

                # 数据提交
                transaction.commit()
                print('数据提交!')

            else:
                msg = "银行卡状态错误.status:{}".format(card2.status.name)
                raise ValueError(msg)
        except Exception as e:
            # 数据回滚
            msg = '未知错误. e: {}'.format(e)
            transaction.rollback()
            print(msg)

def freeze(card):
    '''冻结'''
    with NotAutoCommit():
        try:
            status = card.status.name
            if status == '正常':
                try:
                    operator = CardOperate.objects.get(name='冻结')
                except CardOperate.DoesNotExist:
                    msg = '操作类型不存在. operator_type: {}'.format(operator)
                    raise ValueError(msg)

                data_old = card.to_json()

                card.status = "冻结"
                card.save()

                data_new = card.to_json()

                # remark = "时间：" + str(time) + "\n" + "存款：" + str(money) + "元\n" "前金额：" + str(pre_balance) + "元\n" "后金额：" + str(card.balance) + "元\n" "状态：" + str(status)
                remark = '''
                                时间：{time},
                                发生金额：{money},
                                业务发生前的数据：{data_old},
                                业务发生后的数据：{data_new},
                            '''.format(
                    time=datetime.now(),
                    money=0,
                    data_old=data_old,
                    data_new=data_new,

                )

                # raise ValueError('调试')

                cardhistory = CardHistory.createcardhistory(card, remark, operator)
                cardhistory.save()

                # 数据提交
                transaction.commit()
                print('数据提交!')

            else:
                msg = "银行卡状态错误.status:{}".format(card.status.name)
                raise ValueError(msg)

        except Exception as e:
            # 数据回滚
            msg = '未知错误. e: {}'.format(e)
            transaction.rollback()
            print(msg)

def open_freeze(card):
    '''解冻'''
    with NotAutoCommit():
        try:
            status = card.status.name
            if status == '冻结':
                try:
                    operator = CardOperate.objects.get(name='解冻')
                except CardOperate.DoesNotExist:
                    msg = '操作类型不存在. operator_type: {}'.format(operator)
                    raise ValueError(msg)

                data_old = card.to_json()

                card.status = "正常"
                card.save()

                data_new = card.to_json()

                # remark = "时间：" + str(time) + "\n" + "存款：" + str(money) + "元\n" "前金额：" + str(pre_balance) + "元\n" "后金额：" + str(card.balance) + "元\n" "状态：" + str(status)
                remark = '''
                                时间：{time},
                                发生金额：{money},
                                业务发生前的数据：{data_old},
                                业务发生后的数据：{data_new},
                            '''.format(
                    time=datetime.now(),
                    money=0,
                    data_old=data_old,
                    data_new=data_new,

                )

                # raise ValueError('调试')

                cardhistory = CardHistory.createcardhistory(card, remark, operator)
                cardhistory.save()

                # 数据提交
                transaction.commit()
                print('数据提交!')

            else:
                msg = "银行卡状态错误.status:{}".format(card.status.name)
                raise ValueError(msg)

        except Exception as e:
            # 数据回滚
            msg = '未知错误. e: {}'.format(e)
            transaction.rollback()
            print(msg)

def loss(card):
    '''挂失'''
    with NotAutoCommit():
        try:
            status = card.status.name
            if status == '正常':
                try:
                    operator = CardOperate.objects.get(name='挂失')
                except CardOperate.DoesNotExist:
                    msg = '操作类型不存在. operator_type: {}'.format(operator)
                    raise ValueError(msg)

                data_old = card.to_json()

                card.status = "挂失"
                card.save()

                data_new = card.to_json()

                # remark = "时间：" + str(time) + "\n" + "存款：" + str(money) + "元\n" "前金额：" + str(pre_balance) + "元\n" "后金额：" + str(card.balance) + "元\n" "状态：" + str(status)
                remark = '''
                                时间：{time},
                                发生金额：{money},
                                业务发生前的数据：{data_old},
                                业务发生后的数据：{data_new},
                            '''.format(
                    time=datetime.now(),
                    money=0,
                    data_old=data_old,
                    data_new=data_new,

                )

                # raise ValueError('调试')

                cardhistory = CardHistory.createcardhistory(card, remark, operator)
                cardhistory.save()

                # 数据提交
                transaction.commit()
                print('数据提交!')

            else:
                msg = "银行卡状态错误.status:{}".format(card.status.name)
                raise ValueError(msg)

        except Exception as e:
            # 数据回滚
            msg = '未知错误. e: {}'.format(e)
            transaction.rollback()
            print(msg)




























