from django.contrib import admin

from . import models

# Register your models here.

class CardInfoInline(admin.TabularInline):
    model = models.CardInfo

class CardAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'status',
        'balance',
        'balance_available',
        'balance_freeze',
    )
    inlines = [CardInfoInline]

class CardOperateAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
    )

class CardStatusAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
    )


admin.site.register(models.CardStatus, CardStatusAdmin)
admin.site.register(models.CardOperate, CardOperateAdmin)
admin.site.register(models.Card, CardAdmin)
admin.site.register(models.CardInfo)
admin.site.register(models.CardHistory)
