import requests
from django.conf import settings
from django.core.cache import cache
from datetime import datetime
from ..models import ExchangeRateLog

def get_exchange_rate(base_currency, target_currency):
    cache_key = f'exchange_rate_{base_currency}_{target_currency}'
    cached_rate = cache.get(cache_key)
    
    if cached_rate:
        return cached_rate
    
    try:
        url = f"{settings.EXCHANGE_RATE_API_URL}{settings.EXCHANGE_RATE_API_KEY}/pair/{base_currency}/{target_currency}"
        response = requests.get(url)
        data = response.json()
        
        if data.get('result') == 'success':
            rate = data['conversion_rate']
            # Save to database
            exchange_log = ExchangeRateLog.objects.create(
                base_currency=base_currency,
                target_currency=target_currency,
                rate=rate
            )
            # Cache the result
            cache.set(cache_key, rate, settings.CACHE_TTL)
            return rate
        else:
            raise ValueError(f"API Error: {data.get('error-type', 'Unknown error')}")
            
    except requests.RequestException as e:
        ExchangeRateLog.log_failure(base_currency, target_currency, e)
        # Fallback to most recent database entry if available
        last_rate = ExchangeRateLog.objects.filter(
            base_currency=base_currency,
            target_currency=target_currency,
            success=True
        ).order_by('-fetched_at').first()
        
        if last_rate:
            return last_rate.rate
        raise ValueError("Service unavailable and no cached rates available")
    except ValueError as e:
        ExchangeRateLog.log_failure(base_currency, target_currency, e)
        raise