from rest_framework import serializers
from .models import Collect, Payment


class CollectSimpleSerializer(serializers.ModelSerializer):
    """Сериализатор для Collect"""

    class Meta:
        model = Collect
        fields = '__all__'


class PaymentSimpleSerializer(serializers.ModelSerializer):
    """Сериализатор для Payment"""
    user_full_name = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = '__all__'

    def get_user_full_name(self, obj):
        """
        Возвращает ФИО пользователя или 'Аноним'
        """
        if obj.is_anonymous:
            return "Аноним"

        if not obj.user:
            return "Гость"

        first_name = obj.user.first_name or ''
        last_name = obj.user.last_name or ''
        full_name = f"{first_name} {last_name}".strip()
        return full_name if full_name else obj.user.username