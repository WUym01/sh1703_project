from django.db import models

# Create your models here.


class CardStatus(models.Model):
    '''银行卡的状态'''
    name = models.CharField(max_length=16, verbose_name='名称')
    remark = models.TextField(blank=True, verbose_name='备注')

    def __str__(self):
        return self.name


class CardOperate(models.Model):
    '''银行卡的操作'''
    name = models.CharField(max_length=16, verbose_name='名称')
    remark = models.TextField(verbose_name='备注')

    def __str__(self):
        return self.name

class Card(models.Model):
    '''银行卡'''

    balance = models.IntegerField(verbose_name="余额", default=0)
    balance_available = models.IntegerField(verbose_name="可用余额", default=0)
    balance_freeze = models.IntegerField(verbose_name="冻结金额", default=0)

    status = models.ForeignKey(
        CardStatus,
        on_delete=models.CASCADE,
        verbose_name='状态',
    )

    def __str__(self):
        return '{card_id} - {balance}'.format(
            card_id=self.id,
            balance=self.balance,

        )

    def name(self):
        return self.cardinfo.name
    name.short_description = '姓名'

class CardInfo(models.Model):
    '''用户信息'''
    name = models.CharField(max_length=64, verbose_name='姓名')
    phone = models.CharField(max_length=64, verbose_name='电话')
    email = models.EmailField(blank=True)

    card = models.OneToOneField(
        'Card',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name

class CardHistory(models.Model):
    '''银行卡的流水账'''
    time = models.DateTimeField(auto_now_add=True, verbose_name='时间')
    remark = models.TextField(verbose_name='说明')

    card = models.ForeignKey(
        'Card',
        on_delete=models.DO_NOTHING,
        verbose_name='银行卡',
    )

    operator = models.ForeignKey(
        'CardOperate',
        on_delete=models.DO_NOTHING,
        verbose_name='操作类型',
    )

    def __str__(self):
        return "{time} - {card_id} - {operator}".format(
            time=self.time.isoformat(),
            card_id=self.card.id,
            operator=self.operator.name,
        )




