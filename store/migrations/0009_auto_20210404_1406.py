# Generated by Django 3.1.7 on 2021-04-04 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_auto_20210404_1136'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deliveryinfo',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='deliveryinfo',
            name='last_name',
        ),
        migrations.AddField(
            model_name='deliveryinfo',
            name='mobile_number',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='deliveryinfo',
            name='city',
            field=models.CharField(choices=[('1', 'Santiago'), ('2', 'Quirino')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='deliveryinfo',
            name='province',
            field=models.CharField(choices=[('1', 'Isabela'), ('2', 'Something')], max_length=200, null=True),
        ),
    ]
