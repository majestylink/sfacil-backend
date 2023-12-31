# Generated by Django 4.2 on 2023-09-04 13:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inventory', '0004_alter_rawmaterial_category_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CoverMaterialTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('transaction_date', models.DateTimeField()),
                ('transaction_type', models.CharField(choices=[('purchase', 'Purchase'), ('usage', 'Usage')], max_length=20)),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cost_per_unit', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cover_material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.covermaterial')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cover_material_transactions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AccessoryTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('transaction_date', models.DateTimeField()),
                ('transaction_type', models.CharField(choices=[('purchase', 'Purchase'), ('usage', 'Usage')], max_length=20)),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cost_per_unit', models.DecimalField(decimal_places=2, max_digits=10)),
                ('accessory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.accessory')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accessory_transactions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
