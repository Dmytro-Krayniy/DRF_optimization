from rest_framework import serializers

from services.models import Subscription, Plan


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ('__all__')


class SubscriptionSerializer(serializers.ModelSerializer):
    plan = PlanSerializer()
    client_company = serializers.CharField(source='client.company_name')
    client_email = serializers.CharField(source='client.user.email')
    price = serializers.SerializerMethodField()

    def get_price(self, instance) -> float:
        return instance.price

    class Meta:
        model = Subscription
        fields = ['id', 'plan_id', 'client_company', 'client_email', 'service_id', 'plan', 'price']
