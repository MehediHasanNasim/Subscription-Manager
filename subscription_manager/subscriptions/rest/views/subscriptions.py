import requests
from datetime import timedelta
from datetime import datetime
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from django.db import transaction
from subscriptions.models import Subscription, ExchangeRateLog, Plan
from subscriptions.rest.serializers.subscriptions import (
    SubscriptionSerializer,
    CancelSubscriptionSerializer,
    ExchangeRateSerializer,
    PlanSerializer
)
from subscriptions.services.exchange_rate import get_exchange_rate
from subscriptions.rest.permissions import (
    IsAdminOrOwnerForSubscriptions,
    IsAdminOrStaffReadOnly,
    IsAdminOrStaffCanManagePlan
)

class LogoutView(APIView):
    def post(self, request):
        request.user.auth_token.delete()
        return Response(
            {"detail": "Successfully logged out."},
            status=status.HTTP_200_OK
        )
    
    
class SubscriptionViewSet(viewsets.ViewSet):
    permission_classes = [IsAdminOrOwnerForSubscriptions]

    def list(self, request):
        if request.user.is_superuser or request.user.is_staff:
            subscriptions = Subscription.objects.all()
        else:
            subscriptions = Subscription.objects.filter(user=request.user)

        serializer = SubscriptionSerializer(subscriptions, many=True)
        return Response(serializer.data)


    @transaction.atomic
    def create(self, request):
        try:
            serializer = SubscriptionSerializer(
                data=request.data,
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            
            # Calculate end date
            plan = serializer.validated_data['plan']
            start_date = timezone.now().date()
            end_date = start_date + timedelta(days=plan.duration_days)
            
            # Create subscription
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
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
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
    permission_classes = [IsAdminOrStaffReadOnly]

    def list(self, request):
        base = request.query_params.get('base', 'USD').upper()
        target = request.query_params.get('target', 'BDT').upper()
        
        try:
            rate = get_exchange_rate(base, target)
            return Response({
                'base_currency': base,
                'target_currency': target,
                'rate': rate,
                'fetched_at': datetime.now().isoformat()
            })
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': 'An unexpected error occurred'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        

class PlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    permission_classes = [IsAdminOrStaffCanManagePlan]