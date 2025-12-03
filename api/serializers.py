from rest_framework import serializers
from .models import Collect, Payment


class CollectSimpleSerializer(serializers.ModelSerializer):
    """Сериализатор для Collect"""

    class Meta:
        model = Collect
        fields = '__all__'


class PaymentSimpleSerializer(serializers.ModelSerializer):
    """Сериализатор для Payment"""

    class Meta:
        model = Payment
        fields = '__all__'