from datetime import datetime

from django.db import transaction

from .models import Card, CardHistory, CardOperate, CardInfo, CardStatus

def open_account(num, name, phone, email):
    '''开户'''
    card = Card()
    card.id = num
    card.balance = 0
    card.balance_available = 0
    card.balance_freeze = 0
    card.status = CardStatus.objects.get(id=1)
    card.save()

    cardinfo = CardInfo.createcardinfo(name, phone, email, card)
    cardinfo.save()

    remark = "开户\n" "金额" + str(card.balance) + "元\n" "状态" + str(card.status)
    operator = CardOperate.objects.get(id=3)
    cardhistory = CardHistory.createcardhistory(card, remark, operator)
    cardhistory.save()


def put_money(card, money):
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

    status = card.status.name
    if status == '正常':
        pre_balance = card.balance
        if pre_balance >= money:
            card.balance = pre_balance - int(money)
            card.balance_available -= int(money)
            card.save()

            remark = "取款" + str(money) + "元\n" "前金额" + str(pre_balance) + "元\n" "后金额" + str(card.balance) + "元\n" "状态" + str(status)
            operator = CardOperate.objects.get(id=10)
            cardhistory = CardHistory.createcardhistory(card, remark, operator)
            cardhistory.save()

        else:
            pre_balance = card.balance
            return "可用金额" + str(pre_balance)
    else:
        raise ValueError("银行卡状态错误")



def tansfer(card1, card2, money):
    '''转账'''
    status = card1.status.name
    if status == '正常':
        pre_balance = card1.balance
        if pre_balance >= money:
            card1.balance = pre_balance - int(money)
            card1.balance_available -= int(money)
            card1.save()

            remark = "取款" + str(money) + "元\n" "前金额" + str(pre_balance) + "元\n" "后金额" + str(
                card1.balance) + "元\n" "状态" + str(status)
            operator = CardOperate.objects.get(id=10)
            cardhistory = CardHistory.createcardhistory(card1, remark, operator)
            cardhistory.save()

        else:
            pre_balance = card1.balance
            return "可用金额" + str(pre_balance)
    else:
        raise ValueError("银行卡状态错误")

    status = card2.status.name
    if status == '正常':
        pre_balance = card2.balance
        card2.balance = pre_balance + int(money)
        card2.balance_available += int(money)
        card2.save()

        remark = "存款" + str(money) + "元\n" "前金额" + str(pre_balance) + "元\n" "后金额" + str(
            card2.balance) + "元\n" "状态" + str(status)
        operator = CardOperate.objects.get(id=1)
        cardhistory = CardHistory.createcardhistory(card2, remark, operator)
        cardhistory.save()

    else:
        raise ValueError("银行卡状态错误")



































