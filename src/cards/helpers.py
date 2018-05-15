# -*- encoding: utf-8 -*-

# python apps
import datetime
import time

# django apps
from django.db import transaction

# our apps
from .models import Card, CardHistory, CardOperateType, CardStatus, CardInfo


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


def put_money(card, money):
    ''' 存款

    :param card: 银行卡
    :type card: Card
    :param money: 发生金额
    :type money: int
    :return: None or Exception
    '''
    pass
    print('put_money(): ...{}\n\t函数执行前，django自动事务: {}'.format(
        datetime.datetime.now().isoformat(), transaction.get_autocommit()
        ))
    s_status = '正常'
    s_operator_type = '存款'

    with NotAutoCommit():
        # print('django自动事务: {}'.format(transaction.get_autocommit()))
        try:
            # print('休眠30秒 ... {}'.format(datetime.datetime.now().isoformat()))
            # time.sleep(30)
            if card.status.name == s_status:
                try:
                    operator_type = CardOperateType.objects.get(name=s_operator_type)
                except CardOperateType.DoesNotExist:
                    msg = '操作类型不存在. operator_type: {}'.format(s_operator_type)
                    raise ValueError(msg)

                # 业务发生前的数据
                data_old = card.to_json()
                # 存钱
                card.balance += money
                card.balance_available += money
                card.save()
                # 业务发生后的数据
                data_new = card.to_json()
                # 写流水帐
                remark = '''
                时间：{now},
                发生金额：{money},
                业务发生前的数据：{data_old},
                业务发生后的数据：{data_new},
                '''.format(
                    now=datetime.datetime.now().isoformat(),
                    money=money,
                    data_old=data_old,
                    data_new=data_new,
                )

                # raise ValueError('调试')

                obj = CardHistory(
                    card=card,
                    operator_type=operator_type,
                    remark=remark,
                )
                obj.save()

                # print('数据提交之前 ... {}'.format(datetime.datetime.now().isoformat()))
                # 数据提交
                transaction.commit()
                # print('数据提交之后 ... {}'.format(datetime.datetime.now().isoformat()))
            else:
                msg = '银行卡的状态错误. status: {}'.format(card.status.name)
                raise ValueError(msg)
        except Exception as e:
            # 数据回滚
            msg = '未知错误. e: {}'.format(e)
            transaction.rollback()
            # print('数据回滚 ... {}'.format(datetime.datetime.now().isoformat()))
            raise ValueError(msg)
    # print('\t函数返回前，django自动事务: {}'.format(transaction.get_autocommit()))


def put_money_2(card, money):
    ''' 存款

    :param card: 银行卡
    :type card: Card
    :param money: 发生金额
    :type money: int
    :return: None or Exception
    '''
    pass
    s_status = '正常'
    s_operator_type = '存款'

    # 保存django自动事务的设置
    old_autocommit = transaction.get_autocommit()
    try:
        # 关闭django自动事务
        transaction.set_autocommit(False)

        if card.status.name == s_status:
            try:
                operator_type = CardOperateType.objects.get(name=s_operator_type)
            except CardOperateType.DoesNotExist:
                msg = '操作类型不存在. operator_type: {}'.format(s_operator_type)
                raise ValueError(msg)

            # 业务发生前的数据
            data_old = card.to_json()
            # 存钱
            card.balance += money
            card.balance_available += money
            card.save()
            # 业务发生后的数据
            data_new = card.to_json()
            # 写流水帐
            remark = '''
            时间：{now},
            发生金额：{money},
            业务发生前的数据：{data_old},
            业务发生后的数据：{data_new},
            '''.format(
                now=datetime.datetime.now().isoformat(),
                money=money,
                data_old=data_old,
                data_new=data_new,
            )

            # raise ValueError('调试')

            obj = CardHistory(
                card=card,
                operator_type=operator_type,
                remark=remark,
            )
            obj.save()

            # 数据提交
            transaction.commit()
            print('数据提交!')
        else:
            msg = '银行卡的状态错误. status: {}'.format(card.status.name)
            raise ValueError(msg)
    except Exception as e:
        # 数据回滚
        msg = '未知错误. e: {}'.format(e)
        transaction.rollback()
        raise ValueError(msg)
    finally:
        # 恢复django自动事务的设置
        transaction.set_autocommit(old_autocommit)
        print('恢复django自动设置的设置')


