# Generated by Django 3.1.7 on 2021-04-04 03:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_auto_20210404_1132'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliveryinfo',
            name='first_name',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='deliveryinfo',
            name='last_name',
            field=models.CharField(default='', max_length=200),
        ),
    ]
