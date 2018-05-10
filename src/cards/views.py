from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from .models import Card, CardInfo, CardHistory
from datetime import datetime

def hello(request):
    return HttpResponse("hello world")

def open_account(request):
    '''开户'''
    balance = request.POST.get("balance")
    balance_available = request.POST.get("balance_available")
    balance_freeze = request.POST.get("balance_freeze")
    card = Card.createcard(balance, balance_available, balance_freeze, "正常")
    card.save()

    name = request.POST.get("name")
    phone = request.POST.get("phone")
    email = request.POST.get("email")
    cardinfo = CardInfo.createcardinfo(name, phone, email, card)
    cardinfo.save()

    remark = "开户"
    operator = openaccount
    cardhistory = CardHistory.createcardhistory(remark, card, operator)
    cardhistory.save()

def put_money(request):
    '''存款'''
    card_id = request.POST.get('id')
    money = request.POST.get('money')
    card = Card.objects.filter(id=card_id)
    card.balance += money

    remark = "存款"
    operator = put_money
    cardhistory = CardHistory.createcardhistory(card_id, remark, card, operator)
    cardhistory.save()


def draw_money(request):
    '''取款'''
    card_id = request.POST.get('id')
    money = request.POST.get('money')
    card = Card.objects.filter(id=card_id)
    card.balance -= money

    time = datetime.now()
    remark = "取款"
    operator = draw_money
    cardhistory = CardHistory.createcardhistory(time, remark, card, operator)
    cardhistory.save()

def tansfer(request):
    '''转账'''
    pass