def put_money_v3_1(card, money):
    ''' 存款

    :param card: 银行卡
    :type card: Card
    :param money: 发生金额
    :type money: int
    :return: None or Exception
    '''
    s_status = '正常'
    s_operator_type = '存款'

    if card.status.name == s_status:
        try:
            operator_type = CardOperateType.objects.get(name=s_operator_type)
        except CardOperateType.DoesNotExist:
            msg = '操作类型不存在. operator_type: {}'.format(s_operator_type)
            raise ValueError(msg)

        # 业务发生前的数据
        data_old = card.to_json()
        # 存钱
        card.balance += money
        card.balance_available += money
        card.save()
        # 业务发生后的数据
        data_new = card.to_json()
        # 写流水帐
        remark = '''
        时间：{now},
        发生金额：{money},
        业务发生前的数据：{data_old},
        业务发生后的数据：{data_new},
        '''.format(
            now=datetime.datetime.now().isoformat(),
            money=money,
            data_old=data_old,
            data_new=data_new,
        )

        # raise ValueError('调试')

        obj = CardHistory(
            card=card,
            operator_type=operator_type,
            remark=remark,
        )
        obj.save()

        # print('数据提交之后 ... {}'.format(datetime.datetime.now().isoformat()))
    else:
        msg = '银行卡的状态错误. status: {}'.format(card.status.name)
        raise ValueError(msg)
 

def put_money_v3(card, money):
    ''' 存款
    使用django推荐的transaction.atomic().

    :param card: 银行卡
    :type card: Card
    :param money: 发生金额
    :type money: int
    :return: None or Exception
    '''
    with transaction.atomic():
        put_money_v3_1(card, money)


def get_money(card, money):
    ''' 取款

    :param card: 银行卡
    :type card: Card
    :param money: 发生金额
    :type money: int
    :return: None or Exception
    '''
    s_status = '正常'
    s_operator_type = '取款'

    with NotAutoCommit():
        try:
            # 检查银行卡状态
            check_CardStatus(card, s_status)

            # 检查余额
            if card.balance < money:
                msg = '余额不足'
                raise ValueError(msg)
            elif card.balance_available < money:
                msg = '可用余额不足'
                raise ValueError(msg)

            # 取银行卡的操作类型
            operator_type = get_CardOperateType(s_operator_type)

            # 业务发生前的数据
            data_old = card.to_json()
            # 取款
            card.balance -= money
            card.balance_available -= money
            card.save()
            # 业务发生后的数据
            data_new = card.to_json()

            # 写流水帐
            remark = '''
            时间：{now},
            发生金额：{money},
            业务发生前的数据：{data_old},
            业务发生后的数据：{data_new},
            '''.format(
                now=datetime.datetime.now().isoformat(),
                money=money,
                data_old=data_old,
                data_new=data_new,
            )

            # raise ValueError('调试')

            obj = CardHistory(
                card=card,
                operator_type=operator_type,
                remark=remark,
            )
            obj.save()

            # 数据提交
            transaction.commit()
        except Exception as e:
            # 数据回滚
            msg = '未知错误. e: {}'.format(e)
            transaction.rollback()
            raise ValueError(msg)


def get_money_v2_1(card, money):
    ''' 取款

    :param card: 银行卡
    :type card: Card
    :param money: 发生金额
    :type money: int
    :return: None or Exception
    '''
    s_status = '正常'
    s_operator_type = '取款'

    # 检查银行卡状态
    check_CardStatus(card, s_status)

    # 检查余额
    if card.balance < money:
        msg = '余额不足'
        raise ValueError(msg)
    elif card.balance_available < money:
        msg = '可用余额不足'
        raise ValueError(msg)

    # 取银行卡的操作类型
    operator_type = get_CardOperateType(s_operator_type)

    # 业务发生前的数据
    data_old = card.to_json()
    # 取款
    card.balance -= money
    card.balance_available -= money
    card.save()
    # 业务发生后的数据
    data_new = card.to_json()

    # 写流水帐
    remark = '''
    时间：{now},
    发生金额：{money},
    业务发生前的数据：{data_old},
    业务发生后的数据：{data_new},
    '''.format(
        now=datetime.datetime.now().isoformat(),
        money=money,
        data_old=data_old,
        data_new=data_new,
    )

    # raise ValueError('调试')

    obj = CardHistory(
        card=card,
        operator_type=operator_type,
        remark=remark,
    )
    obj.save()


