from rest_framework import serializers
from subscriptions.models import Plan, Subscription, ExchangeRateLog

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['id', 'name', 'price', 'duration_days']

class SubscriptionSerializer(serializers.ModelSerializer):
    plan = PlanSerializer(read_only=True)
    plan_id = serializers.PrimaryKeyRelatedField(
        queryset=Plan.objects.all(),
        source='plan',
        write_only=True
    )
    
    class Meta:
        model = Subscription
        fields = [
            'id', 'plan', 'plan_id', 
            'start_date', 'end_date', 'status'
        ]
        read_only_fields = ['start_date', 'end_date', 'status']

class CancelSubscriptionSerializer(serializers.Serializer):
    subscription_id = serializers.PrimaryKeyRelatedField(
        queryset=Subscription.objects.all()
    )

class ExchangeRateSerializer(serializers.Serializer):
    base_currency = serializers.CharField(max_length=3)
    target_currency = serializers.CharField(max_length=3)
    rate = serializers.DecimalField(max_digits=12, decimal_places=6)
    fetched_at = serializers.DateTimeField()