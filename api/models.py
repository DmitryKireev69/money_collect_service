from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import User

import uuid


class Collect(models.Model):
    """Модель группового денежного сбора"""

    class Occasion(models.TextChoices):
        BIRTHDAY = 'birthday', 'День рождения'
        WEDDING = 'wedding', 'Свадьба'
        MEDICAL = 'medical', 'Медицинское лечение'
        CHARITY = 'charity', 'Благотворительность'
        EDUCATION = 'education', 'Образование'
        BUSINESS = 'business', 'Бизнес'
        OTHER = 'other', 'Другое'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name='Идентификатор сбора')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='collects',
        verbose_name='Автор сбора'
    )
    title = models.CharField(
        max_length=200,
        verbose_name='Название сбора')
    occasion = models.CharField(
        max_length=50,
        choices=Occasion.choices,
        verbose_name='Повод сбора'
    )
    description = models.TextField(verbose_name='Описание сбора')
    target_amount_cents = models.BigIntegerField(
        null=True,
        blank=True,
        verbose_name='Целевая сумма (в копейках)',
        help_text='Укажите только если это НЕ бесконечный сбор'
    )
    collected_amount_cents = models.BigIntegerField(
        default=0,
        verbose_name='Собранная сумма (в копейках)'
    )
    contributors_count = models.PositiveIntegerField(
        default=0,
        verbose_name='Количество донатеров'
    )
    cover_image = models.ImageField(
        upload_to='collects/covers/%Y/%m/%d/',
        null=True,
        blank=True,
        verbose_name='Обложка сбора'
    )
    end_datetime = models.DateTimeField(verbose_name='Дата и время завершения сбора')
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активный сбор'
    )

    class Meta:
        verbose_name = 'Групповой сбор'
        verbose_name_plural = 'Групповые сборы'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['author', 'created_at']),
            models.Index(fields=['is_active', 'end_datetime']),
            models.Index(fields=['occasion']),
        ]

    def __str__(self):
       return self.title



class Payment(models.Model):
    """Модель платежа для сбора"""

    class Status(models.TextChoices):
        PENDING = 'pending', 'Ожидает оплаты'
        SUCCESSFUL = 'successful', 'Успешный'
        FAILED = 'failed', 'Неуспешный'
        REFUNDED = 'refunded', 'Возвращен'


    class PaymentMethod(models.TextChoices):
        CARD = 'card', 'Банковская карта'
        SBP = 'sbp', 'СБП'
        QIWI = 'qiwi', 'QIWI'
        YOOMONEY = 'yoomoney', 'ЮMoney'
        OTHER = 'other', 'Другое'


    id = models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False, verbose_name='Идентификатор платежа')
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='payments',
        verbose_name='Пользователь'
    )
    collect = models.ForeignKey(
        'Collect',
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='Сбор'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(1)],
        verbose_name='Сумма платежа'
    )
    payment_method = models.CharField(
        max_length=50,
        choices=PaymentMethod.choices,
        verbose_name='Способ оплаты'
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name='Статус платежа'
    )
    comment = models.TextField(
        blank=True,
        null=True,
        verbose_name='Комментарий к платежу'
    )
    is_anonymous = models.BooleanField(
        default=False,
        verbose_name='Анонимный платеж'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата и время создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата и время обновления'
    )

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['collect', 'created_at']),
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['payment_method']),
        ]

    def __str__(self):
        return f"Платеж {self.id}"