def get_money_v2(card, money):
    ''' 取款
    使用django推荐的transaction.atomic().

    :param card: 银行卡
    :type card: Card
    :param money: 发生金额
    :type money: int
    :return: None or Exception
    '''
    with transaction.atomic():
        get_money_v2_1(card, money)


def check_CardStatus(card, status):
    ''' 检查银行卡的状态

    :param card: 银行卡
    :type card: Card
    :param status: 银行卡的状态
    :type status: str or CartStatus
    :return: None or ValueError
    '''
    if not isinstance(card, Card):
        msg = '参数错误. card: {}'.format(card)
        raise ValueError(msg)

    if isinstance(status, CardStatus):
        status = status.name
    elif not isinstance(status, str):
        msg = '参数错误. status: {}'.format(status)
        raise ValueError(msg)

    if card.status.name != status:
        msg = '银行卡的状态错误. status: {}'.format(card.status.name)
        raise ValueError(msg)


def get_CardOperateType(s_operator_type):
    ''' 取银行卡的操作类型

    :param s_operator_type: 银行卡的操作类型
    :type s_operator_type: str
    :return: CardOperateType or ValueError
    '''
    # print('get_CardOperateType(): ...\n\ts_operator_type: {}'.format(s_operator_type))
    try:
        operator_type = CardOperateType.objects.get(name=s_operator_type)
    except CardOperateType.DoesNotExist:
        msg = '操作类型不存在. operator_type: {}'.format(s_operator_type)
        raise ValueError(msg)
    # print('operator_type: {}'.format(operator_type))
    return operator_type


def credit_transfer_v1(card_from, card_to, money):
    ''' 转账

    :param card_from: 转出银行卡
    :type card_from: Card
    :param card_to: 转入银行卡
    :type card_to: Card
    :param money: 发生金额
    :type money: int
    :return: None or ValueError
    '''
    pass

    get_money(card_from, money)
    put_money(card_to, money)


def credit_transfer_v2(card_from, card_to, money):
    ''' 转账

    :param card_from: 转出银行卡
    :type card_from: Card
    :param card_to: 转入银行卡
    :type card_to: Card
    :param money: 发生金额
    :type money: int
    :return: None or ValueError
    '''
    s_status = '正常'
    s_operator_type = '转账'

    # 检查银行卡状态
    check_CardStatus(card_from, s_status)
    check_CardStatus(card_to, s_status)

    # 检查余额
    if card_from.balance < money:
        msg = '余额不足'
        raise ValueError(msg)
    elif card_from.balance_available < money:
        msg = '可用余额不足'
        raise ValueError(msg)

    # 取银行卡的操作类型
    operator_type = get_CardOperateType(s_operator_type)

    ''' 取款 '''
    # 业务发生前的数据
    data_old = card_from.to_json()
    # 取款
    card_from.balance -= money
    card_from.balance_available -= money
    card_from.save()
    # 业务发生后的数据
    data_new = card_from.to_json()

    # 写流水帐
    remark = '''
    时间：{now},
    业务类型：{operator_type}--转出,
    发生金额：{money},
    业务发生前的数据：{data_old},
    业务发生后的数据：{data_new},
    收款银行卡：{card_to},
    '''.format(
        now=datetime.datetime.now().isoformat(),
        operator_type=s_operator_type,
        money=money,
        data_old=data_old,
        data_new=data_new,
        card_to=card_to.id,
    )
    obj = CardHistory(
        card=card_from,
        operator_type=operator_type,
        remark=remark,
    )
    obj.save()

    ''' 存款 '''
    # 业务发生前的数据
    data_old = card_to.to_json()
    # 存钱
    card_to.balance += money
    card_to.balance_available += money
    card_to.save()
    # 业务发生后的数据
    data_new = card_to.to_json()
    # 写流水帐
    remark = '''
    时间：{now},
    业务类型：{operator_type}--转入,
    发生金额：{money},
    业务发生前的数据：{data_old},
    业务发生后的数据：{data_new},
    付款银行卡：{card_from},
    '''.format(
        now=datetime.datetime.now().isoformat(),
        operator_type=s_operator_type,
        money=money,
        data_old=data_old,
        data_new=data_new,
        card_from=card_from.id,
    )

    obj = CardHistory(
        card=card_to,
        operator_type=operator_type,
        remark=remark,
    )
    obj.save()

    # raise ValueError('调试')


