from django.contrib import admin
from models import Currency, ExchangeRate


class CurrencyAdmin(admin.ModelAdmin):
    search_fields = ('code',)
    list_display = ('code', 'name')


class ExchangeRateAdmin(admin.ModelAdmin):
    search_fields = ('source__code', 'target__code')
    list_display = ('source', 'target', 'rate')
    list_select_related = ('source', 'target')
    raw_id_fields = ('source', 'target')
    list_filter = ('source__code',)

    class Meta:
        model = ExchangeRate


admin.site.register(Currency, CurrencyAdmin)
admin.site.register(ExchangeRate, ExchangeRateAdmin)
