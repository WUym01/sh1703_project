from django.urls import path

from . import views

urlpatterns = [
    path('hello/', views.hello),

    path('open_account/', views.open_account),
    path('put_money/', views.put_money),
    path('draw_money/', views.draw_money),
    path('tansfer/', views.tansfer),
]