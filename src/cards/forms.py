# -*- encoding: utf-8 -*-

# python apps

# django apps
from django import forms

# our apps


class PutMoneyForm(forms.Form):
    card_id = forms.IntegerField(label='银行卡号')
    money = forms.IntegerField(label='发生金额')