# Generated by Django 4.1.7 on 2023-03-09 22:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_payment_orderplace'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderplace',
            name='payment',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='shop.payment'),
        ),
    ]
