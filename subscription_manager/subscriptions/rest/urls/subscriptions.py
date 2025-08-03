from django.urls import path
from rest_framework.routers import DefaultRouter
from subscriptions.rest.views.subscriptions import (
    SubscriptionViewSet, 
    ExchangeRateView, 
    LogoutView, 
    PlanViewSet, 
    SubscriptionListView
)

from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.decorators import api_view
from rest_framework.response import Response

router = DefaultRouter()
router.register(r'subscriptions', SubscriptionViewSet, basename='subscription')
router.register(r'exchange-rate', ExchangeRateView, basename='exchange-rate')
router.register('plans', PlanViewSet, basename='plan')


urlpatterns = [
    path('login/', obtain_auth_token, name='api-login'),
    path('logout/', LogoutView.as_view(), name='api-logout'),

    path('subscribe/', SubscriptionViewSet.as_view({'post': 'create'})),
    path('cancel/', SubscriptionViewSet.as_view({'post': 'cancel'})),
] + router.urls 