def credit_transfer_v3_1(
        card_from, card_to, money, s_status, s_operator_type,
        ):
    ''' 转账的主题

    :param card_from: 转出银行卡
    :type card_from: Card
    :param card_to: 转入银行卡
    :type card_to: Card
    :param money: 发生金额
    :type money: int
    :param s_status: 银行卡状态
    :type s_status: str
    :param s_operator_type: 银行卡操作的类型
    :type s_operator_type: str
    :return: None or ValueError
    '''

    # 检查银行卡状态
    check_CardStatus(card_from, s_status)
    check_CardStatus(card_to, s_status)

    # 检查余额
    if card_from.balance < money:
        msg = '余额不足'
        raise ValueError(msg)
    elif card_from.balance_available < money:
        msg = '可用余额不足'
        raise ValueError(msg)

    # 取银行卡的操作类型
    operator_type = get_CardOperateType(s_operator_type)

    ''' 取款 '''
    # 业务发生前的数据
    data_old = card_from.to_json()
    # 取款
    card_from.balance -= money
    card_from.balance_available -= money
    card_from.save()
    # 业务发生后的数据
    data_new = card_from.to_json()

    # 写流水帐
    remark = '''
            时间：{now},
            业务类型：{operator_type}--转出,
            发生金额：{money},
            业务发生前的数据：{data_old},
            业务发生后的数据：{data_new},
            收款银行卡：{card_to},
            '''.format(
                    now=datetime.datetime.now().isoformat(),
                    operator_type=s_operator_type,
                    money=money,
                    data_old=data_old,
                    data_new=data_new,
                    card_to=card_to.id,
                    )
    obj = CardHistory(
        card=card_from,
        operator_type=operator_type,
        remark=remark,
    )
    obj.save()

    raise ValueError('调试')

    ''' 存款 '''
    # 业务发生前的数据
    data_old = card_to.to_json()
    # 存钱
    card_to.balance += money
    card_to.balance_available += money
    card_to.save()
    # 业务发生后的数据
    data_new = card_to.to_json()
    # 写流水帐
    remark = '''
            时间：{now},
            业务类型：{operator_type}--转入,
            发生金额：{money},
            业务发生前的数据：{data_old},
            业务发生后的数据：{data_new},
            付款银行卡：{card_from},
            '''.format(
                    now=datetime.datetime.now().isoformat(),
                    operator_type=s_operator_type,
                    money=money,
                    data_old=data_old,
                    data_new=data_new,
                    card_from=card_from.id,
                    )

    obj = CardHistory(
        card=card_to,
        operator_type=operator_type,
        remark=remark,
    )
    obj.save()


def credit_transfer_v3(card_from, card_to, money):
    ''' 转账

    :param card_from: 转出银行卡
    :type card_from: Card
    :param card_to: 转入银行卡
    :type card_to: Card
    :param money: 发生金额
    :type money: int
    :return: None or ValueError
    '''
    s_status = '正常'
    s_operator_type = '转账'

    with NotAutoCommit():
        try:
            credit_transfer_v3_1(
                    card_from, card_to, money, s_status, s_operator_type,
                    )
        except Exception as e:
            # 数据回滚
            msg = '未知错误. e: {}'.format(e)
            transaction.rollback()
            raise ValueError(msg)


def credit_transfer_v4(card_from, card_to, money):
    ''' 转账

    :param card_from: 转出银行卡
    :type card_from: Card
    :param card_to: 转入银行卡
    :type card_to: Card
    :param money: 发生金额
    :type money: int
    :return: None or ValueError
    '''
    with transaction.atomic():
        credit_transfer_v2(card_from, card_to, money)

