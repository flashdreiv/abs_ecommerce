# Generated by Django 3.1.7 on 2021-04-05 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_remove_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(blank=True, choices=[('1', 'Order confirmed'), ('2', 'Picked by courier'), ('3', 'On the way'), ('4', 'Delivered')], max_length=80, null=True),
        ),
    ]
