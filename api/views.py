from rest_framework import viewsets, mixins
from .models import Collect, Payment
from .serializers import (
    CollectSimpleSerializer,
    PaymentSimpleSerializer
)
from rest_framework.response import Response

class CollectViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с групповыми сборами
    """
    queryset = Collect.objects.all()
    serializer_class = CollectSimpleSerializer


class PaymentViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                     mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    ViewSet для работы с групповыми сборами
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSimpleSerializer
