from django.contrib.auth.models import User
from django.db import models


class Client(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    company_name = models.CharField(max_length=100)
    full_address = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username
