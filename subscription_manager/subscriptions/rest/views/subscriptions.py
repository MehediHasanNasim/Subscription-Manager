from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from django.db import transaction
from subscriptions.models import Subscription, ExchangeRateLog
from subscriptions.rest.serializers.subscriptions import (
    SubscriptionSerializer,
    CancelSubscriptionSerializer,
    ExchangeRateSerializer
)
import requests
from datetime import timedelta


class LogoutView(APIView):
    def post(self, request):
        request.user.auth_token.delete()
        return Response(
            {"detail": "Successfully logged out."},
            status=status.HTTP_200_OK
        )
    
    
class SubscriptionViewSet(viewsets.ViewSet):
    def list(self, request):
        subscriptions = Subscription.objects.filter(user=request.user)
        serializer = SubscriptionSerializer(subscriptions, many=True)
        return Response(serializer.data)

    @transaction.atomic
    def create(self, request):
        serializer = SubscriptionSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            plan = serializer.validated_data['plan']

            # Check if user already subscribed to this plan
            if Subscription.objects.filter(user=request.user, plan=plan).exists():
                raise ValidationError("You are already subscribed to this plan.")
            
            # Calculate end date based on plan duration
            start_date = timezone.now().date()
            end_date = start_date + timedelta(days=plan.duration_days)
            
            subscription = Subscription.objects.create(
                user=request.user,
                plan=plan,
                start_date=start_date,
                end_date=end_date,
                status='active'
            )
            
            return Response(
                SubscriptionSerializer(subscription).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def cancel(self, request):
        serializer = CancelSubscriptionSerializer(data=request.data)
        if serializer.is_valid():
            subscription = serializer.validated_data['subscription_id']
            
            if subscription.user != request.user:
                return Response(
                    {'error': 'Not your subscription'},
                    status=status.HTTP_403_FORBIDDEN
                )
                
            subscription.status = 'cancelled'
            subscription.save()
            
            return Response(
                SubscriptionSerializer(subscription).data,
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ExchangeRateView(viewsets.ViewSet):
    def list(self, request):
        base = request.query_params.get('base', 'USD').upper()
        target = request.query_params.get('target', 'BDT').upper()
        
        # Try to get cached rate first (last 10 minutes)
        cached_rate = ExchangeRateLog.objects.filter(
            base_currency=base,
            target_currency=target,
            fetched_at__gte=timezone.now() - timedelta(minutes=10)
        ).first()
        
        if cached_rate:
            serializer = ExchangeRateSerializer(cached_rate)
            return Response(serializer.data)
        
        # Fetch from external API if no cached version
        try:
            # Using ExchangeRate-API (you'll need an API key)
            response = requests.get(
                f'https://v6.exchangerate-api.com/v6/YOUR_API_KEY/pair/{base}/{target}'
            )
            data = response.json()
            
            if data.get('result') == 'success':
                rate = ExchangeRateLog.objects.create(
                    base_currency=base,
                    target_currency=target,
                    rate=data['conversion_rate']
                )
                return Response(ExchangeRateSerializer(rate).data)
            else:
                return Response(
                    {'error': 'Failed to fetch exchange rate'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except requests.RequestException:
            return Response(
                {'error': 'Exchange rate service unavailable'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )