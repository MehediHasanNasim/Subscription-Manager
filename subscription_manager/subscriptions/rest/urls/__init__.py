from django.urls import path, include

app_name = 'subscriptions_api'

urlpatterns = [
    path('', include('subscriptions.rest.urls.subscriptions')),

]