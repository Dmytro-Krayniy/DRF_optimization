from django.db.models import Prefetch, F, Sum
from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet

from clients.models import Client
from services.models import Subscription
from services.serializers import SubscriptionSerializer


class SubscriptionView(ReadOnlyModelViewSet):
    queryset = Subscription.objects.all().prefetch_related(
        'plan',
        # 'service',
        Prefetch(
            'client',
            queryset=Client.objects.all().select_related().only('company_name', 'user__email')
        )
    )#.annotate(price=F('service__full_price') * (1 - F('plan__discount_percent') / 100.00))
    serializer_class = SubscriptionSerializer

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data = {
            'result': response.data,
            'total_amount': self.get_queryset().aggregate(total=Sum('price')).get('total')
        }
        return response
