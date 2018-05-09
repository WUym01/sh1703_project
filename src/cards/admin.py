from django.contrib import admin

from . import models

# Register your models here.

class CardAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'status',
        'balance',
        'balance_available',
    )

admin.site.register(models.CardStatus)
admin.site.register(models.CardOperate)
admin.site.register(models.Card, CardAdmin)
admin.site.register(models.CardInfo)
admin.site.register(models.CardHistory)
