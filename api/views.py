from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets, mixins
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

    @method_decorator(cache_page(60 * 5))
    def list(self, request, *args, **kwargs):
        """Список сборов с кэшированием"""
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60 * 5))
    def retrieve(self, request, *args, **kwargs):
        """Детали сбора с кэшированием"""
        return super().retrieve(request, *args, **kwargs)


class PaymentViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                     mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    ViewSet для работы с групповыми сборами
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSimpleSerializer

    @method_decorator(cache_page(60 * 2))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60 * 2))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
