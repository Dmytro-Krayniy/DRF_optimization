# Generated by Django 5.0.3 on 2024-08-06 12:01

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clients', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan_type', models.CharField(choices=[('full', 'Full'), ('student', 'Student'), ('discount', 'Discount')], max_length=20)),
                ('discount_percent', models.PositiveIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(100)])),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('full_price', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='subscriptions', to='clients.client')),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='subscriptions', to='services.plan')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='subscriptions', to='services.service')),
            ],
        ),
    ]
