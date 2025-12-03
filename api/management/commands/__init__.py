# api/management/commands/seed_data.py
import random
from datetime import timedelta
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.models import User
from api.models import Collect, Payment


class Command(BaseCommand):
    help = 'Заполняет базу данных моковыми данными для тестирования'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            default=50,
            help='Количество пользователей для создания (по умолчанию: 50)'
        )
        parser.add_argument(
            '--collects',
            type=int,
            default=100,
            help='Количество сборов для создания (по умолчанию: 100)'
        )
        parser.add_argument(
            '--payments',
            type=int,
            default=2000,
            help='Количество платежей для создания (по умолчанию: 2000)'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Очистить существующие данные перед созданием'
        )

    def handle(self, *args, **options):
        users_count = options['users']
        collects_count = options['collects']
        payments_count = options['payments']
        clear_existing = options['clear']

        self.stdout.write(self.style.SUCCESS(
            f'Начинаю создание моковых данных: {users_count} пользователей, '
            f'{collects_count} сборов, {payments_count} платежей'
        ))

        # Очистка существующих данных
        if clear_existing:
            self.stdout.write('Очищаю существующие данные...')
            Payment.objects.all().delete()
            Collect.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()
            self.stdout.write(self.style.SUCCESS('Данные очищены'))

        # 1. Создаем пользователей
        users = self.create_users(users_count)

        # 2. Создаем сборы
        collects = self.create_collects(collects_count, users)

        # 3. Создаем платежи
        self.create_payments(payments_count, users, collects)

        self.stdout.write(self.style.SUCCESS('Моковые данные успешно созданы!'))

    def create_users(self, count):
        """Создание тестовых пользователей"""
        self.stdout.write(f'Создаю {count} пользователей...')

        users = []
        first_names = [
            'Иван', 'Алексей', 'Дмитрий', 'Сергей', 'Андрей', 'Михаил',
            'Екатерина', 'Анна', 'Мария', 'Ольга', 'Татьяна', 'Наталья'
        ]
        last_names = [
            'Иванов', 'Петров', 'Сидоров', 'Смирнов', 'Кузнецов', 'Попов',
            'Васильев', 'Федоров', 'Морозов', 'Волков', 'Алексеев', 'Лебедев'
        ]

        for i in range(count):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            username = f'user_{i + 1:04d}'
            email = f'{username}@example.com'

            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                    'is_active': True
                }
            )

            if created:
                user.set_password('password123')
                user.save()
                users.append(user)

            if (i + 1) % 10 == 0:
                self.stdout.write(f'  Создано {i + 1}/{count} пользователей')

        self.stdout.write(self.style.SUCCESS(f'Создано {len(users)} пользователей'))
        return users

    def create_collects(self, count, users):
        """Создание тестовых сборов"""
        self.stdout.write(f'Создаю {count} сборов...')

        collects = []
        occasions = [choice[0] for choice in Collect.Occasion.choices]

        titles = [
            'Сбор на лечение', 'Помощь семье', 'Образовательный проект',
            'Благотворительный фонд', 'Спортивное мероприятие', 'Творческий проект',
            'Экологическая инициатива', 'Помощь животным', 'Детский праздник',
            'Научное исследование', 'Музыкальный альбом', 'Театральная постановка'
        ]

        descriptions = [
            'Помогите собрать средства на важное дело',
            'Каждый рубль имеет значение для достижения цели',
            'Вместе мы можем сделать этот мир лучше',
            'Поддержите инициативу, которая изменит жизни',
            'Ваш вклад поможет реализовать важный проект',
            'Присоединяйтесь к нашему благотворительному сбору'
        ]

        for i in range(count):
            author = random.choice(users)
            title = f"{random.choice(titles)} #{i + 1}"
            occasion = random.choice(occasions)
            description = random.choice(descriptions)

            # Случайно выбираем тип сбора (ограниченный/бесконечный)
            if random.random() < 0.7:  # 70% ограниченных сборов
                target_amount_cents = random.randint(100000, 10000000)  # 1000-100000 руб
            else:
                target_amount_cents = None  # Бесконечный сбор

            # Дата завершения от 1 до 365 дней в будущем
            end_datetime = timezone.now() + timedelta(
                days=random.randint(1, 365)
            )

            collect = Collect.objects.create(
                author=author,
                title=title,
                occasion=occasion,
                description=description,
                target_amount_cents=target_amount_cents,
                collected_amount_cents=0,  # Начинаем с 0
                contributors_count=0,  # Начинаем с 0
                end_datetime=end_datetime,
                is_active=random.random() < 0.9  # 90% активных сборов
            )

            collects.append(collect)

            if (i + 1) % 20 == 0:
                self.stdout.write(f'  Создано {i + 1}/{count} сборов')

        self.stdout.write(self.style.SUCCESS(f'Создано {len(collects)} сборов'))
        return collects

    def create_payments(self, count, users, collects):
        """Создание тестовых платежей"""
        self.stdout.write(f'Создаю {count} платежей...')

        payment_methods = [choice[0] for choice in Payment.PaymentMethod.choices]

        comments = [
            'Желаю удачи!', 'Успехов в начинании', 'Очень важное дело',
            'Рад помочь', 'Надеюсь, все получится', 'От всей души',
            'Молодцы, что занимаетесь этим', 'Пусть все будет хорошо',
            '', '', '', '', ''  # Пустые комментарии для реалистичности
        ]

        batch_size = 100  # Размер батча для bulk_create
        payments_to_create = []

        for i in range(count):
            user = random.choice(users) if random.random() < 0.8 else None  # 80% с пользователем
            collect = random.choice(collects)

            # Сумма от 100 до 50000 рублей
            amount = Decimal(str(round(random.uniform(100.0, 50000.0), 2)))

            payment = Payment(
                user=user,
                collect=collect,
                amount=amount,
                payment_method=random.choice(payment_methods),
                comment=random.choice(comments),
                is_anonymous=user is None or random.random() < 0.2,  # 20% анонимных
                created_at=timezone.now() - timedelta(
                    days=random.randint(0, 30),
                    hours=random.randint(0, 23),
                    minutes=random.randint(0, 59)
                )
            )

            payments_to_create.append(payment)

            # Используем bulk_create для эффективности
            if len(payments_to_create) >= batch_size:
                Payment.objects.bulk_create(payments_to_create)
                payments_to_create = []
                self.stdout.write(f'  Создано {i + 1}/{count} платежей')

        # Создаем оставшиеся платежи
        if payments_to_create:
            Payment.objects.bulk_create(payments_to_create)

        # После создания всех платежей обновляем статистику сборов
        self.stdout.write('Обновляю статистику сборов...')
        self.update_collects_statistics(collects)

        self.stdout.write(self.style.SUCCESS(f'Создано {count} платежей'))

    def update_collects_statistics(self, collects):
        """Обновляет собранную сумму и количество донатеров для сборов"""
        from django.db.models import Sum, Count

        for collect in collects:
            # Агрегируем данные по платежам
            stats = collect.payments.aggregate(
                total_collected=Sum('amount'),
                unique_donors=Count('user', distinct=True)
            )

            # Обновляем сбор
            if stats['total_collected']:
                collect.collected_amount_cents = int(stats['total_collected'] * 100)
                collect.contributors_count = stats['unique_donors'] or 0
                collect.save(update_fields=['collected_amount_cents', 'contributors_count'])