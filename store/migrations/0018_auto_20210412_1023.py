# Generated by Django 3.1.7 on 2021-04-12 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0017_remove_customer_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='mobile_number',
            field=models.CharField(blank=True, max_length=12, null=True, unique=True),
        ),
    ]