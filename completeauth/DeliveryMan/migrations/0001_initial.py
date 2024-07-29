# Generated by Django 5.0.6 on 2024-07-24 19:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryMan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('city', models.CharField(max_length=15)),
                ('location', models.CharField(max_length=20)),
                ('pincode', models.CharField(max_length=10)),
                ('joined_at', models.DateField()),
                ('is_active', models.BooleanField(default=True)),
                ('salary', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Deliver_User', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
