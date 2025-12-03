# api/management/commands/seed_data.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import transaction
import random
from datetime import timedelta
from decimal import Decimal
from api.models import Collect, Payment


class Command(BaseCommand):
    help = 'Создает тестовые данные: 2000 пользователей, 2000 сборов, 5000 платежей'

    def handle(self, *args, **options):
        with transaction.atomic():
            users = [User.objects.create_user(f'user{i}', 'pass') for i in range(2001)]
            collects = [Collect.objects.create(
                author=random.choice(users),
                title=f'Сбор {i}',
                occasion='birthday',
                target_amount_cents=500000,
                end_datetime=timezone.now() + timedelta(days=30)
            ) for i in range(2001)]

            Payment.objects.bulk_create([
                Payment(user=random.choice(users), collect=random.choice(collects),
                        amount=Decimal('1000'), payment_method='card')
                for _ in range(5001)
            ])

        print(f"Создано 2000 пользователей")
        print(f"Создано 2000 сборов")
        print(f"Создано 5000 платежей")