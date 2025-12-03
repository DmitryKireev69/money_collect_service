from rest_framework import viewsets
from .models import Collect, Payment
from .serializers import (
    CollectSimpleSerializer,
    PaymentSimpleSerializer
)


class CollectViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с групповыми сборами
    """
    queryset = Collect.objects.all()
    serializer_class = CollectSimpleSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с групповыми сборами
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSimpleSerializer