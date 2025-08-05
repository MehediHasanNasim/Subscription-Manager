# Subscription Management System with Currency Exchange Tracker

![Django](https://img.shields.io/badge/Django-5.0.6-green)
![DRF](https://img.shields.io/badge/Django_REST-3.16-blue)
![Celery](https://img.shields.io/badge/Celery-5.5.3-red)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange)
![Redis](https://img.shields.io/badge/Redis-6.2-red)

A Django-based system for managing subscriptions with currency exchange rate tracking, featuring:
- REST API endpoints
- Celery background tasks
- MySQL database
- Redis broker
- Bootstrap frontend
- Dockerized deployment

## Features

- **User Subscription Management**
  - Create/view/cancel subscriptions
  - Multiple plan types
  - Status tracking (active/cancelled/expired)

- **Currency Exchange**
  - Real-time rate fetching
  - Historical rate logging
  - Hourly background updates

- **Admin Interface**
  - Full CRUD operations
  - Custom permission system
  - Staff can:
      - Add/Edit/Delete plans 
      - View user subscriptions 
      - View exchange logs 

## Prerequisites
- Docker Engine 20.10+
- Docker Compose 2.0+
- Python 3.12
- MySQL 8.0
- Redis 6.2

## Installation
### 1. Clone the repository
```bash
git clone https://github.com/MehediHasanNasim/Subscription-Manager.git
cd subscription-manager
```
### 2. Set up environment
```bash
cp .env.example .env
# Edit .env with your configurations
```
### 3. Start services
```bash
docker-compose up -d --build
```
### 4. Apply migrations
```bash
docker-compose exec web python manage.py migrate
```
### 5. Create superuser
```bash
docker-compose exec web python manage.py createsuperuser
```
### 🚀 API Endpoints
| Endpoint              | Method | Description               |
| --------------------- | ------ | ------------------------- |
| `/api/subscribe/`     | POST   | Create a new subscription |
| `/api/subscriptions/` | GET    | List user subscriptions   |
| `/api/cancel/`        | POST   | Cancel a subscription     |
| `/api/exchange-rate/` | GET    | Get current exchange rate |
#### Example Request:
```bash
curl -X GET "http://localhost:8000/api/exchange-rate/?base=USD&target=BDT"
```
#### Admin Access:
```bash
http://localhost:8000/admin/
```
#### Frontend Access:
```bash
http://localhost:8000/subscriptions/
```


## Local Development Setup (Non-Docker)
```bash
git clone https://github.com/yourusername/subscription-manager.git
cd subscription-manager
python -m venv venv

# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
```
### Setup .env, Database Migrations, Start Services, Redis, Celery Worker
```bash
cp .env.example .env
# Edit .env with your configurations
```
```bash
python manage.py migrate
python manage.py createsuperuser
```
```bash
python manage.py runserver
```
```bash
redis-server
```
```bash
celery -A subscription_manager worker --loglevel=info --pool=solo
```
```bash
celery -A subscription_manager beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

## System Architecture

```mermaid
graph TD
    A[Frontend] --> B[Django Views]
    B --> C[DRF API]
    C --> D[MySQL Database]
    C --> E[Redis]
    E --> F[Celery Worker]
    F --> G[Exchange Rate API]
```


## System Walkthrough

### 1. Docker Setup Success
<img width="660" height="491" alt="docker build successful" src="https://github.com/user-attachments/assets/7df4d617-14f0-4331-be21-c52f497a6771" />

*Successful Docker build process*

<img width="1362" height="727" alt="docker run successful__" src="https://github.com/user-attachments/assets/06aafc39-ae98-49ad-9329-ff0cc824df79" />

*All containers running successfully*

### 2. Database Configuration
<img width="1363" height="727" alt="db_connection" src="https://github.com/user-attachments/assets/40048b95-3ab8-411c-ada7-b6e9ef98cdaa" />
*Verified MySQL database connection*

### 3. Redis Integration
<img width="1362" height="680" alt="redis_connection" src="https://github.com/user-attachments/assets/1056ab4c-657b-42c1-8396-324c25783d75" />
*Redis service connected and working with Celery*

### 4. Admin Interface Customization
<img width="1347" height="637" alt="customize admin" src="https://github.com/user-attachments/assets/689df574-3366-4f9b-a977-569f2ef88d0d" />
*Customized Django admin interface*

### 5. Currency API Integration
<img width="1175" height="509" alt="currency_api" src="https://github.com/user-attachments/assets/79a352e1-bea7-47dc-a029-bc1b0ae8d6e5" />
*Live currency exchange rate API working*

### 6. Exchange Rate Logging
<img width="733" height="382" alt="exchangeratelog with timestamp" src="https://github.com/user-attachments/assets/e6705e48-037f-4fc5-b634-a7f98d127061" />

*Timestamped exchange rate logs in Django admin*

### 7. Frontend UI
<img width="1210" height="428" alt="Frontend UI" src="https://github.com/user-attachments/assets/e59654f4-e071-42e0-8aa9-0e6201ed6643" />
*Bootstrap-powered subscription management interface*


