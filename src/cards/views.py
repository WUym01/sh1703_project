# -*- encoding: utf-8 -*-

# python apps
import json
import pdb

# django apps
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView
from django.views import View
from django.urls import reverse
from django.core.paginator import Paginator

# Create your views here.
from .models import Card
from .helpers import put_money_v3
from .forms import PutMoneyForm


def hello(request):
    ''' 演示函数模式的视图 '''
    return HttpResponse('hello')


class CardList(ListView):
    ''' 演示类模式的视图 '''
    models = Card
    queryset = Card.objects.all()


def put_money_view(request):
    ''' 存钱 '''
    msg_error = None
    info = {'error': None}
    if request.method == 'POST':
        # 取form表单的值
        card_id = request.POST.get('card_id')
        money = request.POST.get('money')
        print('card_id: {}, money: {}'.format(card_id, money))

        try:
            # 数据转换
            card = Card.objects.get(pk=card_id)
            money = int(money)

            put_money_v3(card, money)
        except ValueError as e:
            msg_error = str(e)
        except Exception as e:
            msg_error = '未知错误. e: {}'.format(e)

        if msg_error is None:
            # 跳转到其它页面
            return redirect('/hello')
        else:
            info = {'error': msg_error}

    tpl = 'cards/put_money.html'
    return render(request, tpl, info)


class CardView(View):
    ''' 银行卡信息 '''
    pass

    def get(self, request, *args, **kwargs):
        ''' 获取Card的记录
            返回单条记录，或者多条记录
            返回html，或者json格式。

        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        print('CardView.get(): ...')
        print('request.GET: {}'.format(request.GET))

        info = None
        format_json = request.GET.get('json', None)

        print('format_json: {}'.format(format_json))

        card_id = request.GET.get('card_id', None)
        if card_id:
            # 访问Card单条记录
            card = Card.objects.get(pk=card_id)
            info = card.to_json()
            print('info: {}'.format(info))
        else:
            # 访问Card列表
            qs = Card.objects.all()

            # 分页
            page = request.GET.get('page')
            paginator = Paginator(qs, 2)
            contacts = paginator.get_page(page)
            info = {
                'count': qs.count(),
                'data': [
                    obj.to_json()
                    for obj in contacts
                ],
            }

        if format_json is None:
            # 返回html格式
            if card_id:
                # 单条记录
                tpl = 'cards/card_detail.html'
                info = {'obj': info}
            else:
                # 多条记录
                tpl = 'cards/card_list.html'
                info['contacts'] = contacts
                info['object_list'] = info['data']
            return render(request, tpl, info)
        else:
            # 返回json格式
            msg = json.dumps(info, ensure_ascii=False, indent=4)
            content_type = 'text/json'
            return HttpResponse(msg, content_type=content_type)

    def post(self, request, *args, **kwargs):
        pass

        print('CardView.post(): ...')
        # pdb.set_trace()

        msg_error = None
        print('request.POST: {}'.format(request.POST))
        form = PutMoneyForm(request.POST)
        if form.is_valid():
            pass
            card_id = form.cleaned_data['card_id']
            money = form.cleaned_data['money']

            try:
                # 数据转换
                card = Card.objects.get(pk=card_id)

                put_money_v3(card, money)
            except ValueError as e:
                msg_error = str(e)
            except Exception as e:
                msg_error = '未知错误. e: {}'.format(e)
                print(msg_error)

            if msg_error:
                return HttpResponse(msg_error)

            # obj = Card.objects.get(pk=card_id)
            # msg = json.dumps(obj.to_json(), ensure_ascii=False, indent=4)
            # return HttpResponse(msg)

            # url = '/hello/cards_view/?card_id={}'.format(card_id)
            url = '{}?card_id={}'.format(
                    reverse('card_view'),
                    card_id,
                    )
        else:
            # url = '/hello/cards_class_list'
            url = reverse('card_view')
        return redirect(url)
