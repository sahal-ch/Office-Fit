# Generated by Django 4.0.4 on 2022-06-19 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0013_alter_orderproduct_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderproduct',
            name='is_paid',
            field=models.BooleanField(default=False),
        ),
    ]
