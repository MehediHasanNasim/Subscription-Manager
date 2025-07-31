from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Plan(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # USD
    duration_days = models.PositiveIntegerField(
        help_text="Duration of plan in days"
    )
    
    def __str__(self):
        return f"{self.name} (${self.price})"
    
    class Meta:
        ordering = ['price']


class Subscription(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired'),
    ]
    
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='subscriptions'
    )
    plan = models.ForeignKey(
        Plan,
        on_delete=models.PROTECT,
        related_name='subscriptions'
    )
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active'
    )
    
    def __str__(self):
        return f"{self.user.email} - {self.plan.name} ({self.status})"
    
    class Meta:
        ordering = ['-start_date']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['end_date']),
        ]
        unique_together = ['user', 'plan']


class ExchangeRateLog(models.Model):
    base_currency = models.CharField(max_length=3, default='USD')
    target_currency = models.CharField(max_length=3)
    rate = models.DecimalField(max_digits=12, decimal_places=6)
    fetched_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.base_currency}→{self.target_currency}: {self.rate}"
    
    class Meta:
        ordering = ['-fetched_at']
        indexes = [
            models.Index(fields=['base_currency', 'target_currency']),
            models.Index(fields=['fetched_at']),
        ]
        verbose_name = "Exchange Rate Log"