def open_account_v1(name, phone, email):
    ''' 开户

    :param name: 姓名
    :type name: str
    :param phone: 电话
    :type phone: str
    :param email: 电子信箱
    :type email: str
    :return: Card
    '''
    pass
    s_operator_type = '开户'
    s_status = '正常'

    try:
        status = CardStatus.objects.get(name=s_status)
    except CardStatus.DoesNotExist:
        msg = '状态不存在. status: {}'.format(s_status)
        raise ValueError(msg)

    try:
        operator_type = CardOperateType.objects.get(name=s_operator_type)
    except CardOperateType.DoesNotExist:
        msg = '操作类型不存在. operator_type: {}'.format(s_operator_type)
        raise ValueError(msg)


    ''' 开银行卡 '''
    # 业务发生前的数据
    data_old = None
    # 开银行卡
    card = Card(status=status)
    card.save()
    # 业务发生后的数据
    data_new = card.to_json()
    # 写流水帐
    remark = '''
    时间：{now},
    业务类型：{operator_type},
    发生金额：{money},
    业务发生前的数据：{data_old},
    业务发生后的数据：{data_new},
    '''.format(
        now=datetime.datetime.now().isoformat(),
        operator_type=s_operator_type,
        money=0,
        data_old=data_old,
        data_new=data_new,
    )

    # raise ValueError('调试')

    obj = CardHistory(
        card=card,
        operator_type=operator_type,
        remark=remark,
    )
    obj.save()


    ''' 开用户信息 '''
    # 业务发生前的数据
    data_old = None
    # 开用户信息
    card_info = CardInfo(
            name=name,
            phone=phone,
            email=email,
            card=card,
            )
    card_info.save()
    # 业务发生后的数据
    data_new = card_info.to_json()
    # 写流水帐
    remark = '''
    时间：{now},
    业务类型：{operator_type},
    发生金额：{money},
    业务发生前的数据：{data_old},
    业务发生后的数据：{data_new},
    '''.format(
        now=datetime.datetime.now().isoformat(),
        operator_type=s_operator_type,
        money=0,
        data_old=data_old,
        data_new=data_new,
    )

    obj = CardHistory(
        card=card,
        operator_type=operator_type,
        remark=remark,
    )
    obj.save()

    return card


def open_account_v2_1(name, phone, email, s_status, s_operator_type):
    ''' 开户

    :param name: 姓名
    :type name: str
    :param phone: 电话
    :type phone: str
    :param email: 电子信箱
    :type email: str
    :return: Card
    '''
    pass
    try:
        status = CardStatus.objects.get(name=s_status)
    except CardStatus.DoesNotExist:
        msg = '状态不存在. status: {}'.format(s_status)
        raise ValueError(msg)

    try:
        operator_type = CardOperateType.objects.get(name=s_operator_type)
    except CardOperateType.DoesNotExist:
        msg = '操作类型不存在. operator_type: {}'.format(s_operator_type)
        raise ValueError(msg)

    ''' 开银行卡 '''
    # 业务发生前的数据
    data_old = None
    # 开银行卡
    card = Card(status=status)
    card.save()
    # 业务发生后的数据
    data_new = card.to_json()
    # 写流水帐
    remark = '''
    时间：{now},
    业务类型：{operator_type},
    发生金额：{money},
    业务发生前的数据：{data_old},
    业务发生后的数据：{data_new},
    '''.format(
        now=datetime.datetime.now().isoformat(),
        operator_type=s_operator_type,
        money=0,
        data_old=data_old,
        data_new=data_new,
    )

    obj = CardHistory(
        card=card,
        operator_type=operator_type,
        remark=remark,
    )
    obj.save()

    # raise ValueError('调试')

    ''' 开用户信息 '''
    # 业务发生前的数据
    data_old = None
    # 开用户信息
    card_info = CardInfo(
            name=name,
            phone=phone,
            email=email,
            card=card,
            )
    card_info.save()
    # 业务发生后的数据
    data_new = card_info.to_json()
    # 写流水帐
    remark = '''
    时间：{now},
    业务类型：{operator_type},
    发生金额：{money},
    业务发生前的数据：{data_old},
    业务发生后的数据：{data_new},
    '''.format(
        now=datetime.datetime.now().isoformat(),
        operator_type=s_operator_type,
        money=0,
        data_old=data_old,
        data_new=data_new,
    )

    obj = CardHistory(
        card=card,
        operator_type=operator_type,
        remark=remark,
    )
    obj.save()

    return card


def open_account_v2(name, phone, email):
    ''' 开户 -- 事务版

    :param name: 姓名
    :type name: str
    :param phone: 电话
    :type phone: str
    :param email: 电子信箱
    :type email: str
    :return: Card
    '''
    s_status = '正常'
    s_operator_type = '开户'

    with NotAutoCommit():
        try:
            card = open_account_v2_1(
                    name, phone, email, s_status, s_operator_type,
                    )
            return card
        except Exception as e:
            # 数据回滚
            msg = '未知错误. e: {}'.format(e)
            transaction.rollback()
            raise ValueError(msg)


