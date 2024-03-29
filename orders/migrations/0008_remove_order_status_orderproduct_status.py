# Generated by Django 4.0.4 on 2022-06-16 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_alter_order_payment_method'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='status',
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='status',
            field=models.CharField(choices=[('pending', 'pending'), ('packed', 'packed'), ('shipped', 'shipped'), ('delivered', 'delivered'), ('cancelled', 'cancelled')], default='pending', max_length=150),
        ),
    ]
