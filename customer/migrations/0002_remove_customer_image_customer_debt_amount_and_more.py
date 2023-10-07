# Generated by Django 4.2 on 2023-08-25 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='image',
        ),
        migrations.AddField(
            model_name='customer',
            name='debt_amount',
            field=models.DecimalField(decimal_places=2, default=4000000, max_digits=12),
        ),
        migrations.AddField(
            model_name='customer',
            name='remaining_credit',
            field=models.DecimalField(decimal_places=2, default=4000000, max_digits=10),
        ),
    ]
