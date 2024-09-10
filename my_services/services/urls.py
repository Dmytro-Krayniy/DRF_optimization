from django.urls import path
from rest_framework import routers

from services.views import SubscriptionView

router = routers.DefaultRouter()
router.register('subscription', SubscriptionView)


urlpatterns = [

] + router.urls
