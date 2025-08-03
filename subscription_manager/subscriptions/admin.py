from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Plan, Subscription, ExchangeRateLog

class PlanAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'duration_days', 'active_subscriptions_count')
    search_fields = ('name',)
    list_filter = ('duration_days',)
    ordering = ('price',)

    def active_subscriptions_count(self, obj):
        return obj.subscriptions.filter(status='active').count()
    active_subscriptions_count.short_description = 'Active Subs'

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_email', 'user', 'plan_name', 'plan', 'start_date', 'end_date', 'status')
    search_fields = ('user__email', 'user__username', 'plan__name')
    list_filter = ('status', 'plan', 'start_date')
    date_hierarchy = 'start_date'
    raw_id_fields = ('user', 'plan')
    actions = ['mark_as_cancelled']

    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user', 'plan')

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'User Email'
    user_email.admin_order_field = 'user__email'

    def plan_name(self, obj):
        return obj.plan.name
    plan_name.short_description = 'Plan'
    plan_name.admin_order_field = 'plan__name'

    def mark_as_cancelled(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'{updated} subscriptions cancelled')
    mark_as_cancelled.short_description = "Mark selected as cancelled"

class ExchangeRateLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'base_currency', 'target_currency', 'rate', 'fetched_at', 'was_successful')
    list_filter = ('base_currency', 'target_currency')
    search_fields = ('base_currency', 'target_currency')
    date_hierarchy = 'fetched_at'
    readonly_fields = ('fetched_at',)

    def was_successful(self, obj):
        return obj.success
    was_successful.boolean = True
    was_successful.short_description = 'Success'


admin.site.register(Plan, PlanAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(ExchangeRateLog, ExchangeRateLogAdmin)