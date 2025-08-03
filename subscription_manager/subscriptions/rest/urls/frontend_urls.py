from django.urls import path
from subscriptions.rest.views.subscriptions import SubscriptionListView

urlpatterns = [
    path('subscriptions/', SubscriptionListView.as_view(), name='subscription-list'),
]
