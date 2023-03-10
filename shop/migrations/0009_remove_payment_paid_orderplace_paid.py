# Generated by Django 4.1.7 on 2023-03-10 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_remove_orderplace_payment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='paid',
        ),
        migrations.AddField(
            model_name='orderplace',
            name='paid',
            field=models.BooleanField(default=False),
        ),
    ]