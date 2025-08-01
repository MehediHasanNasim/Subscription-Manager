from django.contrib import admin
from .models import Plan, Subscription, ExchangeRateLog

class PlanAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'duration_days')
    search_fields = ('name',)
    list_filter = ('duration_days',)
    ordering = ('price',)

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'plan', 'start_date', 'end_date', 'status')
    search_fields = ('user__username', 'plan__name')
    list_filter = ('status', 'plan')
    date_hierarchy = 'start_date'
    raw_id_fields = ('user', 'plan')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user', 'plan')

class ExchangeRateLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'base_currency', 'target_currency', 'rate', 'fetched_at')
    list_filter = ('base_currency', 'target_currency')
    search_fields = ('base_currency', 'target_currency')
    date_hierarchy = 'fetched_at'
    readonly_fields = ('fetched_at',)

admin.site.register(Plan, PlanAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(ExchangeRateLog, ExchangeRateLogAdmin)